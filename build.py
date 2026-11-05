#!/usr/bin/env python3
"""Genera la web estática (es/ y en/) a partir de data/products.json y payment_links.json.
Uso: python3 build.py   (edita payment_links.json y vuelve a ejecutar para cambiar enlaces de pago)."""
import json, html, os, shutil

P = json.load(open('data/products.json', encoding='utf-8'))
LINKS = json.load(open('payment_links.json', encoding='utf-8'))
PRICE = {'citrus-shock': '23,99', 'forbidden-roast': '23,99', 'guilty-pleasure': '23,99'}  # packs: pendiente de confirmar
H = html.escape
HANDLES = ['citrus-shock', 'forbidden-roast', 'guilty-pleasure']
IMG = {  # imágenes de respaldo del theme (imgur) descargadas en img/
    'citrus-shock': ['B75CkFa', 'sKH3FNF', '3f3XBr7'],
    'forbidden-roast': ['4SodpZy', 'ym4Ut3y', 'R014k60'],
    'guilty-pleasure': ['KqGL5Rg', 'E6jgxKN', '0eLn6DU'],
}
T = {  # textos de interfaz
 'en': dict(lang='en', other='es', other_label='Español', home='HOME', catalog='CATALOG', lab='THE LAB', ship='FREE SHIPPING ON EVERY ORDER',
   title='ØVD Coffee · Experimental specialty coffee', desc='Three specialty coffees with clear profiles: Citrus Shock, Forbidden Roast and Guilty Pleasure. Whole bean or ground, 250 g. Free shipping, dispatched in 24–48 h.',
   kicker='EXPERIMENTAL SPECIALTY COFFEE.', h1='COFFEE FOR PEOPLE WHO ARE TOO MUCH.', sub='THREE REAL COFFEES. THREE CLEAR PROFILES. MAXIMUM QUALITY WITHOUT THE LECTURE.',
   choose='CHOOSE YOUR EXPERIMENT', formulas='CURRENT FORMULAS / 001—003', instinct='CHOOSE BY INSTINCT.', instinct_sub='THREE REAL COFFEES. THREE CLEAR PROFILES. NO LECTURE REQUIRED.',
   shop='SHOP EXPERIMENT', exp='EXPERIMENT', ways='START HERE / THREE WAYS IN', level='CHOOSE YOUR LEVEL OF COMMITMENT.',
   p1k='01 / PICK ONE', p1h='CHOOSE YOUR EXPERIMENT.', p1c='THREE CLEAR PROFILES. START WITH THE ONE THAT SOUNDS LIKE YOU.', p1b='COMPARE THE SERIES',
   p2k='02 / PICK TWO', p2h='TWO EXPERIMENTS. YOUR CALL.', p2c='CHOOSE TWO 250 G BAGS. BUILD THE PAIR THAT SOUNDS LIKE YOU.', p2b='BUILD YOUR PAIR',
   p3k='03 / TAKE ALL THREE', p3h='THE FULL SERIES.', p3c='001. 002. 003. THE COMPLETE SERIES IN ONE ORDER.', p3b='SHOP THE BUNDLE',
   labk='THE LAB / WHY ØVD EXISTS', labh='YOU DON’T NEED TO BE A GEEK.', labc='YOU CAN LIKE SPECIALTY COFFEE BECAUSE IT TASTES GREAT, LOOKS GOOD AND FEELS CONSIDERED. ØVD IS FOR PEOPLE WHO NOTICE DETAILS, DO THINGS PROPERLY AND LIKE THEM BEAUTIFULLY MADE. MAXIMUM QUALITY. ZERO GATEKEEPING.', labb='ENTER THE LAB',
   revk='REAL PEOPLE / REAL REACTIONS', revh='PROOF, NOT PROMISES.', folk='FIELD NOTES / CONTROLLED DISORDER', folh='FOLLOW THE EXPERIMENT.', closing='COFFEE FOR PEOPLE WHO ARE TOO MUCH.',
   whole='WHOLE BEAN', ground='GROUND', buy='BUY NOW', soon='COMING SOON', fmt='FORMAT', note='FREE DELIVERY ON EVERY ORDER / SECURE CHECKOUT.', disp='DISPATCHED IN 24–48 H',
   roast='ROAST', best='BEST FOR', origin='ORIGIN', farm='PRODUCER / LOT', alt='ALTITUDE', proc='PROCESS', var='VARIETY', score='SCORE', profile='PROFILE', cup='IN THE CUP', also='ALSO TRY',
   bags2='2 × 250 G / CHOOSE YOUR TWO COFFEES', bags3='3 × 250 G / THE COMPLETE SERIES', duo='X2 EXPERIMENTS', trio='THE COMPLETE SERIES',
   duo_d='Choose two ØVD experiments and build your own pairing. Two 250 g bags, selected by instinct.', trio_d='Citrus Shock, Forbidden Roast and Guilty Pleasure together. Three 250 g bags, the complete ØVD series.',
   duo_n='After paying, tell us at hello@ovdcoffee.com which two coffees you want (or choose them in the payment form).', trio_n='',
   status='ACTIVE / AVAILABLE', labhero='WE DON’T RELEASE PRODUCTS. WE RELEASE EXPERIMENTS.', labstory='SPECIALTY COFFEE. NO GATEKEEPING.',
   lp1='YOU DO NOT HAVE TO BE A COFFEE GEEK TO LIKE SPECIALTY COFFEE. ØVD IS FOR PEOPLE WHO CARE ABOUT HOW THINGS TASTE, LOOK AND FEEL.', lp2='FOR PEOPLE WHO WORK HARD, NOTICE THE DETAILS AND LIKE THINGS DONE PROPERLY—AND BEAUTIFULLY.', lp3='HIGH-QUALITY SPECIALTY COFFEE WITHOUT PRETENSION, GATEKEEPING OR BULLSHIT.',
   steps=[('CHOOSE','WE SELECT DISTINCT SPECIALTY COFFEES FOR QUALITY, CHARACTER AND HOW GOOD THEY FEEL TO DRINK.'),('DETAIL','TASTE, FORMAT, PHOTOGRAPHY AND DESIGN ARE TREATED AS ONE EXPERIENCE. DETAILS ARE THE POINT.'),('ENJOY','CLEAR GUIDANCE, NO GATEKEEPING AND NO JARGON TEST. JUST MAKE IT THE WAY YOU LIKE IT.')],
   contact='CONTACT THE LAB.', contact_c='GENERAL / WHOLESALE / COLLABORATIONS / PRESS', brew='BREWING / STARTING POINTS', brewh='MAKE IT YOURS.', brewn='STARTING POINTS ONLY. ADJUST TO YOUR EQUIPMENT, WATER AND TASTE.', coffee='COFFEE', water='WATER', time='TIME', inn='IN', out='OUT',
   rev=[('Muy buen café. Se nota que hay producto detrás, pero sin complicaciones: buen sabor, buena presentación y dan ganas de probar los otros.','Laura F.','THE COMPLETE SERIES'),('Citrus Shock tiene bastante carácter pero sigue siendo muy fácil de beber. El toque cítrico se nota sin hacerse raro y en espresso queda increíble.','Marta C.','EXPERIMENT 001 // CITRUS SHOCK'),('Me ha sorprendido muchísimo. Es dulce, muy fácil de beber y tiene un punto diferente a los cafés que suelo comprar. Repetiré seguro.','Isa G.','EXPERIMENT 003 // GUILTY PLEASURE')]),
 'es': dict(lang='es', other='en', other_label='English', home='INICIO', catalog='CATÁLOGO', lab='THE LAB', ship='ENVÍO GRATIS EN TODOS LOS PEDIDOS',
   title='ØVD Coffee · Café de especialidad experimental', desc='Tres cafés de especialidad con perfiles claros: Citrus Shock, Forbidden Roast y Guilty Pleasure. Grano o molido, 250 g. Envío gratis, salida en 24–48 h.',
   kicker='CAFÉ DE ESPECIALIDAD EXPERIMENTAL.', h1='CAFÉ PARA GENTE QUE ES DEMASIADO.', sub='TRES CAFÉS REALES. TRES PERFILES CLAROS. MÁXIMA CALIDAD SIN LECCIONES.',
   choose='ELIGE TU EXPERIMENTO', formulas='FÓRMULAS ACTUALES / 001—003', instinct='ELIGE POR INSTINTO.', instinct_sub='TRES CAFÉS REALES. TRES PERFILES CLAROS. SIN LECCIONES.',
   shop='COMPRAR EXPERIMENTO', exp='EXPERIMENTO', ways='EMPIEZA AQUÍ / TRES FORMAS DE ENTRAR', level='ELIGE TU NIVEL DE COMPROMISO.',
   p1k='01 / ELIGE UNO', p1h='ELIGE TU EXPERIMENTO.', p1c='TRES PERFILES CLAROS. EMPIEZA POR EL QUE SUENE A TI.', p1b='COMPARA LA SERIE',
   p2k='02 / ELIGE DOS', p2h='DOS EXPERIMENTOS. TÚ DECIDES.', p2c='ELIGE DOS BOLSAS DE 250 G. MONTA LA PAREJA QUE SUENE A TI.', p2b='MONTA TU PAREJA',
   p3k='03 / LLÉVATE LOS TRES', p3h='LA SERIE COMPLETA.', p3c='001. 002. 003. LA SERIE COMPLETA EN UN SOLO PEDIDO.', p3b='COMPRAR EL PACK',
   labk='THE LAB / POR QUÉ EXISTE ØVD', labh='NO HACE FALTA SER UN FRIKI.', labc='PUEDE GUSTARTE EL CAFÉ DE ESPECIALIDAD PORQUE SABE GENIAL, SE VE BIEN Y SE SIENTE CUIDADO. ØVD ES PARA GENTE QUE SE FIJA EN LOS DETALLES, HACE LAS COSAS BIEN Y LAS QUIERE BONITAS. MÁXIMA CALIDAD. CERO BARRERAS.', labb='ENTRA EN THE LAB',
   revk='GENTE REAL / REACCIONES REALES', revh='PRUEBAS, NO PROMESAS.', folk='NOTAS DE CAMPO / DESORDEN CONTROLADO', folh='SIGUE EL EXPERIMENTO.', closing='CAFÉ PARA GENTE QUE ES DEMASIADO.',
   whole='GRANO', ground='MOLIDO', buy='COMPRAR', soon='PRÓXIMAMENTE', fmt='FORMATO', note='ENVÍO GRATIS EN TODOS LOS PEDIDOS / PAGO SEGURO.', disp='SALIDA EN 24–48 H',
   roast='TUESTE', best='IDEAL PARA', origin='ORIGEN', farm='PRODUCTOR / LOTE', alt='ALTITUD', proc='PROCESO', var='VARIEDAD', score='PUNTUACIÓN', profile='PERFIL', cup='EN TAZA', also='PRUEBA TAMBIÉN',
   bags2='2 × 250 G / ELIGE TUS DOS CAFÉS', bags3='3 × 250 G / SERIE COMPLETA', duo='X2 EXPERIMENTS', trio='THE COMPLETE SERIES',
   duo_d='Elige dos experimentos ØVD y crea tu propia combinación. Dos bolsas de 250 g, elegidas por instinto.', trio_d='Citrus Shock, Forbidden Roast y Guilty Pleasure juntos. Tres bolsas de 250 g, la serie ØVD completa.',
   duo_n='Después de pagar, escríbenos a hello@ovdcoffee.com con los dos cafés que quieres (o elígelos en el formulario de pago).', trio_n='',
   status='ACTIVO / DISPONIBLE', labhero='NO LANZAMOS PRODUCTOS. LANZAMOS EXPERIMENTOS.', labstory='CAFÉ DE ESPECIALIDAD. SIN BARRERAS.',
   lp1='NO TIENES QUE SER UN FRIKI DEL CAFÉ PARA DISFRUTAR DEL CAFÉ DE ESPECIALIDAD. ØVD ES PARA GENTE QUE SE FIJA EN CÓMO SABE, SE VE Y SE SIENTE ALGO.', lp2='PARA GENTE QUE TRABAJA DURO, SE FIJA EN LOS DETALLES Y QUIERE LAS COSAS BIEN HECHAS, Y BONITAS.', lp3='CAFÉ DE ESPECIALIDAD DE ALTA CALIDAD, SIN PRETENSIÓN NI CÓDIGOS DE ENTRADA.',
   steps=[('ELIGE','SELECCIONAMOS CAFÉS DE ESPECIALIDAD DISTINTOS POR CALIDAD, CARÁCTER Y LO BIEN QUE SE BEBEN.'),('DETALLE','SABOR, FORMATO, FOTOGRAFÍA Y DISEÑO SE TRATAN COMO UNA SOLA EXPERIENCIA. LOS DETALLES SON LO IMPORTANTE.'),('DISFRUTA','GUÍA CLARA, SIN BARRERAS Y SIN EXAMEN DE JERGA. PREPÁRALO COMO TE GUSTE.')],
   contact='CONTACTA CON THE LAB.', contact_c='GENERAL / MAYORISTAS / COLABORACIONES / PRENSA', brew='PREPARACIÓN / PUNTOS DE PARTIDA', brewh='HAZLO A TU MANERA.', brewn='SOLO PUNTOS DE PARTIDA. AJUSTA A TU EQUIPO, AGUA Y GUSTO.', coffee='CAFÉ', water='AGUA', time='TIEMPO', inn='ENTRADA', out='SALIDA', rev=None),
}
T['es']['rev'] = T['en']['rev']
NAMES = {'citrus-shock': 'CITRUS SHOCK', 'forbidden-roast': 'FORBIDDEN ROAST', 'guilty-pleasure': 'GUILTY PLEASURE'}

