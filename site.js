// Botones de formato (grano/molido): cambian el enlace de pago. Sin enlace configurado, el botón muestra «Próximamente».
document.querySelectorAll('.fmts').forEach(g => {
  const buy = g.parentElement.querySelector('.buy');
  const set = b => { const u = b.dataset.url; g.querySelectorAll('.fmt').forEach(x => x.classList.toggle('on', x === b));
    if (u) { buy.href = u; buy.textContent = buy.dataset.buy; buy.classList.remove('off'); } else { buy.removeAttribute('href'); buy.textContent = buy.dataset.soon; buy.classList.add('off'); } };
  g.querySelectorAll('.fmt').forEach(b => b.addEventListener('click', () => set(b)));
});
