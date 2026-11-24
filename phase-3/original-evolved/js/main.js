/* Version 3, Concept A: Original, Evolved. Three motion systems, all optional:
   (1) Recognition map: pulses travel from the brand to people, search engines, and AI systems.
       Nodes lean gently toward the cursor. Pauses with the button, on a hidden tab, and under reduced motion.
   (2) Digital Presence Stack: the five layers light in order as the stack section scrolls through view.
   (3) Section-aware layer bar: as you read the Domain, Website, Search, Entity, and AI sections, the
       matching layer highlights and earlier layers stay marked. The diagnostic lives in v3.js. */
(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* 1. recognition map */
  var map = $('.rmap');
  if (map) {
    var box = $('.rm-box', map), btn = $('.rm-pause', map), nodes = $$('.rm-n', map), user = false;
    var sync = function () { box.classList.toggle('rm-paused', user || document.hidden); };
    if (reduce) { btn.hidden = true; box.classList.add('rm-paused'); }
    else {
      btn.addEventListener('click', function () { user = !user; btn.setAttribute('aria-pressed', user); btn.textContent = user ? 'Play' : 'Pause'; sync(); });
      document.addEventListener('visibilitychange', sync);
      if (fine) {
        var hero = map.closest('.hero'), pend = false, px = 0, py = 0;
        hero.addEventListener('pointermove', function (e) {
          px = e.clientX; py = e.clientY;
          if (pend) return; pend = true;
          requestAnimationFrame(function () {
            pend = false;
            nodes.forEach(function (n) {
              var b = n.getBoundingClientRect(), cx = b.left + b.width / 2, cy = b.top + b.height / 2;
              var dx = px - cx, dy = py - cy, d = Math.sqrt(dx * dx + dy * dy), k = Math.max(0, 1 - d / 260);
              n.style.setProperty('--dx', (dx * k * 0.08).toFixed(1) + 'px'); n.style.setProperty('--dy', (dy * k * 0.08).toFixed(1) + 'px');
              n.classList.toggle('near', k > 0.35);
            });
          });
        });
        hero.addEventListener('pointerleave', function () { nodes.forEach(function (n) { n.style.setProperty('--dx', '0px'); n.style.setProperty('--dy', '0px'); n.classList.remove('near'); }); });
      }
    }
  }

  /* 2. stack lights in order with scroll position */
  var stack = $('[data-stack]');
  if (stack) {
    var items = $$('.sk', stack), tick = false;
    var paint = function () {
      tick = false;
      var b = stack.getBoundingClientRect(), vh = window.innerHeight;
      var p = reduce ? 1 : Math.max(0, Math.min(1, (vh * 0.8 - b.top) / (vh * 0.55)));
      stack.style.setProperty('--p', p.toFixed(3));
      items.forEach(function (it, i) { it.classList.toggle('on', p >= (i + 0.5) / items.length || reduce); });
    };
    window.addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(paint); } }, { passive: true });
    paint();
  }

  /* 3. section-aware layer bar (homepage only) */
  var bar = $('.lbar'), secs = $$('main > section[data-layer]');
  if (bar && secs.length && $('a[href^="#"]', bar) && 'IntersectionObserver' in window) {
    var links = $$('a[data-l]', bar), order = links.map(function (a) { return a.getAttribute('data-l'); });
    var set = function (id) {
      var k = order.indexOf(id);
      links.forEach(function (a, i) { if (i === k) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current'); a.classList.toggle('done', k > -1 && i < k); });
    };
    var io = new IntersectionObserver(function (en) { en.forEach(function (e) { if (e.isIntersecting) set(e.target.getAttribute('data-layer')); }); }, { rootMargin: '-40% 0px -55% 0px' });
    secs.forEach(function (s) { io.observe(s); });
    var off = new IntersectionObserver(function (en) { en.forEach(function (e) { if (e.isIntersecting) set(null); }); }, { rootMargin: '-40% 0px -55% 0px' });
    ['stack', 'services', 'stuck', 'work'].forEach(function (id) { var s = document.getElementById(id); if (s) off.observe(s); });
  }
})();
