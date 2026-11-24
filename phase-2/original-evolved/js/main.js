/* Phase 2, Concept A: Original, Evolved. Vanilla JS.
   Motion systems:
   (1) Hero presence card: the five layers light in order, hold, then repeat. Pauses on hover,
       focus, a hidden tab, or the Pause button. Static and fully lit under reduced motion.
   (2) Digital Presence Stack: as each step scrolls into the reading line, its slab settles into
       place in the stack beside it. No scroll-jacking; the list reads normally without it.
   (3) Diagnostic: choosing a problem reveals the recommended starting point (aria-live).
   Plus one gentle rise per section, skipped under reduced motion. */
(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var IO = 'IntersectionObserver' in window;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* 1. presence card */
  var card = $('.pcard');
  if (card) {
    var rows = $$('.pc-list li', card), btn = $('.pc-pause', card), i = -1, t = 0, user = false, hold = false;
    var paint = function (n) { rows.forEach(function (r, k) { r.classList.toggle('on', k <= n); }); };
    var tick = function () {
      i = i + 1; if (i > rows.length + 2) i = -1;         /* hold the full stack for three beats */
      paint(Math.min(i, rows.length - 1));
    };
    var run = function () { clearInterval(t); if (!user && !hold && !reduce && !document.hidden) t = setInterval(tick, 1100); };
    if (reduce) { paint(rows.length - 1); btn.hidden = true; }
    else {
      card.addEventListener('pointerenter', function () { hold = true; run(); });
      card.addEventListener('pointerleave', function () { hold = false; run(); });
      card.addEventListener('focusin', function () { hold = true; run(); });
      card.addEventListener('focusout', function () { hold = false; run(); });
      btn.addEventListener('click', function () { user = !user; btn.setAttribute('aria-pressed', user); btn.textContent = user ? 'Play' : 'Pause'; if (user) paint(rows.length - 1); run(); });
      document.addEventListener('visibilitychange', run);
      paint(-1); run();
    }
  }

  /* 2. stack */
  var steps = $$('.st[data-layer]'), slabs = $$('.slab[data-layer]');
  if (steps.length) {
    var order = steps.map(function (s) { return s.getAttribute('data-layer'); });
    var set = function (idx) {
      slabs.forEach(function (sl) { var k = order.indexOf(sl.getAttribute('data-layer')); sl.classList.toggle('on', k <= idx); sl.classList.toggle('now', k === idx); });
    };
    if (reduce || !IO) set(order.length - 1);
    else {
      var io = new IntersectionObserver(function (en) { en.forEach(function (e) { if (e.isIntersecting) set(steps.indexOf(e.target)); }); }, { rootMargin: '-45% 0px -45% 0px' });
      steps.forEach(function (s) { io.observe(s); });
      set(-1);
    }
  }

  /* 3. diagnostic */
  var out = $('.dg-out');
  if (out) {
    var empty = $('.dg-empty', out), ans = $$('.dg-a', out);
    $$('input[name="stuck"]').forEach(function (r) {
      r.addEventListener('change', function () {
        empty.hidden = true;
        ans.forEach(function (a) { a.classList.toggle('on', a.getAttribute('data-for') === r.value); });
      });
    });
  }

  /* gentle section rise */
  var rise = $$('main > section > .wrap > .sec-hd, .out, .tri, .wk-feat, .proc li, .engs li');
  if (!reduce && IO) {
    var ro = new IntersectionObserver(function (en) { en.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); ro.unobserve(e.target); } }); }, { rootMargin: '0px 0px -8% 0px' });
    rise.forEach(function (r) { r.classList.add('rise'); ro.observe(r); });
  }
})();
