/* Concept B: The Register. Vanilla JS, no dependencies.
   Motion systems: (1) kinetic variable-font headlines whose weight follows scroll,
   (2) running head with reading progress and section-aware title,
   (3) history line that draws with scroll, (4) cursor-following preview plates,
   (5) page tone that shifts between paper and wash, (6) figure wipes and reveals.
   All of it is disabled or static under prefers-reduced-motion. */
(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var clamp = function (v) { return v < 0 ? 0 : v > 1 ? 1 : v; };

  /* contents panel */
  var btn = $('.run-btn'), toc = $('#toc');
  function setToc(open) { toc.hidden = !open; btn.setAttribute('aria-expanded', open); }
  btn.addEventListener('click', function () { setToc(toc.hidden); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !toc.hidden) { setToc(false); btn.focus(); } });
  document.addEventListener('click', function (e) { if (!toc.hidden && !toc.contains(e.target) && e.target !== btn) setToc(false); });

  /* running head visibility */
  var run = $('[data-run]'), mast = $('.mast');
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (en) { run.classList.toggle('on', !en[0].isIntersecting); }, { rootMargin: '-40px 0px 0px 0px' }).observe(mast);
  } else run.classList.add('on');

  /* section-aware title and page tone */
  var title = $('[data-run-title]'), cur = title.textContent;
  function setTitle(t) {
    if (t === cur) return; cur = t;
    if (reduce) { title.textContent = t; return; }
    title.classList.add('out');
    setTimeout(function () { title.textContent = t; title.classList.remove('out'); }, 240);
  }
  if ('IntersectionObserver' in window) {
    var mid = { rootMargin: '-35% 0px -60% 0px' };
    var lo = new IntersectionObserver(function (en) { en.forEach(function (e) { if (e.isIntersecting) setTitle(e.target.getAttribute('data-run-label')); }); }, mid);
    $$('[data-run-label]').forEach(function (s) { lo.observe(s); });
    var to = new IntersectionObserver(function (en) { en.forEach(function (e) { if (e.isIntersecting) document.body.setAttribute('data-tone', e.target.getAttribute('data-tone-zone')); }); }, { rootMargin: '-50% 0px -49% 0px' });
    $$('[data-tone-zone]').forEach(function (s) { to.observe(s); });
  }

  /* scroll-linked: reading progress, kinetic weight, history line */
  var kin = $$('.kin'), tracks = $$('[data-track]'), base = [], tick = false;
  function kOf(el) { var vh = window.innerHeight, r = el.getBoundingClientRect(); return clamp(1 - (r.top - vh * 0.1) / (vh * 0.8)); }
  kin.forEach(function (el, i) { var k = kOf(el); base[i] = k > 0 ? Math.min(k, 0.9) : 0; });
  function frame() {
    tick = false;
    var vh = window.innerHeight, max = document.documentElement.scrollHeight - vh;
    run.style.setProperty('--read', max > 0 ? clamp(window.scrollY / max).toFixed(4) : 0);
    if (!reduce) kin.forEach(function (el, i) {
      var r = el.getBoundingClientRect();
      if (r.bottom < -50 || r.top > vh + 50) return;
      var k = kOf(el); if (base[i]) k = 0.12 + 0.88 * clamp((k - base[i]) / (1 - base[i]));
      el.style.setProperty('--k', k.toFixed(3));
    });
    tracks.forEach(function (tr) {
      var r = tr.getBoundingClientRect(), items = $$('li', tr), vert = window.innerWidth <= 760;
      var t = reduce ? 1 : vert ? clamp((vh * 0.75 - r.top) / r.height) : clamp((vh * 0.96 - r.top) / (vh * 0.42));
      tr.style.setProperty('--t', t.toFixed(4));
      items.forEach(function (li, i) { li.classList.toggle('on', t >= (i + 0.4) / items.length); });
    });
  }
  window.addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(frame); } }, { passive: true });
  window.addEventListener('resize', frame);
  frame();

  /* preview plates: follow the cursor, or sit beside the row on keyboard focus */
  if (fine && !reduce) {
    $$('.rg-row').forEach(function (row) {
      var p = $('.plate', row); if (!p) return;
      function place(x, y) {
        var w = 300, h = p.offsetHeight || 220;
        x = Math.min(Math.max(12, x), window.innerWidth - w - 12); y = Math.min(Math.max(66, y), window.innerHeight - h - 12);
        p.style.setProperty('--px', x + 'px'); p.style.setProperty('--py', y + 'px');
      }
      row.addEventListener('pointermove', function (e) { place(e.clientX + 26, e.clientY + 18); p.classList.add('show'); });
      row.addEventListener('pointerleave', function () { p.classList.remove('show'); });
      row.addEventListener('focusin', function () { var b = row.getBoundingClientRect(); place(b.left - 320, b.top - 20); p.classList.add('show'); });
      row.addEventListener('focusout', function () { p.classList.remove('show'); });
    });
    window.addEventListener('scroll', function () { $$('.plate.show').forEach(function (p) { p.classList.remove('show'); }); }, { passive: true });
  }

  /* reveals */
  var rv = $$('.rv');
  if (reduce || !('IntersectionObserver' in window)) rv.forEach(function (r) { r.classList.add('in'); });
  else {
    var ro = new IntersectionObserver(function (en) { en.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); ro.unobserve(e.target); } }); }, { rootMargin: '0px 0px -10% 0px' });
    rv.forEach(function (r) { ro.observe(r); });
  }

  /* correspondence: the chosen subject decides which fields are shown. Nothing is sent. */
  var radios = $$('.rt input');
  if (radios.length) {
    var groups = $$('.cf-g');
    var sync = function () { var v = (radios.filter(function (r) { return r.checked; })[0] || radios[0]).value; groups.forEach(function (g) { g.hidden = g.getAttribute('data-for') !== v; }); };
    radios.forEach(function (r) { r.addEventListener('change', sync); });
    var want = new URLSearchParams(location.search).get('path');
    radios.forEach(function (r) { if (r.value === want) r.checked = true; });
    sync();
  }
  $$('.cf').forEach(function (f) {
    f.addEventListener('submit', function (e) { e.preventDefault(); });
    var b = $('.btn', f), n = $('.cf-note', f);
    if (b) b.addEventListener('click', function () { n.textContent = 'Concept form. Nothing was collected, stored, or sent.'; });
  });
})();
