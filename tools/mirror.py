#!/usr/bin/env python3
"""Copia estática de https://ovdcoffee.com (Shopify) para GitHub Pages.
Descarga el HTML renderizado, CSS, fuentes e imágenes; quita los scripts de Shopify y cambia el botón de compra por enlaces de Stripe
(payment_links.json). Uso: python3 tools/mirror.py [--offline]   (--offline reutiliza el HTML ya descargado en tools/cache/)."""
import re, os, sys, json, time, hashlib, subprocess, urllib.parse
from bs4 import BeautifulSoup

SITE = 'https://ovdcoffee.com'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, 'tools', 'cache'); os.makedirs(CACHE, exist_ok=True)
OFFLINE = '--offline' in sys.argv
HANDLES = ['citrus-shock', 'forbidden-roast', 'guilty-pleasure', 'ovd-duo', 'ovd-full-series']
PAGES = ['', 'collections/all', 'pages/the-lab'] + [f'products/{h}' for h in HANDLES]
PAGES = PAGES + ['en/' + p if p else 'en' for p in PAGES]
LEGAL = ['policies/privacy-policy']
LINKS = json.load(open(os.path.join(ROOT, 'payment_links.json'), encoding='utf-8'))

def curl(url, out):
    for _ in range(3):
        r = subprocess.run(['curl', '-sSL', '-m', '60', '-A', 'Mozilla/5.0', '-o', out, '-w', '%{http_code}', url], capture_output=True, text=True)
        if r.stdout == '200': return True
        time.sleep(2)
    return False

def fetch_page(path):
    f = os.path.join(CACHE, (path or 'home').replace('/', '_') + '.html')
    if not (OFFLINE and os.path.exists(f)):
        url = f'{SITE}/{path}' + ('?view=ovrdose' if path.split('/')[-2:-1] == ['products'] else '')
        if not curl(url, f): return None
        time.sleep(1)
    return open(f, encoding='utf-8', errors='ignore').read()

ASSETS = os.path.join(ROOT, 'assets')
done = {}
def asset(url, kind, base_url=SITE):
    """Descarga un recurso y devuelve su ruta local (relativa a la raíz del sitio) o None."""
    url = urllib.parse.urljoin(base_url + '/', url if not url.startswith('//') else 'https:' + url)
    u = urllib.parse.urlparse(url)
    if u.netloc not in ('ovdcoffee.com', 'cdn.shopify.com', 'www.ovdcoffee.com'): return None
    key = u.netloc + u.path
    if key in done: return done[key]
    name = os.path.basename(u.path)
    if kind == 'img':
        stem = os.path.splitext(name)[0]; local = f'assets/img/{stem}.jpg'; dl = f'{SITE}{u.path}?width=1400&format=jpg' if u.netloc == 'ovdcoffee.com' else f'{url.split("?")[0]}?width=1400&format=jpg'
    elif kind == 'font': local = f'assets/fonts/{name}'; dl = url
    elif kind == 'css': local = f'assets/css/{name}'; dl = url
    else: local = f'assets/other/{name}'; dl = url
    dest = os.path.join(ROOT, local); os.makedirs(os.path.dirname(dest), exist_ok=True)
    if not os.path.exists(dest) and not curl(dl, dest): print('FALLO', dl); done[key] = None; return None
    if kind == 'css': fix_css(dest, url)
    done[key] = local; return local

def fix_css(path, css_url):
    css = open(path, encoding='utf-8', errors='ignore').read()
    def rep(m):
        raw = m.group(2).strip()
        if raw.startswith('data:') or raw.startswith('#'): return m.group(0)
        ext = os.path.splitext(urllib.parse.urlparse(raw).path)[1].lower()
        kind = 'font' if ext in ('.woff', '.woff2', '.ttf', '.otf') else 'img' if ext in ('.png', '.jpg', '.jpeg', '.webp', '.gif') else 'other'
        loc = asset(raw, kind, css_url.rsplit('/', 1)[0])
        return f'url({m.group(1)}../../{loc}{m.group(1)})' if loc else m.group(0)
    css = re.sub(r'url\((["\']?)([^)"\']+)\1\)', lambda m: rep(m) if m.group(2) else m.group(0), css)
    open(path, 'w', encoding='utf-8').write(css)

