/* Version 3, Original Interactive, refined. Vanilla JS and SVG, no libraries, no network requests.
   Two homepage interactions and one supporting motion:
   (1) Presence map in the hero. Six signals start scattered, settle around one identity, and a
       single soft pulse travels from one signal to the centre at a time. The pulse pauses on hover,
       focus, a hidden tab, when the map is off screen, while a signal is selected, and with the
       Pause button. Signals are selectable by mouse, touch, and keyboard.
   (2) "What is holding you back?" (handled by the shared v3.js). The choice also lights the
       related signals on the map.
   (3) The five-layer progression draws its line once when it scrolls into view.
   Plus the Digital Presence Check, which totals answers in the browser and stores nothing.
   Under reduced motion nothing moves and every state is still reachable. Without JavaScript the
   signals, layers, answers, and questions are plain text. */
(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var NS = 'http://www.w3.org/2000/svg';
  var el = function (n, a) { var e = document.createElementNS(NS, n); for (var k in a) e.setAttribute(k, a[k]); return e; };
  var esc = function (s) { var d = document.createElement('div'); d.textContent = s; return d.innerHTML; };

  /* 1. presence map */
  var root = $('[data-map]');
  if (root) (function () {
    var data = JSON.parse($('.pm-data', root).textContent), view = $('.pm-view', root), detail = $('.pm-detail', root), segs = $$('.sg', root), pauseBtn = $('.pm-pause', root);
    var nodes = data.nodes, svg, pulseDot, W, H, G, state = 'recognized', sel = null, timer = 0, turn = 0, touched = false, userPaused = false, hold = false, visible = true, raf = 0;
    /* scattered positions [x, y, tilt] for wide and narrow layouts; each keeps clear of the centre */
    var FRAG = { wide: [[96, 58, -5], [452, 46, 4], [492, 192, -3], [410, 314, 5], [136, 306, -4], [84, 186, 3]],
                 narrow: [[70, 34, -5], [262, 78, 4], [286, 190, -3], [236, 338, 5], [84, 300, -4], [66, 112, 3]] };
    var BROKEN = [[0, 3], [1, 4], [2, 5]];
    function layout() {
      var p = view.clientWidth < 480;
      W = p ? 340 : 560; H = p ? 380 : 360;
      var cx = W / 2, cy = H / 2, rx = p ? 0 : 196, ry = p ? 160 : 132, f = FRAG[p ? 'narrow' : 'wide'];
      nodes.forEach(function (n, i) {
        var a = -Math.PI / 2 + i * 2 * Math.PI / nodes.length, ca = Math.cos(a), sa = Math.sin(a);
        n.w = Math.max(84, n.label.length * 9.2 + 34);
        /* narrow screens: side signals sit against the edges, above and below the centre */
        n.rx = p ? (ca > 0.2 ? W - n.w / 2 - 6 : ca < -0.2 ? n.w / 2 + 6 : cx) : cx + rx * ca;
        n.ry = p ? cy + (Math.abs(ca) < 0.2 ? ry * sa : 92 * (sa > 0 ? 1 : -1)) : cy + ry * sa;
        n.fx = Math.min(Math.max(f[i][0], n.w / 2 + 6), W - n.w / 2 - 6); n.fy = f[i][1]; n.fr = f[i][2];
      });
      G = { p: p, cx: cx, cy: cy };
    }
    function build() {
      layout();
      if (svg) view.removeChild(svg);
      svg = el('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'group', 'aria-label': 'Presence map: six signals connected to one brand identity. Select a signal for details.' });
      var ge = el('g', {}), gb = el('g', {}), gn = el('g', {});
      nodes.forEach(function (n, i) {
        n.edge = el('line', { 'class': 'edge', x1: G.cx, y1: G.cy, x2: n.rx, y2: n.ry }); ge.appendChild(n.edge);
        var m = nodes[(i + 1) % nodes.length];
        ge.appendChild(el('line', { 'class': 'edge edge-x', x1: n.rx, y1: n.ry, x2: m.rx, y2: m.ry }));
      });
      BROKEN.forEach(function (l) { var a = nodes[l[0]], b = nodes[l[1]], mx = (a.fx + b.fx) / 2, my = (a.fy + b.fy) / 2; gb.appendChild(el('line', { 'class': 'broken', x1: a.fx, y1: a.fy, x2: mx + (a.fx - mx) * 0.45, y2: my + (a.fy - my) * 0.45 })); });
      var core = el('g', { 'class': 'core', transform: 'translate(' + G.cx + ',' + G.cy + ')' });
      core.appendChild(el('circle', { r: 52, 'class': 'core-ring' }));
      core.appendChild(el('circle', { r: 40, fill: '#fff', stroke: '#0C2340', 'stroke-width': 2 }));
      /* the visible pixels of the 128px icon centre at (58.4, 63.9), so the artwork is centred, not its box */
      core.appendChild(el('image', { href: data.icon, x: -21.9, y: -24, width: 48, height: 48 }));
      pulseDot = el('circle', { r: 4.5, 'class': 'pulse' });
      nodes.forEach(function (n) {
        var g = el('g', { 'class': 'nd', tabindex: 0, role: 'button', 'aria-label': n.label + '. ' + n.line, 'aria-pressed': 'false' });
        g.appendChild(el('rect', { 'class': 'nd-b', x: -n.w / 2, y: -19, width: n.w, height: 38, rx: 19 }));
        g.appendChild(el('circle', { 'class': 'nd-d', cx: -n.w / 2 + 16, cy: 0, r: 4.5 }));
        var t = el('text', { x: 8, y: 5, 'text-anchor': 'middle' }); t.textContent = n.label; g.appendChild(t);
        g.addEventListener('click', function () { pick(n.id); });
        g.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); pick(n.id); } });
        n.g = g; gn.appendChild(g);
      });
      svg.appendChild(gb); svg.appendChild(ge); svg.appendChild(pulseDot); svg.appendChild(core); svg.appendChild(gn);
      view.appendChild(svg);
      place(true); paint();
    }
    function place(instant, lean) {
      svg.setAttribute('class', (state === 'recognized' ? 'rec' : 'frag') + (lean ? ' lean' : ''));
      nodes.forEach(function (n) {
        var rec = state === 'recognized', x = (rec ? n.rx : n.fx) + (lean ? n.lx || 0 : 0), y = (rec ? n.ry : n.fy) + (lean ? n.ly || 0 : 0);
        if (instant) n.g.style.transition = 'none';
        n.g.style.transform = 'translate(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px)' + (rec ? '' : ' rotate(' + n.fr + 'deg)');
        if (instant) { void n.g.getBoundingClientRect(); n.g.style.transition = ''; }
      });
      segs.forEach(function (s) { s.setAttribute('aria-pressed', s.getAttribute('data-state') === state); });
    }
    function paint() {
      var hot = sel ? sel.ids : null;
      nodes.forEach(function (n) {
        var on = hot && hot.indexOf(n.id) > -1;
        n.g.classList.toggle('hot', !!on); n.g.classList.toggle('cold', !!hot && !on);
        n.g.setAttribute('aria-pressed', !!(sel && sel.kind === 'node' && on));
        n.edge.classList.toggle('hot', !!on); n.edge.classList.toggle('cold', !!hot && !on);
      });
    }
    function show(html) { detail.innerHTML = html; if (!reduce) { detail.classList.remove('swap'); void detail.offsetWidth; detail.classList.add('swap'); } }
    function idle() { show('<p>' + esc(state === 'recognized' ? data.idle : data.fragmented) + '</p>'); }
    function setState(s) { state = s; place(false); if (!sel) idle(); run(); }
    function byId(id) { return nodes.filter(function (n) { return n.id === id; })[0]; }
    function pick(id) {
      touched = true;
      if (sel && sel.kind === 'node' && sel.ids[0] === id) { sel = null; paint(); idle(); run(); return; }
      if (state !== 'recognized') { state = 'recognized'; place(false); }
      var n = byId(id);
      sel = { kind: 'node', ids: [id] }; paint(); run();
      show('<p class="pd-h">' + esc(n.label) + '</p><p>' + esc(n.line) + '</p><ul class="pd-chips" aria-label="Includes">' + n.details.map(function (d) { return '<li>' + esc(d) + '</li>'; }).join('') +
           '</ul><a class="pd-link" href="' + n.href + '">' + esc(n.svcName) + '</a>');
    }
    function problem(pid) {
      var ids = data.problems[pid]; if (!ids) return;
      touched = true;
      if (state !== 'recognized') { state = 'recognized'; place(false); }
      sel = { kind: 'problem', ids: ids }; paint(); run();
      show('<p class="pd-h">' + esc(data.labels[pid]) + '</p><p>Signals involved: ' + esc(ids.map(function (i) { return byId(i).label; }).join(', ')) + '. Select any one for details.</p>');
    }
    /* one soft pulse at a time, from a signal to the centre */
    function pulse() {
      var n = nodes[turn % nodes.length]; turn++;
      if (!pulseDot.animate) return;
      n.edge.classList.add('hot'); setTimeout(function () { if (!sel) n.edge.classList.remove('hot'); }, 1500);
      pulseDot.animate([{ transform: 'translate(' + n.rx + 'px,' + n.ry + 'px)', opacity: 0 }, { opacity: 1, offset: 0.2 }, { opacity: 1, offset: 0.75 },
                        { transform: 'translate(' + G.cx + 'px,' + G.cy + 'px)', opacity: 0 }], { duration: 1500, easing: 'ease-in-out' });
    }
    function run() {
      clearInterval(timer);
      if (reduce || userPaused || hold || !visible || document.hidden || state !== 'recognized' || sel) return;
      timer = setInterval(pulse, 2800);
    }
    segs.forEach(function (s) { s.addEventListener('click', function () { touched = true; sel = null; paint(); setState(s.getAttribute('data-state')); }); });
    pauseBtn.addEventListener('click', function () {
      userPaused = !userPaused; pauseBtn.setAttribute('aria-pressed', userPaused);
      pauseBtn.setAttribute('aria-label', userPaused ? 'Play map animation' : 'Pause map animation'); run();
    });
    root.addEventListener('pointerenter', function () { hold = true; run(); });
    root.addEventListener('pointerleave', function () { hold = false; run(); });
    root.addEventListener('focusin', function () { hold = true; run(); });
    root.addEventListener('focusout', function () { hold = false; run(); });
    document.addEventListener('visibilitychange', run);
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && sel && root.contains(document.activeElement)) { sel = null; paint(); idle(); } });
    /* signals lean a few pixels toward a mouse pointer; the edges end under each label, so they stay attached */
    if (fine && !reduce) {
      view.addEventListener('pointermove', function (e) {
        if (raf) return;
        raf = requestAnimationFrame(function () {
          raf = 0; var r = view.getBoundingClientRect(), px = (e.clientX - r.left) / r.width * W, py = (e.clientY - r.top) / r.height * H;
          nodes.forEach(function (n) { var x = state === 'recognized' ? n.rx : n.fx, y = state === 'recognized' ? n.ry : n.fy; n.lx = Math.max(-5, Math.min(5, (px - x) / 40)); n.ly = Math.max(-5, Math.min(5, (py - y) / 40)); });
          place(false, true);
        });
      });
      view.addEventListener('pointerleave', function () { nodes.forEach(function (n) { n.lx = n.ly = 0; }); place(false, true); });
    }
    build();
    var lastP = G.p;
    window.addEventListener('resize', function () { var p = view.clientWidth < 480; if (p !== lastP) { lastP = p; build(); } });
    if ('IntersectionObserver' in window) new IntersectionObserver(function (en) { visible = en[0].isIntersecting; run(); }, { threshold: 0.25 }).observe(view);
    if (reduce) { state = 'recognized'; place(true); }
    else {
      state = 'fragmented'; place(true); idle();
      setTimeout(function () { if (!touched) setState('recognized'); }, 900);
    }
    document.addEventListener('v3:diagnostic', function (e) { problem(e.detail); });
  })();

  /* 3. five-layer progression: draw the line once */
  var prog = $('[data-prog]');
  if (prog) {
    if (reduce || !('IntersectionObserver' in window)) prog.classList.add('on');
    else { var po = new IntersectionObserver(function (en) { if (en[0].isIntersecting) { prog.classList.add('on'); po.disconnect(); } }, { threshold: 0.2 }); po.observe(prog); }
  }

  /* Digital Presence Check: totals answers in the page. Nothing is stored or sent. */
  var dpc = $('[data-dpc]');
  if (dpc) (function () {
    var cfg = JSON.parse($('.dpc-data').textContent), qs = $$('.dq', dpc), rows = $$('.dpc-areas li', dpc), sum = $('[data-sum]', dpc), next = $('[data-next]', dpc), nextT = $('[data-next-t]', dpc);
    function update() {
      var by = {}, answered = 0;
      qs.forEach(function (q) { var a = q.getAttribute('data-area'), c = $('input:checked', q); (by[a] = by[a] || []).push(c ? c.value : null); if (c) answered++; });
      var look = 0, checkN = 0, first = null;
      rows.forEach(function (li) {
        var v = by[li.getAttribute('data-area')] || [], st = 'none';
        if (v.indexOf('no') > -1) st = 'no'; else if (v.indexOf('unsure') > -1) st = 'unsure';
        else if (v.length && v.every(function (x) { return x === 'yes'; })) st = 'yes'; else if (v.indexOf('yes') > -1) st = 'partial';
        li.setAttribute('data-state', st === 'partial' ? 'yes' : st); $('[data-status]', li).textContent = cfg.status[st];
        if (st === 'no') look++; if (st === 'unsure') checkN++;
        if (!first && (st === 'no' || st === 'unsure')) first = li;
      });
      var t = answered + ' of ' + cfg.total + ' answered.';
      if (!answered) t = 'Answer the questions to see possible areas to investigate.';
      else if (look || checkN) t += ' ' + (look ? look + (look === 1 ? ' area is' : ' areas are') + ' worth a closer look' : '') + (look && checkN ? ', and ' : '') + (checkN ? checkN + (checkN === 1 ? ' area is' : ' areas are') + ' worth checking' : '') + '.';
      else if (answered === cfg.total) t += ' ' + cfg.allYes;
      else t += ' Nothing flagged so far.';
      sum.textContent = t;
      next.hidden = !first;
      if (first) nextT.textContent = $('.da-b a', first).textContent.trim();
    }
    dpc.addEventListener('change', update);
    $('[data-reset]', dpc).addEventListener('click', function () { $$('input:checked', dpc).forEach(function (i) { i.checked = false; }); update(); var f = $('input', dpc); if (f) f.focus(); });
    update();
  })();
})();
