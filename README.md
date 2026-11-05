# ovd.coffee — web de ØVD (estática)

Sustituye a la tienda de Shopify. HTML/CSS estático en español (`es/`) e inglés (`en/`); la compra va por enlaces de pago de Stripe.

- **Cambiar enlaces de pago:** edita `payment_links.json` (una URL `https://buy.stripe.com/…` por producto y formato) y ejecuta `python3 build.py`.
- **Textos de los cafés:** `data/products.json` (extraídos del theme de Shopify exportado el 02/11/2026).
- **Imágenes:** `img/` (copias de las imágenes de respaldo del theme; las fotos que estaban subidas a Shopify no vienen en el export).
- **Publicar:** GitHub → Settings → Pages → *Deploy from a branch* → `main` / `(root)`.
- **Dominio:** al final, apuntar ovdcoffee.com a GitHub Pages desde Hostinger. No antes de probar la compra.

No se guardan credenciales en este repo.
