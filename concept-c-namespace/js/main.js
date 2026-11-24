/* Concept C: Namespace. Vanilla JS and SVG, no dependencies, no WebGL.
   Motion systems: (1) a drifting, cursor-aware constellation map with selectable
   relationships, (2) an address bar that tracks the section in view,
   (3) FLIP card rearrangement when filtering, (4) a layer stack that opens on scroll
   and responds to hover and focus, (5) marching route lines and rise-in tiles.
   Everything is static under prefers-reduced-motion and the map has a list equivalent. */
(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var NS = 'http://www.w3.org/2000/svg';
  var el = function (n, a) { var e = document.createElementNS(NS, n); for (var k in a) e.setAttribute(k, a[k]); return e; };
  var esc = function (s) { var d = document.createElement('div'); d.textContent = s; return d.innerHTML; };

  /* address bar: directory menu + section-aware fragment */
  var ab = $('.ab'), dir = $('#dir'), hash = $('[data-hash]');
  function setDir(open) { dir.hidden = !open; ab.setAttribute('aria-expanded', open); }
  ab.addEventListener('click', function () { setDir(dir.hidden); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !dir.hidden) { setDir(false); ab.focus(); } });
  document.addEventListener('click', function (e) { if (!dir.hidden && !dir.contains(e.target) && !ab.contains(e.target)) setDir(false); });
  if ('IntersectionObserver' in window) {
    var ao = new IntersectionObserver(function (en) {
      en.forEach(function (e) { if (e.isIntersecting) { var a = e.target.getAttribute('data-addr'); hash.textContent = a ? '#' + a : ''; } });
    }, { rootMargin: '-30% 0px -65% 0px' });
    $$('[data-addr]').forEach(function (s) { ao.observe(s); });
  }

  /* 1. constellation map */
  var maps = [];
  $$('[data-map]').forEach(function (root) {
    var data = JSON.parse($('.map-data', root).textContent), view = $('.map-view', root), card = $('.map-card', root);
    var chips = $$('.fchip', root), byId = {}, sel = null, portrait = null, svg, W, H;
    data.nodes.forEach(function (n) { byId[n.id] = n; n.ph = Math.random() * 6.28; n.ox = 0; n.oy = 0; });
    function neighbors(id) {
      var s = {}; s[id] = 1;
      data.edges.forEach(function (e) { if (e[0] === id) s[e[1]] = 1; if (e[1] === id) s[e[0]] = 1; });
      return s;
    }
    function build() {
      var p = view.clientWidth < 520;
      if (p === portrait) return; portrait = p;
      W = p ? 350 : 760; H = p ? 600 : 590;
      if (svg) view.removeChild(svg);
      svg = el('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'group', 'aria-label': 'Map of Lucky Domains: four domains of work and six ventures. Select a node for details.' });
      var ge = el('g', {}), gn = el('g', {});
      data.edges.forEach(function (e) { e.el = el('line', { 'class': 'e e-' + e[2] }); ge.appendChild(e.el); });
      data.nodes.forEach(function (n) {
        n.x = n.pos[p ? 2 : 0]; n.y = n.pos[p ? 3 : 1];
        var cls = n.type === 'core' ? 'n n-core' : n.type === 'pillar' ? 'n n-p' : 'n n-v n-' + (n.status || '').toLowerCase().replace(' ', '-');
        var g = el('g', { 'class': cls, tabindex: '0', role: 'button', 'aria-label': n.title + (n.status ? ', ' + n.status.toLowerCase() : '') + '. ' + (n.type === 'pillar' ? 'Domain of work.' : '') });
        if (n.type === 'core') {
          g.appendChild(el('circle', { r: 40, 'class': 'n-ring' })); g.appendChild(el('circle', { r: 33, 'class': 'n-disc', fill: '#0c2340', stroke: 'rgba(255,255,255,.5)' }));
          var im = el('image', { href: data.icon, x: -19, y: -19, width: 38, height: 38 }); g.appendChild(im);
          g.firstChild.nextSibling.setAttribute('style', 'fill:#0c2340');
        } else if (n.type === 'pillar') {
          g.appendChild(el('circle', { r: 41, 'class': 'n-ring' })); g.appendChild(el('circle', { r: 35, 'class': 'n-disc' }));
          var t = el('text', { y: 4 }); t.textContent = n.label; g.appendChild(t);
        } else {
          g.appendChild(el('circle', { r: 26, 'class': 'n-hit' })); g.appendChild(el('circle', { r: 13, 'class': 'n-pulse' }));
          g.appendChild(el('circle', { r: 15, 'class': 'n-ring' })); g.appendChild(el('circle', { r: 8, 'class': 'n-dot' }));
          var tv = el('text', { y: 32 }); tv.textContent = n.label; g.appendChild(tv);
        }
        g.addEventListener('click', function () { select(n.id, true); });
        g.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); select(n.id, true); } });
        n.el = g; gn.appendChild(g);
      });
      svg.appendChild(ge); svg.appendChild(gn); view.appendChild(svg);
      place(); paint();
    }
    function place() {
      data.nodes.forEach(function (n) { n.el.setAttribute('transform', 'translate(' + (n.x + n.ox).toFixed(1) + ',' + (n.y + n.oy).toFixed(1) + ')'); });
      data.edges.forEach(function (e) {
        var a = byId[e[0]], b = byId[e[1]];
        e.el.setAttribute('x1', (a.x + a.ox).toFixed(1)); e.el.setAttribute('y1', (a.y + a.oy).toFixed(1));
        e.el.setAttribute('x2', (b.x + b.ox).toFixed(1)); e.el.setAttribute('y2', (b.y + b.oy).toFixed(1));
      });
    }
    function paint() {
      var nb = sel ? neighbors(sel) : null;
      data.nodes.forEach(function (n) {
        n.el.classList.toggle('sel', n.id === sel);
        n.el.classList.toggle('cold', !!nb && !nb[n.id] && n.type !== 'core');
        n.el.setAttribute('aria-pressed', n.id === sel);
      });
      data.edges.forEach(function (e) {
        var hot = sel && (e[0] === sel || e[1] === sel);
        e.el.classList.toggle('hot', !!hot); e.el.classList.toggle('cold', !!sel && !hot);
      });
      chips.forEach(function (c) { var p = c.getAttribute('data-pillar'); c.setAttribute('aria-pressed', sel ? p === sel : p === 'all'); });
    }
    function select(id, user) {
      sel = (id === sel || id === 'all') ? null : id;
      var n = byId[sel || 'core'], h = '<p class="map-card-k"><span class="chip' + (n.status === 'LIVE' ? ' st-live' : n.status === 'ACTIVE SERVICE' ? ' st-active-service' : '') + '">' + (n.status ? '<i aria-hidden="true"></i>' : '') + esc(n.chip) + '</span>' + (n.kind ? '<span class="vc-k">' + esc(n.kind) + '</span>' : '') + '</p>';
      h += '<h2>' + esc(n.title) + '</h2><p>' + esc(n.text) + '</p>';
      if (n.type === 'pillar') {
        var vs = data.nodes.filter(function (v) { return v.pillars && v.pillars.indexOf(n.id) > -1; }).map(function (v) { return esc(v.title); });
        h += '<p><b>Connected:</b> ' + vs.join(', ') + '.</p>';
      }
      h += '<p class="mc-l"><a class="lk" href="' + n.href + '">' + esc(n.cta) + '</a>' + (n.log ? '<a class="lk ext" href="' + n.log + '">' + esc(n.type === 'venture' && n.cta === 'Open the record' ? data.logLine : 'Build record on KenAshe.ai') + '</a>' : '') + '</p>';
      card.innerHTML = h;
      if (!reduce) { card.classList.remove('swap'); void card.offsetWidth; card.classList.add('swap'); }
      paint();
      if (user) stopped = true;
    }
    chips.forEach(function (c) { c.addEventListener('click', function () { select(c.getAttribute('data-pillar'), true); }); });

    /* ambient drift + cursor attraction; runs only while visible */
    var vis = false, raf = 0, mx = -9999, my = -9999, stopped = false, hold = false;
    function loop(now) {
      raf = 0; if (!vis || hold) return;
      var t = now / 1000;
      data.nodes.forEach(function (n) {
        var amp = n.type === 'core' ? 0 : n.type === 'pillar' ? 3.5 : 6;
        var tx = Math.sin(t * 0.42 + n.ph) * amp, ty = Math.cos(t * 0.35 + n.ph * 1.7) * amp;
        var dx = mx - n.x, dy = my - n.y, d = Math.sqrt(dx * dx + dy * dy);
        if (d < 150 && n.type !== 'core') { var k = (1 - d / 150) * 0.16; tx += dx * k; ty += dy * k; }
        n.ox += (tx - n.ox) * 0.08; n.oy += (ty - n.oy) * 0.08;
      });
      place(); raf = requestAnimationFrame(loop);
    }
    function kick() { if (!raf && !reduce) raf = requestAnimationFrame(loop); }
    if (!reduce) {
      new IntersectionObserver(function (en) { vis = en[0].isIntersecting; if (vis) kick(); }).observe(view);
      document.addEventListener('visibilitychange', function () { hold = document.hidden; if (!hold) kick(); });
      if (fine) {
        view.addEventListener('pointermove', function (e) { var b = view.getBoundingClientRect(); mx = (e.clientX - b.left) / b.width * W; my = (e.clientY - b.top) / b.height * H; });
        view.addEventListener('pointerleave', function () { mx = my = -9999; });
      }
    }
    build();
    window.addEventListener('resize', build);
    maps.push({ build: build, select: select });
  });

  /* 3. FLIP rearrangement of venture cards */
  $$('[data-gridfilter]').forEach(function (bar) {
    var grid = $('[data-grid]', bar.closest('section')), cards = $$('.vc', grid), order = cards.slice(), btns = $$('.fchip', bar);
    function apply(p) {
      var first = cards.map(function (c) { return c.getBoundingClientRect(); });
      var hit = order.filter(function (c) { return p === 'all' || c.getAttribute('data-pillars').split(' ').indexOf(p) > -1; });
      var rest = order.filter(function (c) { return hit.indexOf(c) < 0; });
      hit.concat(rest).forEach(function (c) { grid.appendChild(c); c.classList.toggle('dim', rest.indexOf(c) > -1); });
      btns.forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-pillar') === p); });
      if (reduce) return;
      cards.forEach(function (c, i) {
        var last = c.getBoundingClientRect(), dx = first[i].left - last.left, dy = first[i].top - last.top;
        if (!dx && !dy) return;
        c.animate([{ transform: 'translate(' + dx + 'px,' + dy + 'px)' }, { transform: 'none' }], { duration: 620, easing: 'cubic-bezier(.2,.8,.2,1)' });
      });
    }
    btns.forEach(function (b) { b.addEventListener('click', function () { apply(b.getAttribute('data-pillar')); }); });
    var want = new URLSearchParams(location.search).get('in');
    if (want && btns.some(function (b) { return b.getAttribute('data-pillar') === want; })) apply(want);
  });

  /* grid / map view toggle */
  var vb = $$('.seg button');
  if (vb.length) {
    var g = $('[data-grid]'), mv = $('[data-mapview]'), gf = $('[data-gridfilter]');
    vb.forEach(function (b) {
      b.addEventListener('click', function () {
        var m = b.getAttribute('data-view') === 'map';
        vb.forEach(function (o) { o.setAttribute('aria-pressed', o === b); });
        g.hidden = m; mv.hidden = !m; gf.hidden = m;
        if (m) maps.forEach(function (x) { x.build(); });
      });
    });
  }

  /* 4. layer stack */
  $$('[data-layers]').forEach(function (ly) {
    var rows = $$('[data-ly]', ly), plates = $$('[data-pl]', ly);
    function on(id) { rows.forEach(function (r) { r.classList.toggle('on', r.getAttribute('data-ly') === id); }); plates.forEach(function (p) { p.classList.toggle('on', p.getAttribute('data-pl') === id); }); }
    rows.forEach(function (r) {
      var id = r.getAttribute('data-ly');
      r.addEventListener('pointerenter', function () { on(id); });
      r.addEventListener('focusin', function () { on(id); });
      r.addEventListener('click', function () { on(id); });
    });
    on(rows[0].getAttribute('data-ly'));
    if (reduce || !('IntersectionObserver' in window)) { ly.classList.add('open'); return; }
    new IntersectionObserver(function (en) { ly.classList.toggle('open', en[0].isIntersecting); }, { rootMargin: '-25% 0px -25% 0px' }).observe(ly);
  });

  /* 5. tiles rise in */
  var rise = $$('.tile, .vc, .tl li, .l2-n, .rtc');
  if (!reduce && 'IntersectionObserver' in window) {
    var ro = new IntersectionObserver(function (en) { en.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); ro.unobserve(e.target); } }); }, { rootMargin: '0px 0px -6% 0px' });
    rise.forEach(function (r, i) { r.classList.add('rise'); r.style.transitionDelay = (i % 3) * 70 + 'ms'; ro.observe(r); });
  }

  /* contact routes. Nothing is sent. */
  var rt = $$('.rtc');
  if (rt.length) {
    var groups = $$('.cf-g'), pth = $('[data-cf-path]'), ttl = $('[data-cf-title]');
    var pick = function (b) {
      var id = b.getAttribute('data-route');
      rt.forEach(function (o) { o.setAttribute('aria-pressed', o === b); });
      groups.forEach(function (gp) { gp.hidden = gp.getAttribute('data-for') !== id; });
      pth.textContent = '/contact#' + id; ttl.textContent = $('b', b).textContent;
    };
    rt.forEach(function (b) { b.addEventListener('click', function () { pick(b); }); });
    var w = new URLSearchParams(location.search).get('path');
    rt.forEach(function (b) { if (b.getAttribute('data-route') === w) pick(b); });
  }
  $$('.cf').forEach(function (f) {
    f.addEventListener('submit', function (e) { e.preventDefault(); });
    var b = $('.btn', f), n = $('.cf-note', f);
    if (b) b.addEventListener('click', function () { n.textContent = 'Concept form. Nothing was collected, stored, or sent.'; });
  });
})();