def local_url(u, depth, kind_hint=None):
    """URL de recurso -> ruta local relativa; si no es recurso conocido, se devuelve igual."""
    ext = os.path.splitext(urllib.parse.urlparse(u).path)[1].lower()
    kind = kind_hint or ('img' if ext in ('.png', '.jpg', '.jpeg', '.webp', '.gif') else 'font' if ext in ('.woff', '.woff2') else 'css' if ext == '.css' else None)
    if not kind or 'judge.me' in u or 'judgeme' in u: return u
    loc = asset(u, kind)
    return ('../' * depth) + loc if loc else u

def inner_link(href, depth, lang_en):
    if href.startswith('//') or re.match(r'^https?://', href):
        m = re.match(r'^https?://(www\.)?ovdcoffee\.com(/.*)?$', href)
        if not m: return href
        href = m.group(2) or '/'
    if not href.startswith('/'): return href
    path = href.split('#')[0].split('?')[0].strip('/'); frag = ('#' + href.split('#')[1]) if '#' in href else ''
    pre = '../' * depth
    if path in PAGES or path in LEGAL or ('en/' + path) in LEGAL:
        return (pre + path + '/' if path else pre or './') + frag
    if path == 'en': return pre + 'en/' + frag
    return '#'  # carrito, cuenta, búsqueda, etc.: no existen en la web estática

def build_buy(soup, handle, en):
    form = soup.find('product-form-component')
    if not form: return
    old_btn = form.find('button', class_='add-to-cart-button')
    cls = ' '.join(old_btn.get('class', [])) if old_btn else 'button'
    wrap = form.find_parent(class_='buy-buttons-block') or form
    label = 'BUY NOW' if en else 'COMPRAR'
    new = BeautifulSoup(f'<div class="ovd-stripe"><a id="ovd-buy" class="{cls}" href="#" data-label="{label}" data-soon="{"COMING SOON" if en else "PRÓXIMAMENTE"}">{label}</a>'
                        f'<p class="ovd-stripe__note">{"SECURE PAYMENT WITH STRIPE." if en else "PAGO SEGURO CON STRIPE."}</p></div>', 'lxml').div
    wrap.replace_with(new)
    sc = soup.new_tag('script'); sc.string = ('(function(){var L=%s,a=document.getElementById("ovd-buy");function k(){var v=[];document.querySelectorAll("variant-picker input[type=radio]:checked").forEach(function(i){v.push(i.value)});return v.join(" / ")}'
        'function u(){var url=L[k()]||L["*"]||"";if(url){a.href=url;a.textContent=a.dataset.label;a.removeAttribute("aria-disabled")}else{a.removeAttribute("href");a.textContent=a.dataset.soon;a.setAttribute("aria-disabled","true")}}'
        'document.addEventListener("change",u);u()})();') % json.dumps({k: v for k, v in LINKS.get(handle, {}).items() if not k.startswith('_')})
    soup.body.append(sc)

CSS_EXTRA = '''
/* añadido por tools/mirror.py: sin carrito, cuenta ni búsqueda (no existen en la web estática) */
cart-icon,.header-actions__cart,.header-actions__action[href*="account"],.header__column--right .search-action,predictive-search-component,account-button,
.ovd-lang{color:inherit;font-family:var(--font-ovrdose-display,inherit);font-size:1.4rem;letter-spacing:.05em;text-decoration:none;margin-right:1rem}
header-actions,.account-button,shopify-account,shopify-store,.cart-drawer,cart-drawer-component,#cart-icon,.header-actions,localization-form-component,.localization-form{display:none!important}
.ovd-stripe{margin:1rem 0}.ovd-stripe a{display:block;text-align:center;text-decoration:none;cursor:pointer;padding:1rem 1.5rem}.ovd-stripe a[aria-disabled]{opacity:.5;pointer-events:none}
.ovd-stripe__note{font-size:.8rem;opacity:.7;margin:.4rem 0 0}
@media(max-width:749px){body{--header-height:80px!important;--header-group-height:140px!important;--top-row-height:80px!important}}
'''