def prod(h, lang):
    d = dict(P[h]['en']); d.update(P[h]['es'] if lang == 'es' else {})
    return d

def buy_box(handle, t, price, fmtlabel):
    ln = LINKS.get(handle, {})
    btns = ''.join(f'<button type="button" class="fmt{" on" if i==0 else ""}" data-url="{H(ln.get(k,""))}">{H(t[k if k=="ground" else "whole"])}</button>' for i, k in enumerate(['bean', 'ground']))
    first = ln.get('bean', '')
    cta = f'<a class="buy" href="{H(first)}" data-soon="{H(t["soon"])}" data-buy="{H(t["buy"])}">{H(t["buy"] if first else t["soon"])}</a>'
    return (f'<p class="price">{("€"+price) if price else ""}</p><p class="small">{H(fmtlabel)}</p><div class="fmts">{btns}</div>{cta}'
            f'<p class="small">{H(t["note"])}<br>{H(t["disp"])}</p>')

def page(t, name, body, depth=1, accent='#050505'):
    L = t['lang']; up = '../'
    nav = (f'<a href="index.html">{t["home"]}</a><a href="index.html#catalog">{t["catalog"]}</a><a href="the-lab.html">{t["lab"]}</a>'
           f'<a href="../{t["other"]}/{name}.html" lang="{t["other"]}">{t["other_label"]}</a>')
    return f'''<!doctype html><html lang="{L}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{H(t["title"])}</title><meta name="description" content="{H(t["desc"])}"><link rel="alternate" hreflang="{t["other"]}" href="../{t["other"]}/{name}.html">
<link rel="icon" href="{up}img/B75CkFa.jpeg"><link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}style.css"></head><body style="--accent:{accent}">
<div class="ticker"><div>{(" ".join([H(t["ship"])]*12))}</div></div>
<header><a class="logo" href="index.html">OVD EXPERIMENTAL COFFEE BRAND</a><nav>{nav}</nav></header>
{body}
<footer><p>{H(t["closing"])}</p><p><a href="mailto:hello@ovdcoffee.com">hello@ovdcoffee.com</a> · <a href="https://www.instagram.com/ovdcoffee/">@OVDCOFFEE</a></p></footer>
<script src="{up}site.js"></script></body></html>'''

