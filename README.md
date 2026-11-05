# ovd.coffee — web de ØVD (copia estática de la tienda de Shopify)

Copia fiel de https://ovdcoffee.com (español en `/`, inglés en `/en/`) para publicar en GitHub Pages. Se genera con `tools/mirror.py`: descarga el HTML renderizado, CSS, fuentes e imágenes (1400 px, JPG), quita los scripts de Shopify y sustituye el botón de compra por enlaces de pago de Stripe.

- **Enlaces de pago:** edita `payment_links.json` (una URL `https://buy.stripe.com/…` por producto y opción; `"*"` = enlace por defecto) y ejecuta `python3 tools/mirror.py --offline`. Sin enlace, el botón muestra «Próximamente».
- **Volver a copiar la web de Shopify:** `python3 tools/mirror.py` (necesita internet; Shopify puede bloquear con su verificación anti-bot).
- **Publicar:** GitHub → Settings → Pages → *Deploy from a branch* → `main` / `(root)`.
- **Dominio:** apuntar ovdcoffee.com a GitHub Pages desde Hostinger solo cuando la compra esté probada.
- **Qué no existe en la copia:** carrito, cuenta de cliente, búsqueda, reseñas de Judge.me, formularios de Shopify (newsletter, contacto) y sus códigos de descuento.

No se guardan credenciales en este repo.