def process(path, html):
    en = path == 'en' or path.startswith('en/')
    depth = len(path.split('/')) if path else 0
    soup = BeautifulSoup(html, 'lxml')
    for s in soup.find_all('script'):
        if s.get('type') != 'application/ld+json': s.decompose()
    for l in soup.find_all('link'):
        rel = ' '.join(l.get('rel', []))
        if any(x in rel for x in ('preload', 'modulepreload', 'prefetch', 'preconnect', 'dns-prefetch')) or 'judge' in l.get('href', ''): l.decompose()
    for e in soup.select('[class*="jdgm"],[id*="judge"],[data-judgeme]'): e.decompose()
    for l in soup.find_all('link', rel='stylesheet'):
        href = l.get('href', '')
        if 'fonts.googleapis' in href: continue
        loc = local_url(href, depth, 'css')
        if loc == href: l.decompose()
        else: l['href'] = loc
    for st in soup.find_all('style'):
        if st.string and 'url(' in st.string:
            def rep(m):
                u = m.group(2); ext = os.path.splitext(urllib.parse.urlparse(u).path)[1].lower()
                if u.startswith('data:'): return m.group(0)
                r = local_url(u, depth); return f'url({m.group(1)}{r}{m.group(1)})'
            st.string = re.sub(r'url\((["\']?)([^)"\']+)\1\)', rep, st.string)
    for t in soup.find_all(True):
        for a in ('src', 'poster', 'data-src'):
            if t.get(a): t[a] = local_url(t[a], depth)
        if t.get('srcset'):
            cands = [c.strip().split() for c in t['srcset'].split(',') if c.strip()]
            best = max(cands, key=lambda c: int(c[1][:-1]) if len(c) > 1 and c[1][:-1].isdigit() else 0)[0]
            if t.name == 'img' and not t.get('src'): t['src'] = local_url(best, depth)
            elif t.name == 'source': t['srcset'] = local_url(best, depth)
            if t.name == 'img': del t['srcset']; t.attrs.pop('sizes', None)
        if t.get('style') and 'url(' in t['style']:
            t['style'] = re.sub(r'url\((["\']?)([^)"\']+)\1\)', lambda m: f'url({m.group(1)}{local_url(m.group(2), depth)}{m.group(1)})', t['style'])
        if t.name in ('a', 'link') and t.get('href') and t.get('rel') != ['stylesheet']:
            if t.name == 'a' or t.get('rel') in (['canonical'], ['alternate']): t['href'] = inner_link(t['href'], depth, en)
        if t.name == 'meta' and t.get('property') == 'og:image' and t.get('content'): t['content'] = local_url(t['content'], depth)
    # botón de idioma: enlace directo a la otra versión
    other = path[3:] if en else ('en/' + path if path else 'en')
    pre = '../' * depth
    if en: other_href = pre + (other + '/' if other else '')
    else: other_href = pre + other + '/'
    if not other_href.strip('./'): other_href = pre or './'
    col = soup.select_one('.header__column--right')
    if col and not col.find(class_='ovd-lang'):
        col.insert(0, BeautifulSoup(f'<a class="ovd-lang" href="{other_href}">{"ESPAÑOL" if en else "ENGLISH"}</a>', 'lxml').a)
    m = re.match(r'products/([\w-]+)$', path[3:] if en else path)
    if m: build_buy(soup, m.group(1), en)
    for f in soup.find_all('form'):
        if f.get('action', '').split('?')[0].endswith(('/cart/add', '/cart', '/localization', '/search')): f.decompose()
    # estado que en Shopify pone su JS al cargar (menú de escritorio, alturas de cabecera)
    hc = soup.find('header-component')
    if hc: hc['data-menu-style'] = 'menu'
    for e in soup.select('.shopify-section'): e['data-hydrated'] = 'true'
    if soup.body: soup.body['style'] = '--header-height: 96px; --header-group-height: 156px; --transparent-header-offset-boolean: 0; --top-row-height: 96px;'
    st = soup.new_tag('style'); st.string = CSS_EXTRA; soup.head.append(st)
    return str(soup)

def main():
    for p in PAGES + (['en/' + x for x in LEGAL] + LEGAL):
        h = fetch_page(p)
        if h is None: print('sin página', p); continue
        out = os.path.join(ROOT, p, 'index.html') if p else os.path.join(ROOT, 'index.html')
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, 'w', encoding='utf-8').write(process(p, h)); print('ok', p or '/')
main()