def home(t):
    cards = ''
    for i, h in enumerate(HANDLES):
        d = prod(h, t['lang'])
        cards += (f'<a class="card" href="{h}.html" style="--accent:{d["accent_color"]}"><img src="../img/{IMG[h][0]}.jpeg" alt="{NAMES[h]}" loading="lazy">'
                  f'<span>{t["exp"]} 00{i+1}</span><h3>{NAMES[h]}</h3><p>{H(d["sensory_notes"])}</p><b>€{PRICE[h]} · {t["shop"]} →</b></a>')
    d1 = prod('citrus-shock', t['lang'])
    ways = ''.join(f'<a class="way" href="{u}"><img src="../img/{im}.jpeg" alt="" loading="lazy"><span>{k}</span><h3>{hh}</h3><p>{c}</p><b>{b} →</b></a>'
                   for k, hh, c, b, u, im in [(t['p1k'], t['p1h'], t['p1c'], t['p1b'], '#catalog', '4SodpZy'), (t['p2k'], t['p2h'], t['p2c'], t['p2b'], 'ovd-duo.html', 'KqGL5Rg'), (t['p3k'], t['p3h'], t['p3c'], t['p3b'], 'ovd-full-series.html', '0eLn6DU')])
    revs = ''.join(f'<blockquote>“{H(q)}”<cite>{n}<br><small>{H(dd)}</small></cite></blockquote>' for q, n, dd in t['rev'])
    body = f'''<section class="hero" style="background-image:linear-gradient(rgba(0,0,0,.45),rgba(0,0,0,.45)),url(../img/B75CkFa.jpeg)"><p>{t["kicker"]}</p><h1>{t["h1"]}</h1><p>{t["sub"]}</p><a class="btn" href="#catalog">{t["choose"]}</a></section>
<section id="catalog" class="wrap"><p class="k">{t["formulas"]}</p><h2>{t["instinct"]}</h2><p>{t["instinct_sub"]}</p><div class="grid3">{cards}</div></section>
<section class="wrap"><p class="k">{t["ways"]}</p><h2>{t["level"]}</h2><div class="grid3">{ways}</div></section>
<section class="wrap lab"><img src="../img/sKH3FNF.jpeg" alt="" loading="lazy"><div><p class="k">{t["labk"]}</p><h2>{t["labh"]}</h2><p>{t["labc"]}</p><a class="btn" href="the-lab.html">{t["labb"]} ↗</a></div></section>
<section class="wrap"><p class="k">{t["revk"]}</p><h2>{t["revh"]}</h2><div class="grid3 revs">{revs}</div></section>
<section class="wrap"><p class="k">{t["folk"]}</p><h2>{t["folh"]}</h2><p><a href="https://www.instagram.com/ovdcoffee/">@OVDCOFFEE ↗</a> · <a href="mailto:hello@ovdcoffee.com">hello@ovdcoffee.com ↗</a></p></section>'''
    return page(t, 'index', body)

