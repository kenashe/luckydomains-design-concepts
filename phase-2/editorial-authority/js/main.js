/* Phase 2, Concept B: Editorial Authority. Vanilla JS.
   Motion systems:
   (1) Reading progress and a section-aware contents rail: a hairline in the masthead fills as you read,
       and the rail marks the chapter in view. Becomes a horizontal chapter strip on small screens.
   (2) Eras of discovery: the timeline rule fills with scroll position, and each era is marked as the
       rule reaches it. No sticking, no scroll-jacking.
   (3) Before and after: the information-architecture view switches between two page maps, and the
       pages settle into the new order. Plus annotations that highlight on hover, focus, or tap.
   Under reduced motion nothing animates; every state is still reachable. */
(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var IO = 'IntersectionObserver' in window;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var clamp = function (v) { return v < 0 ? 0 : v > 1 ? 1 : v; };

  /* 1. progress and rail */
  var mh = $('.mh'), eras = $('[data-eras]'), eraItems = $$('[data-era]'), tick = false;
  function frame() {
    tick = false;
    var vh = window.innerHeight, max = document.documentElement.scrollHeight - vh;
    if (mh) mh.style.setProperty('--read', max > 0 ? clamp(window.scrollY / max).toFixed(4) : 0);
    if (eras) {
      var b = eras.getBoundingClientRect();
      var p = reduce ? 1 : clamp((vh * 0.62 - b.top) / b.height);
      eras.style.setProperty('--p', p.toFixed(4));
      eraItems.forEach(function (li) { li.classList.toggle('lit', reduce || li.offsetTop + 30 <= p * eras.offsetHeight); });
    }
  }
  window.addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(frame); } }, { passive: true });
  window.addEventListener('resize', frame);
  frame();
  var links = $$('[data-toc]');
  if (links.length && IO) {
    var setOn = function (id) {
      links.forEach(function (a) {
        var on = a.getAttribute('data-toc') === id; a.classList.toggle('on', on);
        if (on) { a.setAttribute('aria-current', 'location'); if (a.parentNode.parentNode.scrollWidth > a.parentNode.parentNode.clientWidth) a.scrollIntoView({ block: 'nearest', inline: 'nearest' }); }
        else a.removeAttribute('aria-current');
      });
    };
    var so = new IntersectionObserver(function (en) { en.forEach(function (e) { if (e.isIntersecting) setOn(e.target.id); }); }, { rootMargin: '-30% 0px -60% 0px' });
    links.forEach(function (a) { var s = document.getElementById(a.getAttribute('data-toc')); if (s) so.observe(s); });
  }

  /* 3a. before and after */
  $$('[data-ba]').forEach(function (ba) {
    var btns = $$('.ba-b', ba), cols = $$('.ba-c', ba);
    var show = function (k) {
      btns.forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-show') === k); });
      cols.forEach(function (c) { c.classList.toggle('on', c.getAttribute('data-state') === k); });
    };
    btns.forEach(function (b) { b.addEventListener('click', function () { show(b.getAttribute('data-show')); }); });
    show('after');
  });

  /* 3b. annotations: marker and note highlight each other */
  $$('.mk').forEach(function (m) {
    var n = document.querySelector('[data-note="' + m.getAttribute('data-mk') + '"]');
    var on = function (v) { m.classList.toggle('on', v); if (n) n.classList.toggle('on', v); };
    m.addEventListener('pointerenter', function () { on(true); });
    m.addEventListener('pointerleave', function () { if (document.activeElement !== m) on(false); });
    m.addEventListener('focus', function () { on(true); });
    m.addEventListener('blur', function () { on(false); });
    m.addEventListener('click', function () { on(true); if (n && window.innerWidth < 1080) n.scrollIntoView({ block: 'nearest', behavior: reduce ? 'auto' : 'smooth' }); });
  });
})();
