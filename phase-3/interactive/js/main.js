/* Version 3, Concept C: Original, Interactive. Vanilla JS and SVG, no libraries.
   Motion systems:
   (1) Presence map in the hero: signals start scattered, settle around one identity, then a slow tour
       lights one signal at a time. Pauses on hover, focus, and a hidden tab; stops once you choose anything.
       Problems and signals are selectable and name the service to start with.
   (2) How recognition is built: as each layer's text reaches the middle of the screen, the sticky map
       lights that layer's signals.
   (3) Example checks: each list steps through its items on its own, pausing on hover, focus, a hidden
       tab, or the Pause button. Plus a self-check that updates as boxes are ticked.
   Under reduced motion nothing cycles or moves; every state is still reachable. Without JavaScript,
   every signal, layer, and check is plain text. */
(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var NS = 'http://www.w3.org/2000/svg';
  var el = function (n, a) { var e = document.createElementNS(NS, n); for (var k in a) e.setAttribute(k, a[k]); return e; };
  var esc = function (s) { var d = document.createElement('div'); d.textContent = s; return d.innerHTML; };

  /* 1 and 2. presence map */
  $$('[data-map]').forEach(function (root) {
    var sticky = root.classList.contains('pmap-s');
    var data = JSON.parse($('.pm-data', root).textContent), view = $('.pm-view', root), card = sticky ? null : $('.pm-card'), segs = $$('.sg', root), probs = sticky ? [] : $$('.pb');
    var nodes = data.nodes, svg, W, H, portrait = null, state = 'recognized', sel = null, tourT = 0, tourI = 0, stopped = false, hold = false, touched = false;
    var LINKS = [['domain', 'website'], ['website', 'content'], ['content', 'search'], ['schema', 'profiles'], ['profiles', 'founders'], ['profiles', 'reviews'], ['citations', 'ai'], ['schema', 'ai'], ['search', 'ai']];
    var BROKEN = [['domain', 'profiles'], ['reviews', 'content'], ['citations', 'founders'], ['schema', 'website']];
    var PERM = [3, 7, 0, 9, 5, 1, 8, 2, 6, 4];
    function seed(i) { var x = Math.sin(i * 12.9898 + 4.1) * 43758.5453; return x - Math.floor(x); }
    function layout() {
      var p = view.clientWidth < 520;
      W = p ? 340 : 640; H = 440; var cx = W / 2, cy = H / 2, rx = p ? 118 : 238, ry = p ? 168 : 156;
      nodes.forEach(function (n, i) {
        var a = -Math.PI / 2 + i * 2 * Math.PI / nodes.length;
        n.w = Math.max(76, n.label.length * 8.8 + 32);
        var ca = Math.cos(a);
        /* on narrow screens, side signals sit against the edges so wide labels never touch */
        n.rx = p ? (ca > 0.2 ? W - n.w / 2 - 4 : ca < -0.2 ? n.w / 2 + 4 : cx) : cx + rx * ca;
        n.ry = cy + (p ? 188 : ry) * Math.sin(a) + (p && Math.abs(ca) < 0.2 && Math.sin(a) > 0 ? 8 : 0) - (p && Math.abs(ca) > 0.5 && Math.abs(ca) < 0.7 && Math.sin(a) > 0 ? 6 : 0);
      });
      /* fragmented: a shuffled, jittered grid that keeps every label legible and clear of the core.
         On narrow screens the middle row, beside the core, holds only the two shortest labels. */
      var slots = p ? [[76, 30], [264, 30], [76, 98], [264, 98], [76, 330], [264, 330], [76, 398], [264, 398]]
                    : [[95, 56], [245, 100], [395, 52], [545, 100], [95, 348], [245, 394], [395, 344], [545, 392]];
      var mids = ['domain', 'search'], q = 0;
      PERM.forEach(function (k) {
        var n = nodes[k], xy;
        if (mids.indexOf(n.id) > -1) xy = [mids.indexOf(n.id) ? W - n.w / 2 - (p ? 4 : 40) : n.w / 2 + (p ? 4 : 40), cy];
        else { xy = slots[q++].slice(); xy[0] += (seed(k + 1) - 0.5) * (p ? 14 : 20); xy[1] += (seed(k + 11) - 0.5) * (p ? 14 : 16); }
        n.fx = Math.min(Math.max(xy[0], n.w / 2 + 4), W - n.w / 2 - 4); n.fy = xy[1];
      });
      return { p: p, cx: cx, cy: cy };
    }
    function build() {
      var g = layout();
      if (svg) view.removeChild(svg);
      svg = el('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'group', 'aria-label': 'Presence map: ten signals connected to one brand identity. Select a signal for details.' });
      var ge = el('g', {}), gb = el('g', {}), gn = el('g', {});
      var byId = {}; nodes.forEach(function (n) { byId[n.id] = n; });
      nodes.forEach(function (n) { n.edge = el('line', { 'class': 'edge', x1: g.cx, y1: g.cy, x2: n.rx, y2: n.ry, 'data-n': n.id }); ge.appendChild(n.edge); });
      LINKS.forEach(function (l) { var a = byId[l[0]], b = byId[l[1]]; var e = el('line', { 'class': 'edge edge-x', x1: a.rx, y1: a.ry, x2: b.rx, y2: b.ry, 'data-a': l[0], 'data-b': l[1] }); ge.appendChild(e); });
      BROKEN.forEach(function (l) { var a = byId[l[0]], b = byId[l[1]]; var mx = (a.fx + b.fx) / 2, my = (a.fy + b.fy) / 2; gb.appendChild(el('line', { 'class': 'broken', x1: a.fx, y1: a.fy, x2: mx + (a.fx - mx) * 0.3, y2: my + (a.fy - my) * 0.3 })); });
      var core = el('g', { 'class': 'core', transform: 'translate(' + g.cx + ',' + g.cy + ')' });
      core.appendChild(el('circle', { r: 52, 'class': 'core-ring' }));
      core.appendChild(el('circle', { r: 40, fill: '#fff', stroke: '#0C2340', 'stroke-width': 2 }));
      /* The 128px PNG's visible pixels center at (58.4, 63.9), not (64, 64).
         Center the artwork, rather than its image box, in the 80-unit disc. */
      core.appendChild(el('image', { href: data.icon, x: -21.9, y: -24, width: 48, height: 48 }));
      nodes.forEach(function (n) {
        var gnode = el('g', { 'class': 'nd l-' + n.layer, tabindex: 0, role: 'button', 'aria-label': n.label + '. ' + n.line, 'aria-pressed': 'false' });
        gnode.appendChild(el('rect', { 'class': 'nd-b', x: -n.w / 2, y: -18, width: n.w, height: 36, rx: 18 }));
        gnode.appendChild(el('circle', { 'class': 'nd-d', cx: -n.w / 2 + 15, cy: 0, r: 5, fill: getComputedStyle(document.documentElement).getPropertyValue('--l-' + n.layer) || '#0C2340' }));
        var t = el('text', { x: 7, y: 5, 'text-anchor': 'middle' }); t.textContent = n.label; gnode.appendChild(t);
        gnode.addEventListener('click', function () { pick(n.id); });
        gnode.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); pick(n.id); } });
        n.g = gnode; gn.appendChild(gnode);
      });
      svg.appendChild(gb); svg.appendChild(ge); svg.appendChild(core); svg.appendChild(gn);
      view.appendChild(svg);
      place(true);
      paint();
    }
    function place(instant) {
      svg.setAttribute('class', state === 'recognized' ? 'rec' : 'frag');
      nodes.forEach(function (n) {
        var x = state === 'recognized' ? n.rx : n.fx, y = state === 'recognized' ? n.ry : n.fy;
        if (instant) { n.g.style.transition = 'none'; }
        n.g.style.transform = 'translate(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px)';
        if (instant) { void n.g.getBoundingClientRect(); n.g.style.transition = ''; }
      });
      segs.forEach(function (s) { s.setAttribute('aria-pressed', s.getAttribute('data-state') === state); });
    }
    function setState(s) { state = s; place(false); }
    function paint(hot) {
      hot = hot || (sel ? sel.ids : null);
      nodes.forEach(function (n) {
        var on = hot && hot.indexOf(n.id) > -1;
        n.g.classList.toggle('hot', !!on); n.g.classList.toggle('cold', !!hot && !on);
        n.g.setAttribute('aria-pressed', !!(sel && sel.kind === 'node' && sel.ids[0] === n.id));
        n.edge.classList.toggle('hot', !!on); n.edge.classList.toggle('cold', !!hot && !on);
      });
      $$('.edge-x', svg).forEach(function (e) { var on = hot && hot.indexOf(e.getAttribute('data-a')) > -1 && hot.indexOf(e.getAttribute('data-b')) > -1; e.classList.toggle('hot', !!on); e.classList.toggle('cold', !!hot && !on); });
    }
    function show(html) { if (!card) return; card.innerHTML = html; if (!reduce) { card.classList.remove('swap'); void card.offsetWidth; card.classList.add('swap'); } }
    function pick(id) {
      stopTour(); if (state !== 'recognized') setState('recognized');
      var n = nodes.filter(function (x) { return x.id === id; })[0];
      if (sel && sel.kind === 'node' && sel.ids[0] === id) { sel = null; paint(); return; }
      sel = { kind: 'node', ids: [id] }; probs.forEach(function (b) { b.setAttribute('aria-pressed', 'false'); });
      paint();
      show('<p class="pc-k">Signal</p><h2>' + esc(n.label) + '</h2><p>' + esc(n.line) + '</p><a class="lk" href="' + n.href + '">' + esc(n.svcName) + '</a>');
    }
    function problem(pid) {
      stopTour(); if (state !== 'recognized') setState('recognized');
      var d = data.diag[pid];
      sel = { kind: 'problem', ids: data.problems[pid] };
      probs.forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-problem') === pid); });
      paint();
      var names = nodes.filter(function (n) { return sel.ids.indexOf(n.id) > -1; }).map(function (n) { return n.label; }).join(', ');
      show('<p class="pc-k">Start here</p><h2>' + esc(d.start) + '</h2><p>' + esc(d.why) + '</p><p><b>Signals involved:</b> ' + esc(names) + '</p><a class="lk" href="' + d.href + '">See ' + esc(d.start) + '</a>');
    }
    probs.forEach(function (b) { b.addEventListener('click', function () { problem(b.getAttribute('data-problem')); }); });
    segs.forEach(function (s) { s.addEventListener('click', function () { touched = true; stopTour(); sel = null; paint(); setState(s.getAttribute('data-state')); }); });
    /* slow tour after recognition: one signal at a time */
    function tour() {
      clearInterval(tourT);
      if (stopped || hold || reduce || document.hidden || state !== 'recognized') return;
      tourT = setInterval(function () { paint([nodes[tourI % nodes.length].id]); tourI++; }, 2600);
    }
    function stopTour() { stopped = true; touched = true; clearInterval(tourT); }
    root.addEventListener('pointerenter', function () { hold = true; clearInterval(tourT); paint(); });
    root.addEventListener('pointerleave', function () { hold = false; tour(); });
    root.addEventListener('focusin', function () { hold = true; clearInterval(tourT); paint(); });
    root.addEventListener('focusout', function () { hold = false; tour(); });
    document.addEventListener('visibilitychange', tour);
    build();
    var lastP = view.clientWidth < 520;
    window.addEventListener('resize', function () { var p = view.clientWidth < 520; if (p !== lastP) { lastP = p; build(); } });
    if (reduce) { state = 'recognized'; place(true); }
    else {
      state = 'fragmented'; place(true);
      var go = function () { setTimeout(function () { if (!touched) { setState('recognized'); setTimeout(function () { if (!touched) { stopped = false; tour(); } }, 1400); } }, 700); };
      if ('IntersectionObserver' in window) { var o = new IntersectionObserver(function (en) { if (en[0].isIntersecting) { go(); o.disconnect(); } }); o.observe(view); } else go();
    }
    root.__paintLayer = function (lid) { stopTour(); if (state !== 'recognized') setState('recognized'); paint(nodes.filter(function (n) { return n.layer === lid; }).map(function (n) { return n.id; })); };
    if (sticky) { stopTour(); touched = true; state = 'recognized'; place(true); }
  });


  /* 2. layers light the sticky map */
  var m2 = $('.pmap-s'), lys = $$('[data-act]');
  if (m2 && lys.length && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (en) { en.forEach(function (e) { if (e.isIntersecting) { lys.forEach(function (l) { l.classList.toggle('on', l === e.target); }); if (m2.__paintLayer) m2.__paintLayer(e.target.getAttribute('data-act')); } }); }, { rootMargin: '-45% 0px -45% 0px' });
    lys.forEach(function (l) { io.observe(l); });
  }

  /* 3a. example checks */
  $$('[data-xchk]').forEach(function (x) {
    var items = $$('.xc-l li', x), btn = $('.xc-pause', x), i = -1, t = 0, user = false, hold = false, vis = true;
    var paint = function (n) { items.forEach(function (li, k) { li.classList.toggle('on', k === n); li.classList.toggle('done', k < n); }); };
    var run = function () { clearInterval(t); if (!user && !hold && !reduce && !document.hidden && vis && x.offsetParent) t = setInterval(function () { i = (i + 1) % (items.length + 1); paint(i === items.length ? items.length : i); }, 1500); };
    if (reduce) { btn.hidden = true; paint(items.length); return; }
    btn.addEventListener('click', function () { user = !user; btn.setAttribute('aria-pressed', user); btn.textContent = user ? 'Play' : 'Pause'; run(); });
    x.addEventListener('pointerenter', function () { hold = true; run(); }); x.addEventListener('pointerleave', function () { hold = false; run(); });
    x.addEventListener('focusin', function () { hold = true; run(); }); x.addEventListener('focusout', function () { hold = false; run(); });
    document.addEventListener('visibilitychange', run);
    if ('IntersectionObserver' in window) new IntersectionObserver(function (en) { vis = en[0].isIntersecting; run(); }).observe(x);
    x.__run = run; run();
  });

  /* 3b. service tabs on the homepage */
  var tabs = $$('[role="tab"]');
  if (tabs.length) {
    var pick = function (t, focus) {
      tabs.forEach(function (o) { var on = o === t; o.setAttribute('aria-selected', on); o.tabIndex = on ? 0 : -1; document.getElementById(o.getAttribute('aria-controls')).hidden = !on; });
      var p = document.getElementById(t.getAttribute('aria-controls')), xc = $('[data-xchk]', p); if (xc && xc.__run) xc.__run();
      if (focus) t.focus();
    };
    tabs.forEach(function (t, k) {
      t.addEventListener('click', function () { pick(t); });
      t.addEventListener('keydown', function (e) { var d = e.key === 'ArrowDown' || e.key === 'ArrowRight' ? 1 : e.key === 'ArrowUp' || e.key === 'ArrowLeft' ? -1 : 0; if (d) { e.preventDefault(); pick(tabs[(k + d + tabs.length) % tabs.length], true); } });
    });
    pick(tabs[0]);
  }

  /* 3c. presence self-check */
  var au = $('.au');
  if (au) {
    var boxes = $$('input[type=checkbox]', au), out = $('.au-out', au), cnt = $('[data-count]', au), recs = $$('.au-r', au), order = ['domain', 'website', 'search', 'entity', 'ai'];
    var upd = function () {
      var have = {}, tot = {};
      boxes.forEach(function (b) { var l = b.getAttribute('data-layer'); tot[l] = (tot[l] || 0) + 1; if (b.checked) have[l] = (have[l] || 0) + 1; });
      cnt.textContent = boxes.filter(function (b) { return b.checked; }).length;
      $$('[data-m]', au).forEach(function (m) { var l = m.getAttribute('data-m'); $('i', m).style.setProperty('--v', ((have[l] || 0) / (tot[l] || 1)).toFixed(2)); });
      var first = order.filter(function (l) { return (have[l] || 0) < (tot[l] || 0); })[0] || 'all';
      recs.forEach(function (r) { r.classList.toggle('on', r.getAttribute('data-for') === first); });
    };
    boxes.forEach(function (b) { b.addEventListener('change', upd); }); upd();
  }
})();
