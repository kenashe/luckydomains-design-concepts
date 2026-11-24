/* Version 3 shared behavior, based on the original site's main.js: sticky header shadow, mobile
   menu, FAQ accordion, and reveal on scroll. Adds the Services menu, the diagnostic, the
   before-and-after page map, and inert concept forms. Concept motion lives in each js/main.js. */
(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var header = document.getElementById('site-header');
  function onScroll() { if (header) header.classList.toggle('scrolled', window.scrollY > 8); }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
  var toggle = document.getElementById('nav-toggle');
  function setNav(open, focus) {
    header.classList.toggle('nav-open', open); toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu'); if (focus) toggle.focus();
  }
  if (toggle && header) {
    toggle.addEventListener('click', function () { setNav(!header.classList.contains('nav-open')); });
    $$('#nav a').forEach(function (a) { a.addEventListener('click', function () { setNav(false); }); });
  }
  $$('.menu-btn').forEach(function (b) {
    var m = document.getElementById(b.getAttribute('aria-controls'));
    b.addEventListener('click', function (e) { e.stopPropagation(); var o = b.getAttribute('aria-expanded') !== 'true'; b.setAttribute('aria-expanded', o); m.classList.toggle('open', o); });
    document.addEventListener('click', function (e) { if (!b.parentNode.contains(e.target)) { b.setAttribute('aria-expanded', 'false'); m.classList.remove('open'); } });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    var open = $$('.menu-btn[aria-expanded="true"]');
    if (open.length) { open.forEach(function (b) { b.setAttribute('aria-expanded', 'false'); document.getElementById(b.getAttribute('aria-controls')).classList.remove('open'); }); open[0].focus(); return; }
    if (header && header.classList.contains('nav-open')) setNav(false, true);
  });
  $$('.faq-q').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var ex = btn.getAttribute('aria-expanded') === 'true', panel = btn.nextElementSibling;
      btn.setAttribute('aria-expanded', ex ? 'false' : 'true'); if (panel) panel.style.maxHeight = ex ? null : panel.scrollHeight + 'px';
    });
  });
  /* without JavaScript the FAQ answers stay open: the original CSS hides them, so open them here only when JS runs */
  var rv = $$('.reveal');
  if (reduce || !('IntersectionObserver' in window)) rv.forEach(function (r) { r.classList.add('in'); });
  else {
    var io = new IntersectionObserver(function (en) { en.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add('in'); io.unobserve(x.target); } }); }, { rootMargin: '0px 0px -8% 0px' });
    rv.forEach(function (r) { io.observe(r); });
  }
  var out = $('.dg-out');
  if (out) {
    var empty = $('.dg-empty', out), ans = $$('.dg-a', out);
    $$('input[name="stuck"]').forEach(function (r) { r.addEventListener('change', function () { empty.hidden = true; ans.forEach(function (a) { a.classList.toggle('on', a.getAttribute('data-for') === r.value); }); document.dispatchEvent(new CustomEvent('v3:diagnostic', { detail: r.value })); }); });
  }
  $$('[data-ba]').forEach(function (ba) {
    var btns = $$('.ba-b', ba), cols = $$('.arch-c', ba);
    var show = function (k) { btns.forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-show') === k); }); cols.forEach(function (c) { c.classList.toggle('on', c.getAttribute('data-state') === k); }); };
    btns.forEach(function (b) { b.addEventListener('click', function () { show(b.getAttribute('data-show')); }); }); show('after');
  });
  $$('form[data-inert]').forEach(function (f) {
    f.addEventListener('submit', function (e) { e.preventDefault(); });
    var b = f.querySelector('button'), n = f.querySelector('.cf-note');
    if (b && n) b.addEventListener('click', function () { n.textContent = 'Design concept only. Nothing was collected, stored, or sent.'; });
  });
})();
