/* Venture Lab v2. Vanilla JS, no dependencies.
   Motion is concentrated where it means something:
   (1) hero dot field, cursor-responsive, runs only while the hero is on screen;
   (2) operating-status stack, cycles every 5 s and pauses on hover, focus, hidden tab, or the Pause button;
   (3) featured venture: spotlight only while the pointer is inside it, and the order flow draws once;
   (4) progression line fills with scroll position (no sticking, no scroll-jacking);
   (5) short, one-time section reveals.
   Under prefers-reduced-motion everything is static and nothing cycles. */
(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var IO = 'IntersectionObserver' in window;

  /* navigation */
  var tog = $('.hd-toggle'), nav = $('#nav');
  if (tog) {
    tog.addEventListener('click', function () { var o = nav.classList.toggle('open'); tog.setAttribute('aria-expanded', o); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('open')) { nav.classList.remove('open'); tog.setAttribute('aria-expanded', 'false'); tog.focus(); }
    });
  }

  /* 1. hero dot field */
  var cv = $('.hero canvas.grid');
  if (cv) {
    var ctx = cv.getContext('2d'), host = cv.parentElement, W = 0, H = 0, gap = 30, raf = 0, vis = true, t0 = performance.now();
    var m = { x: 0, y: 0, tx: 0, ty: 0, on: false };
    var draw = function () {
      ctx.clearRect(0, 0, W, H);
      for (var y = gap / 2; y < H; y += gap) for (var x = gap / 2; x < W; x += gap) {
        var dx = x - m.x, dy = y - m.y, d = Math.sqrt(dx * dx + dy * dy), k = d < 210 ? 1 - d / 210 : 0; k *= k;
        ctx.fillStyle = k > 0.02 ? 'rgba(' + Math.round(236 - 214 * k) + ',' + Math.round(231 - 32 * k) + ',' + Math.round(220 - 88 * k) + ',' + (0.16 + 0.66 * k) + ')' : 'rgba(236,231,220,0.16)';
        var r = 1 + 1.2 * k; ctx.fillRect(x - r / 2, y - r / 2, r, r);
      }
    };
    var size = function () {
      var dpr = Math.min(window.devicePixelRatio || 1, 2); W = host.clientWidth; H = host.clientHeight;
      cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      if (!m.x) { m.x = m.tx = W * 0.72; m.y = m.ty = H * 0.4; }
      draw();
    };
    var tick = function (now) {
      raf = 0; if (!vis || document.hidden) return;
      if (!m.on) { var t = (now - t0) / 1000; m.tx = W * (0.66 + 0.22 * Math.sin(t * 0.2)); m.ty = H * (0.42 + 0.26 * Math.sin(t * 0.31 + 1)); }
      m.x += (m.tx - m.x) * 0.08; m.y += (m.ty - m.y) * 0.08; draw();
      raf = requestAnimationFrame(tick);
    };
    var kick = function () { if (!raf && !reduce) raf = requestAnimationFrame(tick); };
    size(); window.addEventListener('resize', size);
    if (!reduce) {
      if (fine) {
        host.addEventListener('pointermove', function (e) { var b = cv.getBoundingClientRect(); m.tx = e.clientX - b.left; m.ty = e.clientY - b.top; m.on = true; kick(); });
        host.addEventListener('pointerleave', function () { m.on = false; });
      }
      if (IO) new IntersectionObserver(function (en) { vis = en[0].isIntersecting; if (vis) kick(); }).observe(cv);
      document.addEventListener('visibilitychange', kick);
      kick();
    }
  }

  /* 2. operating-status stack */
  var ops = $('.ops');
  if (ops) {
    var rows = $$('.ops-row', ops), btn = $('.ops-pause', ops), i = 0, timer = 0, user = false, hold = false;
    var show = function (n) { i = (n + rows.length) % rows.length; rows.forEach(function (r, k) { r.classList.toggle('is-on', k === i); }); };
    var run = function () { clearInterval(timer); if (!user && !hold && !reduce && !document.hidden) timer = setInterval(function () { show(i + 1); }, 5000); };
    rows.forEach(function (r, k) {
      r.addEventListener('pointerenter', function () { show(k); });
      r.addEventListener('focusin', function () { show(k); });
    });
    ops.addEventListener('pointerenter', function () { hold = true; run(); });
    ops.addEventListener('pointerleave', function () { hold = false; run(); });
    ops.addEventListener('focusin', function () { hold = true; run(); });
    ops.addEventListener('focusout', function () { hold = false; run(); });
    btn.addEventListener('click', function () { user = !user; btn.setAttribute('aria-pressed', user); btn.textContent = user ? 'Play' : 'Pause'; run(); });
    if (reduce) btn.hidden = true;
    document.addEventListener('visibilitychange', run);
    run();
  }

  /* 3. featured venture: local spotlight and a one-time flow draw */
  var spot = $('[data-spot]');
  if (spot && fine && !reduce) {
    var pend = false, ex = 0, ey = 0;
    spot.addEventListener('pointermove', function (e) {
      ex = e.clientX; ey = e.clientY;
      if (!pend) { pend = true; requestAnimationFrame(function () { pend = false; var b = spot.getBoundingClientRect(); spot.style.setProperty('--mx', (ex - b.left) + 'px'); spot.style.setProperty('--my', (ey - b.top) + 'px'); }); }
    });
    spot.addEventListener('pointerenter', function () { spot.style.setProperty('--near', 1); });
    spot.addEventListener('pointerleave', function () { spot.style.setProperty('--near', 0); });
  }
  $$('[data-fx]').forEach(function (fx) {
    var st = $$('.fx-s', fx);
    var light = function (n) { st.forEach(function (s, k) { s.classList.toggle('lit', k <= n); }); fx.style.setProperty('--p', st.length > 1 ? n / (st.length - 1) : 1); };
    if (reduce || !IO) { light(st.length - 1); return; }
    var go = function () {
      fx.classList.add('run');
      st.forEach(function (s, k) { setTimeout(function () { light(k); }, 120 + k * 480); });
    };
    var o = new IntersectionObserver(function (en) { if (en[0].isIntersecting) { go(); o.disconnect(); } }, { rootMargin: '0px 0px -25% 0px' });
    o.observe(fx);
  });

  /* 4. progression line follows scroll position */
  var pg = $('[data-pgroot]');
  if (pg) {
    var wrap = $('.pg-wrap', pg), steps = $$('[data-pg]', pg), sp = false;
    var upd = function () {
      sp = false;
      var b = wrap.getBoundingClientRect(), vh = window.innerHeight;
      var p = reduce ? 1 : Math.max(0, Math.min(1, (vh * 0.85 - b.top) / (b.height + vh * 0.35)));
      wrap.style.setProperty('--p', p.toFixed(3));
      steps.forEach(function (s, k) { s.classList.toggle('lit', p >= k / steps.length + 0.05 || reduce); });
    };
    window.addEventListener('scroll', function () { if (!sp) { sp = true; requestAnimationFrame(upd); } }, { passive: true });
    window.addEventListener('resize', upd);
    upd();
  }

  /* 5. reveals */
  var rev = $$('.reveal');
  if (reduce || !IO) rev.forEach(function (r) { r.classList.add('in'); });
  else {
    var ro = new IntersectionObserver(function (en) { en.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); ro.unobserve(e.target); } }); }, { rootMargin: '0px 0px -6% 0px' });
    rev.forEach(function (r) { ro.observe(r); });
  }

  /* contact tabs (WAI-ARIA tabs pattern) and inert forms */
  var tabs = $$('[role="tab"]');
  if (tabs.length) {
    var pick = function (t, focus) {
      tabs.forEach(function (o) { var on = o === t; o.setAttribute('aria-selected', on); o.tabIndex = on ? 0 : -1; document.getElementById(o.getAttribute('aria-controls')).hidden = !on; });
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