def brew(t):
    rows = [('V60', [(t['coffee'], '18 G'), (t['water'], '270 G'), ('RATIO', '1:15'), (t['time'], '3:20')]),
            ('ESPRESSO', [(t['inn'], '18 G'), (t['out'], '36 G'), ('RATIO', '1:2'), (t['time'], '27—30 S')]),
            ('FRENCH PRESS', [(t['coffee'], '60 G'), (t['water'], '900 G'), ('RATIO', '1:15'), (t['time'], '4:00')])]
    items = ''.join(f'<article><h3>{n}</h3><dl>{"".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in kv)}</dl></article>' for n, kv in rows)
    return f'<section class="wrap dark"><p class="k">{t["brew"]}</p><h2>{t["brewh"]}</h2><div class="grid3">{items}</div><p class="small">{t["brewn"]}</p></section>'

def product(t, h):
    d = prod(h, t['lang']); a = d['accent_color']
    others = [x for x in HANDLES if x != h]
    imgs = ''.join(f'<img src="../img/{i}.jpeg" alt="{NAMES[h]}" loading="{"eager" if n==0 else "lazy"}">' for n, i in enumerate(IMG[h]))
    spec = lambda k, v: f'<div><dt>{k}</dt><dd>{H(v)}</dd></div>'
    body = f'''<section class="pdp"><div class="gallery">{imgs}</div><aside><p class="k">{t["exp"]} {d["experiment_number"]}</p><h1>{NAMES[h]}</h1><p class="notes">{H(d["sensory_notes"])}</p><p>{H(d["fallback_description"])}</p>
{buy_box(h, t, PRICE[h], "250 G / " + t["whole"] + " · " + t["ground"])}</aside></section>
<section class="wrap"><p class="k">{t["cup"]} / {H(d["sensory_notes"])}</p><h2>{H(d["story_headline"])}</h2><p class="lead">{H(d["sensory_copy"])}</p>
<dl class="specs">{spec(t["roast"], d["coffee_roast"])}{spec("FORMAT" if t["lang"]=="en" else "FORMATO", "250 G")}{spec(t["best"], d["coffee_best_for"])}{spec(t["coffee"], "100% ARABICA")}</dl></section>
<section class="wrap"><p class="k">{t["origin"]}</p><h2>{H(d["coffee_origin"])}</h2><p>{H(d["coffee_source_copy"])}</p>
<dl class="specs">{spec(t["farm"], d["coffee_farm"])}{spec(t["alt"], d["coffee_altitude"])}{spec(t["proc"], d["coffee_process"])}{spec(t["var"], d["coffee_variety"])}{spec(t["score"], d["coffee_score"])}{spec(t["profile"], d["sensory_notes"])}</dl></section>
{brew(t)}
<section class="wrap"><p class="k">{t["also"]}</p><div class="grid3">{"".join(f'<a class="card" href="{o}.html" style="--accent:{prod(o,t["lang"])["accent_color"]}"><img src="../img/{IMG[o][0]}.jpeg" alt="" loading="lazy"><h3>{NAMES[o]}</h3><p>{H(prod(o,t["lang"])["sensory_notes"])}</p></a>' for o in others)}</div></section>'''
    return page(t, h, body, accent=a)

