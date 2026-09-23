(() => {
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)');
  const topButton = document.querySelector('.to-top');
  topButton.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: reduceMotion.matches ? 'instant' : 'smooth' });
    document.querySelector('.brand').focus({ preventScroll: true });
  });

  const menuButton = document.querySelector('.toc-fab');
  const menu = document.querySelector('.toc-sheet');
  const menuList = document.querySelector('#toc-list').cloneNode(true);
  menuList.removeAttribute('id');
  menu.append(menuList);
  function positionMenu() {
    menu.style.top = `${menuButton.getBoundingClientRect().bottom + 10}px`;
  }
  function setMenu(open, restoreFocus = false) {
    menu.classList.toggle('open', open);
    menuButton.setAttribute('aria-expanded', String(open));
    menuButton.textContent = open ? '목차 닫기 −' : '목차 +';
    if (open) { positionMenu(); menu.querySelector('a').focus({ preventScroll: true }); }
    else if (restoreFocus) menuButton.focus();
  }
  menuButton.addEventListener('click', () => setMenu(!menu.classList.contains('open')));
  menu.addEventListener('click', (event) => {
    const link = event.target.closest('a');
    if (!link) return;
    setMenu(false);
    const target = document.querySelector(link.getAttribute('href'));
    if (target) {
      target.setAttribute('tabindex', '-1');
      target.focus({ preventScroll: true });
    }
  });
  document.addEventListener('click', (event) => {
    if (!menu.contains(event.target) && !menuButton.contains(event.target)) setMenu(false);
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && menu.classList.contains('open')) setMenu(false, true);
  });
  matchMedia('(min-width: 851px)').addEventListener('change', (event) => {
    if (event.matches) setMenu(false);
  });

  const links = [...document.querySelectorAll('.toc a, .toc-sheet a')];
  const ids = [...new Set(links.map(a => a.getAttribute('href').slice(1)))];
  const sections = ids.map(id => document.getElementById(id)).filter(Boolean);
  let pending = false;
  function updateNavigation() {
    pending = false;
    if (menu.classList.contains('open')) positionMenu();
    let current = sections[0].id;
    for (const section of sections) {
      if (section.getBoundingClientRect().top <= innerHeight * .25) current = section.id;
    }
    if (innerHeight + scrollY >= document.documentElement.scrollHeight - 3) current = sections.at(-1).id;
    for (const link of links) {
      const active = link.getAttribute('href') === '#' + current;
      link.classList.toggle('active', active);
      if (active) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    }
    topButton.classList.toggle('show', scrollY > 650);
  }
  addEventListener('scroll', () => {
    if (!pending) { pending = true; requestAnimationFrame(updateNavigation); }
  }, { passive: true });
  addEventListener('resize', updateNavigation);
  updateNavigation();

  const dialog = document.querySelector('.diagram-dialog');
  const stage = dialog.querySelector('.diagram-stage');
  const image = dialog.querySelector('img');
  const zoom = dialog.querySelector('[data-zoom]');
  let previousOverflow = '';
  function setZoom(enlarged) {
    stage.classList.toggle('zoomed', enlarged);
    zoom.setAttribute('aria-pressed', String(enlarged));
    zoom.textContent = enlarged ? '전체 보기 −' : '확대 +';
    stage.scrollTo(0, 0);
  }
  document.querySelectorAll('[data-diagram]').forEach(link => {
    link.addEventListener('click', (event) => {
      if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      if (typeof dialog.showModal !== 'function') return;
      event.preventDefault();
      const figure = link.closest('figure');
      const source = figure.querySelector('img');
      image.src = source.src;
      image.alt = source.alt;
      dialog.querySelector('h2').textContent = figure.querySelector('.figure-title').textContent;
      dialog.querySelector('[data-download]').href = source.src;
      setZoom(innerWidth < 700);
      previousOverflow = document.body.style.overflow;
      document.body.style.overflow = 'hidden';
      dialog.showModal();
    });
  });
  zoom.addEventListener('click', () => setZoom(!stage.classList.contains('zoomed')));
  dialog.querySelector('[data-close]').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', (event) => {
    const box = dialog.getBoundingClientRect();
    if (event.target === dialog && (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom)) dialog.close();
  });
  dialog.addEventListener('close', () => { document.body.style.overflow = previousOverflow; });
})();
