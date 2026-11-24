/* Phase 2 shared behavior: mobile menu, the Services disclosure menu, and inert concept forms.
   Concept-specific motion lives in each concept's js/main.js. */
(function () {
  'use strict';
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var tog = document.querySelector('.nav-toggle'), nav = document.getElementById('nav');
  function closeNav(focus) { if (!nav) return; nav.classList.remove('open'); if (tog) { tog.setAttribute('aria-expanded', 'false'); if (focus) tog.focus(); } }
  if (tog && nav) tog.addEventListener('click', function () { var o = nav.classList.toggle('open'); tog.setAttribute('aria-expanded', o); });
  $$('.menu-btn').forEach(function (b) {
    var m = document.getElementById(b.getAttribute('aria-controls'));
    b.addEventListener('click', function (e) { e.stopPropagation(); var o = b.getAttribute('aria-expanded') !== 'true'; b.setAttribute('aria-expanded', o); m.classList.toggle('open', o); });
    document.addEventListener('click', function (e) { if (!b.parentNode.contains(e.target)) { b.setAttribute('aria-expanded', 'false'); m.classList.remove('open'); } });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    var open = $$('.menu-btn[aria-expanded="true"]');
    if (open.length) { open.forEach(function (b) { b.setAttribute('aria-expanded', 'false'); document.getElementById(b.getAttribute('aria-controls')).classList.remove('open'); }); open[0].focus(); return; }
    if (nav && nav.classList.contains('open')) closeNav(true);
  });
  $$('#nav a').forEach(function (a) { a.addEventListener('click', function () { if (a.getAttribute('href').indexOf('#') > -1) closeNav(false); }); });
  $$('form[data-inert]').forEach(function (f) {
    f.addEventListener('submit', function (e) { e.preventDefault(); });
    var b = f.querySelector('button'), n = f.querySelector('.cf-note');
    if (b && n) b.addEventListener('click', function () { n.textContent = 'Design concept only. Nothing was collected, stored, or sent.'; });
  });
})();
