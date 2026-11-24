/* Version 3, Concept B: Original, Editorial. Three motion systems:
   (1) Reading progress and a section-aware contents rail on every inner page.
   (2) The evolution timeline: each layer's word comes into full weight as it reaches the middle of the
       screen (scroll-linked, no scroll-jacking).
   (3) Before and after: the identity example alternates on its own and stops for good once the visitor
       chooses a state; it pauses on hover, focus, and a hidden tab. Case-study notes highlight on hover,
       focus, or tap. Under reduced motion nothing moves and everything is shown at full strength. */
(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var clamp = function (v) { return v < 0 ? 0 : v > 1 ? 1 : v; };
  var bar = document.createElement('i'); bar.className = 'progress'; bar.setAttribute('aria-hidden', 'true'); document.body.appendChild(bar);
  var words = $$('.era-w'), tick = false;
  function frame() {
    tick = false;
    var vh = window.innerHeight, max = document.documentElement.scrollHeight - vh;
    bar.style.setProperty('--read', max > 0 ? clamp(window.scrollY / max).toFixed(4) : 0);
    if (!reduce) words.forEach(function (w) {
      var r = w.getBoundingClientRect(); if (r.bottom < -40 || r.top > vh + 40) return;
      var mid = r.top + r.height / 2, k = clamp(1 - Math.abs(mid - vh * 0.5) / (vh * 0.42));
      w.style.setProperty('--k', k.toFixed(3));
    });
  }
  window.addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(frame); } }, { passive: true });
  window.addEventListener('resize', frame); frame();

  var links = $$('[data-toc]').filter(function (a) { return a.tagName === 'A'; });
  if (links.length && 'IntersectionObserver' in window) {
    var setOn = function (id) {
      links.forEach(function (a) {
        var on = a.getAttribute('data-toc') === id; a.classList.toggle('on', on);
        if (on) { a.setAttribute('aria-current', 'location'); var ol = a.closest('ol'); if (ol && ol.parentNode.scrollWidth > ol.parentNode.clientWidth) a.scrollIntoView({ block: 'nearest', inline: 'nearest' }); }
        else a.removeAttribute('aria-current');
      });
    };
    var so = new IntersectionObserver(function (en) { en.forEach(function (e) { if (e.isIntersecting) setOn(e.target.id); }); }, { rootMargin: '-30% 0px -60% 0px' });
    links.forEach(function (a) { var s = document.getElementById(a.getAttribute('data-toc')); if (s) so.observe(s); });
  }

  $$('[data-bv]').forEach(function (bv) {
    var btns = $$('.bv-b', bv), cols = $$('.bv-c', bv), state = 'before', t = 0, stopped = false, hold = false;
    var show = function (k) { state = k; btns.forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-show') === k); }); cols.forEach(function (c) { c.classList.toggle('on', c.getAttribute('data-state') === k); }); };
    var run = function () { clearInterval(t); if (!stopped && !hold && !reduce && !document.hidden) t = setInterval(function () { show(state === 'before' ? 'after' : 'before'); }, 4500); };
    btns.forEach(function (b) { b.addEventListener('click', function () { stopped = true; clearInterval(t); show(b.getAttribute('data-show')); }); });
    bv.addEventListener('pointerenter', function () { hold = true; run(); }); bv.addEventListener('pointerleave', function () { hold = false; run(); });
    bv.addEventListener('focusin', function () { hold = true; run(); }); bv.addEventListener('focusout', function () { hold = false; run(); });
    document.addEventListener('visibilitychange', run);
    show(reduce ? 'after' : 'before'); run();
  });

  $$('.mk').forEach(function (m) {
    var n = document.querySelector('[data-note="' + m.getAttribute('data-mk') + '"]');
    var on = function (v) { m.classList.toggle('on', v); if (n) n.classList.toggle('on', v); };
    m.addEventListener('pointerenter', function () { on(true); }); m.addEventListener('pointerleave', function () { if (document.activeElement !== m) on(false); });
    m.addEventListener('focus', function () { on(true); }); m.addEventListener('blur', function () { on(false); });
    m.addEventListener('click', function () { on(true); if (n && window.innerWidth < 980) n.scrollIntoView({ block: 'nearest', behavior: reduce ? 'auto' : 'smooth' }); });
  });
})();
