/* Concept A: Venture Lab. Vanilla JS, no dependencies.
   Motion systems: (1) cursor-responsive dot field, (2) operating-status stack that cycles
   and pauses, (3) section-aware progression rail, (4) proximity spotlight on cards,
   (5) scroll depth on artifacts, (6) IntersectionObserver reveals.
   Everything is skipped or made static under prefers-reduced-motion. */
(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* nav */
  var tog = $('.hd-toggle'), nav = $('#nav');
  if (tog) {
    tog.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      tog.setAttribute('aria-expanded', open);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('open')) { nav.classList.remove('open'); tog.setAttribute('aria-expanded', 'false'); tog.focus(); }
    });
  }

  /* 1. dot field */
  $$('canvas.grid').forEach(function (cv) {
    var ctx = cv.getContext('2d'), host = cv.parentElement, W, H, dpr, gap = 30;
    var m = { x: -999, y: -999, tx: -999, ty: -999, on: false }, visible = true, raf = 0, t0 = performance.now();
    function size() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = host.clientWidth; H = host.clientHeight;
      cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      draw();
    }
    function draw() {
      ctx.clearRect(0, 0, W, H);
      var R = 210;
      for (var y = gap / 2; y < H; y += gap) {
        for (var x = gap / 2; x < W; x += gap) {
          var dx = x - m.x, dy = y - m.y, d = Math.sqrt(dx * dx + dy * dy), k = d < R ? 1 - d / R : 0;
          k = k * k;
          ctx.fillStyle = k > 0.02 ? 'rgba(' + Math.round(236 - 214 * k) + ',' + Math.round(231 - 32 * k) + ',' + Math.round(220 - 88 * k) + ',' + (0.17 + 0.7 * k) + ')' : 'rgba(236,231,220,0.17)';
          var r = 1 + 1.3 * k;
          ctx.fillRect(x - r / 2 - dx * k * 0.03, y - r / 2 - dy * k * 0.03, r, r);
        }
      }
    }
    function tick(now) {
      raf = 0;
      if (!visible) return;
      if (!m.on) { // ambient drift when no pointer is present
        var t = (now - t0) / 1000;
        m.tx = W * (0.62 + 0.26 * Math.sin(t * 0.21)); m.ty = H * (0.42 + 0.3 * Math.sin(t * 0.33 + 1));
      }
      m.x += (m.tx - m.x) * 0.09; m.y += (m.ty - m.y) * 0.09;
      draw();
      raf = requestAnimationFrame(tick);
    }
    function kick() { if (!raf && !reduce) raf = requestAnimationFrame(tick); }
    size();
    window.addEventListener('resize', size);
    if (reduce) return;
    if (fine) {
      host.addEventListener('pointermove', function (e) {
        var b = cv.getBoundingClientRect(); m.tx = e.clientX - b.left; m.ty = e.clientY - b.top; m.on = true; kick();
      });
      host.addEventListener('pointerleave', function () { m.on = false; });
    }
    new IntersectionObserver(function (en) { visible = en[0].isIntersecting; if (visible) kick(); }).observe(cv);
    m.x = m.tx = W * 0.7; m.y = m.ty = H * 0.4;
    kick();
  });

  /* 2. operating-status stack */
  var ops = $('.ops');
  if (ops) {
    var rows = $$('.ops-row', ops), btn = $('.ops-pause', ops), i = 0, timer = 0, user = false, hold = false;
    var show = function (n) { i = (n + rows.length) % rows.length; rows.forEach(function (r, k) { r.classList.toggle('is-on', k === i); }); };
    var run = function () { clearInterval(timer); if (!user && !hold && !reduce) timer = setInterval(function () { show(i + 1); }, 4200); };
    rows.forEach(function (r, k) {
      r.addEventListener('pointerenter', function () { show(k); });
      r.addEventListener('focusin', function () { show(k); });
    });
    ops.addEventListener('pointerenter', function () { hold = true; run(); });
    ops.addEventListener('pointerleave', function () { hold = false; run(); });
    ops.addEventListener('focusin', function () { hold = true; run(); });
    ops.addEventListener('focusout', function () { hold = false; run(); });
    btn.addEventListener('click', function () {
      user = !user; btn.setAttribute('aria-pressed', user); btn.textContent = user ? 'Play' : 'Pause'; run();
    });
    if (reduce) { btn.hidden = true; }
    document.addEventListener('visibilitychange', function () { hold = document.hidden; run(); });
    run();
  }

  /* 3. progression rail */
  var steps = $$('.step[data-step]');
  if (steps.length && 'IntersectionObserver' in window) {
    var marks = $$('.path-marks a'), dots = $$('.path-fig circle'), fig = $('.path-fig');
    var set = function (idx) {
      steps.forEach(function (s, k) { s.classList.toggle('is-on', k === idx); });
      marks.forEach(function (a, k) { a.classList.toggle('is-on', k === idx); if (k === idx) a.setAttribute('aria-current', 'step'); else a.removeAttribute('aria-current'); });
      dots.forEach(function (c, k) { c.classList.toggle('is-on', k <= idx); });
      if (fig) fig.style.setProperty('--p', idx / (steps.length - 1));
    };
    var io = new IntersectionObserver(function (en) {
      en.forEach(function (e) { if (e.isIntersecting) set(steps.indexOf(e.target)); });
    }, { rootMargin: '-45% 0px -45% 0px' });
    steps.forEach(function (s) { io.observe(s); });
    set(0);
  }

  /* 4. proximity spotlight: glow and border respond as the cursor approaches */
  if (fine && !reduce) {
    var spots = $$('[data-spot]'), px = 0, py = 0, pend = false;
    var upd = function () {
      pend = false;
      spots.forEach(function (el) {
        var b = el.getBoundingClientRect();
        if (b.bottom < -200 || b.top > window.innerHeight + 200) return;
        var dx = Math.max(b.left - px, 0, px - b.right), dy = Math.max(b.top - py, 0, py - b.bottom);
        var near = Math.max(0, 1 - Math.sqrt(dx * dx + dy * dy) / 160);
        el.style.setProperty('--near', near.toFixed(3));
        el.style.setProperty('--mx', (px - b.left) + 'px'); el.style.setProperty('--my', (py - b.top) + 'px');
      });
    };
    window.addEventListener('pointermove', function (e) { px = e.clientX; py = e.clientY; if (!pend) { pend = true; requestAnimationFrame(upd); } }, { passive: true });
  }

  /* 5. artifact depth on scroll (transform only, no layout) */
  var arts = $$('[data-depth]');
  if (arts.length && !reduce && window.innerWidth > 1080) {
    var sp = false;
    var par = function () {
      sp = false;
      var vh = window.innerHeight;
      arts.forEach(function (a) {
        var b = a.getBoundingClientRect();
        if (b.bottom < 0 || b.top > vh) return;
        a.style.setProperty('--dy', (((b.top + b.height / 2) - vh / 2) / vh * -26).toFixed(1));
      });
    };
    window.addEventListener('scroll', function () { if (!sp) { sp = true; requestAnimationFrame(par); } }, { passive: true });
    par();
  }

  /* 6. reveals */
  var rev = $$('.reveal');
  if (reduce || !('IntersectionObserver' in window)) rev.forEach(function (r) { r.classList.add('in'); });
  else {
    var ro = new IntersectionObserver(function (en) {
      en.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); ro.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    rev.forEach(function (r) { ro.observe(r); });
  }

  /* ventures filter */
  var fb = $$('.filter button');
  if (fb.length) {
    var cards = $$('.vc[data-status]'), out = $('.filter-n');
    fb.forEach(function (b) {
      b.addEventListener('click', function () {
        var f = b.getAttribute('data-filter'), n = 0;
        fb.forEach(function (o) { o.setAttribute('aria-pressed', o === b); });
        cards.forEach(function (c) { var ok = f === 'all' || c.getAttribute('data-status') === f; c.hidden = !ok; if (ok) { n++; c.classList.add('in'); } });
        out.textContent = n + ' of ' + cards.length + ' shown';
      });
    });
  }

  /* contact tabs (WAI-ARIA tabs pattern) and inert form */
  var tabs = $$('[role="tab"]');
  if (tabs.length) {
    var pick = function (t, focus) {
      tabs.forEach(function (o) {
        var on = o === t; o.setAttribute('aria-selected', on); o.tabIndex = on ? 0 : -1;
        document.getElementById(o.getAttribute('aria-controls')).hidden = !on;
      });
      if (focus) t.focus();
    };
    tabs.forEach(function (t, k) {
      t.addEventListener('click', function () { pick(t); });
      t.addEventListener('keydown', function (e) {
        var d = e.key === 'ArrowDown' || e.key === 'ArrowRight' ? 1 : e.key === 'ArrowUp' || e.key === 'ArrowLeft' ? -1 : 0;
        if (d) { e.preventDefault(); pick(tabs[(k + d + tabs.length) % tabs.length], true); }
      });
    });
    var want = new URLSearchParams(location.search).get('path'), pre = want && document.getElementById('t-' + want);
    if (pre) pick(pre);
  }
  $$('form').forEach(function (f) {
    f.addEventListener('submit', function (e) { e.preventDefault(); });
    var b = $('.btn', f), n = $('.cf-note', f);
    if (b) b.addEventListener('click', function () { n.textContent = 'Concept form. Nothing was collected, stored, or sent.'; });
  });
})();