def bundle(t, h, trio):
    d = t['trio_d'] if trio else t['duo_d']; n = t['bags3'] if trio else t['bags2']
    title = 'THE COMPLETE SERIES' if trio else 'X2 EXPERIMENTS'
    files = ''.join(f'<p><strong>{t["exp"]} 00{i+1} — {NAMES[x]}</strong><br>{H(prod(x,t["lang"])["sensory_notes"])} · {H(prod(x,t["lang"])["coffee_origin"])} · {H(prod(x,t["lang"])["coffee_roast"])}</p>' for i, x in enumerate(HANDLES))
    img = '0eLn6DU' if trio else 'KqGL5Rg'
    price = PRICE.get(h, '')
    note = '' if trio else f'<p class="small">{H(t["duo_n"])}</p>'
    body = f'''<section class="pdp"><div class="gallery"><img src="../img/{img}.jpeg" alt="{title}"></div><aside><p class="k">{title}</p><h1>{title}</h1><p>{H(d)}</p>
{buy_box(h, t, price, n)}{note}</aside></section><section class="wrap"><p class="k">{n}</p>{files}</section>{brew(t)}'''
    return page(t, h, body)

def lab(t):
    cards = ''.join(f'<a class="card" href="{h}.html" style="--accent:{prod(h,t["lang"])["accent_color"]}"><span>{t["exp"]} 00{i+1}</span><h3>{NAMES[h]}</h3><p>{H(prod(h,t["lang"])["sensory_notes"])}</p><b>{t["status"]}</b></a>' for i, h in enumerate(HANDLES))
    steps = ''.join(f'<article><h3>{a}</h3><p>{b}</p></article>' for a, b in t['steps'])
    body = f'''<section class="hero small"><p>ØVD COFFEE / LAB 001—003</p><h1>THE LAB</h1><p>{t["labhero"]}</p></section>
<section class="wrap"><p class="k">01 / WHY ØVD</p><h2>{t["labstory"]}</h2><p>{t["lp1"]}</p><p>{t["lp2"]}</p><p>{t["lp3"]}</p></section>
<section class="wrap"><p class="k">02 / {t["formulas"]}</p><div class="grid3">{cards}</div></section>
<section class="wrap"><div class="grid3">{steps}</div></section>
<section class="wrap"><p class="k">05 / CONTACT</p><h2>{t["contact"]}</h2><p>{t["contact_c"]}</p><p><a href="mailto:hello@ovdcoffee.com">hello@ovdcoffee.com</a></p></section>'''
    return page(t, 'the-lab', body)

for L, t in T.items():
    os.makedirs(L, exist_ok=True)
    out = {'index': home(t), 'the-lab': lab(t), 'ovd-duo': bundle(t, 'ovd-duo', False), 'ovd-full-series': bundle(t, 'ovd-full-series', True)}
    for h in HANDLES: out[h] = product(t, h)
    for n, c in out.items(): open(f'{L}/{n}.html', 'w', encoding='utf-8').write(c)
open('index.html', 'w', encoding='utf-8').write('<!doctype html><meta charset="utf-8"><title>ØVD Coffee</title><script>location.replace((navigator.language||"es").slice(0,2)==="en"?"en/":"es/")</script><noscript><a href="es/">Español</a> · <a href="en/">English</a></noscript>')
print('ok')
