/*
The viewer of a map in the edition (docs/MAPS_SITE_PLAN.md, section 3):
OpenSeadragon over the map's IIIF tiles in the second repository, the map
shown as drawn (the button turns it by the register's view_rotation, north up), the
editor's marks drawn at their points. A mark names its place on hover,
and clicking it takes the reader to its row in the list below the details;
a row's name on the map takes the map to the mark; the address #<label-id> opens the
map at that mark. The marks are in the pixels of the tiles' image (the
original's, adjusted for the map's crop by the build), so a new crop or a
better scan does not move them.
*/
(function () {
  'use strict';
  var dataEl = document.getElementById('map-data');
  var viewerEl = document.getElementById('map-viewer');
  if (!dataEl || !viewerEl || typeof OpenSeadragon === 'undefined') return;
  var M = JSON.parse(dataEl.textContent);

  var viewer = OpenSeadragon({
    id: 'map-viewer',
    prefixUrl: '',
    showNavigationControl: false,
    tileSources: M.tiles,
    crossOriginPolicy: 'Anonymous',
    // GitHub Pages answers a request now and then with a passing 503; a
    // tile that fails is asked for again rather than left blank.
    tileRetryMax: 3,
    tileRetryDelay: 2000,
    maxZoomPixelRatio: 4,
    visibilityRatio: 0.5,
    animationTime: 0.6,
    gestureSettingsMouse: { clickToZoom: false, dblClickToZoom: true }
  });

  var ROT = M.view_rotation || 0;
  var byId = {};
  (M.labels || []).forEach(function (l) { if (l.id) byId[l.id] = l; });
  // The farmsteads of the liquidation (M.farms): one name label per farm
  // the editor has marked, a layer of its own, hidden until the tools
  // button turns it on; a click opens the farm's row in the table below.
  // The red numbers (M.reds), the statement's row numbers on each parcel,
  // are a second layer beside it; the two toggles are independent.
  var farms = M.farms || { marks: [] };
  var reds = M.reds || [];
  var farmTags = {};
  var redTags = [];
  // the page's language (the DE pages are separate pages): the
  // institution labels speak it
  var ML = document.documentElement.lang || 'en';
  var redTags = [];

  function layerOn(btn, on) {
    if (!btn) return;
    btn.setAttribute('aria-pressed', String(on));
  }

  var status = document.getElementById('map-status');
  function say(msg) {
    if (!status) return;
    status.textContent = msg;
    status.hidden = !msg;
  }

  // ---- the name on hover -------------------------------------------------
  // One floating label for every mark, in the page itself (the viewer's
  // container clips its children, so the tooltip lives outside it): shown
  // on hover or on focus, clamped to the window, gone on leave or click.
  var tipEl = document.createElement('div');
  tipEl.className = 'map-tip';
  tipEl.setAttribute('role', 'tooltip');
  tipEl.hidden = true;
  document.body.appendChild(tipEl);

  function showTip(d) {
    var txt = d.getAttribute('data-tip') || '';
    if (!txt) return;
    tipEl.textContent = txt;
    tipEl.hidden = false;
    var r = d.getBoundingClientRect();
    if (!r.width) { hideTip(); return; }
    var x = r.left + r.width / 2, y = r.bottom + 8;
    // clamp, then read the label's own width and clamp again
    tipEl.style.left = Math.round(x) + 'px';
    tipEl.style.top = Math.round(y) + 'px';
    var w = tipEl.offsetWidth;
    x = Math.min(Math.max(x, w / 2 + 8), window.innerWidth - w / 2 - 8);
    tipEl.style.left = Math.round(x) + 'px';
  }
  function hideTip() { tipEl.hidden = true; }

  // ---- the marks ---------------------------------------------------------
  var marks = {};
  viewer.addHandler('open', function () {
    (M.labels || []).forEach(function (l) {
      if (!l.point) return;
      var lid = l.id;
      var d = document.createElement('div');
      d.className = 'map-mark' + (l.role === 'letter' ? ' map-mark-letter' : '');
      d.setAttribute('role', 'button');
      d.setAttribute('tabindex', '0');
      var tip = l.name || l.form || '';
      if (l.role === 'letter' && l.letter && l.letter !== l.form) tip = l.letter;
      if (l.place_name && l.place_name !== l.form) tip += ' — ' + l.place_name;
      else if (l.name && l.form && l.name !== l.form) tip += ' — ' + l.form;
      d.setAttribute('data-tip', tip);
      d.setAttribute('aria-label', tip);
      d.setAttribute('data-label', lid);
      var p = viewer.viewport.imageToViewportCoordinates(
        new OpenSeadragon.Point(l.point[0], l.point[1]));
      // Centred on its point by the viewer itself (the mark has a fixed size, so
      // OpenSeadragon's centring holds at every zoom and turn); a margin hack
      // drifted off the point as the map was zoomed. Never turned with the map:
      // a circle stays a circle.
      viewer.addOverlay({
        element: d,
        location: p,
        placement: OpenSeadragon.Placement.CENTER,
        rotationMode: OpenSeadragon.OverlayRotationMode.NO_ROTATION
      });
      var activate = function () {
        highlight(lid);
        goToRow(lid);
        hideTip();
        history.replaceState(null, '', '#' + lid);
      };
      d.addEventListener('click', activate);
      d.addEventListener('keydown', function (ev) {
        if (ev.key === 'Enter' || ev.key === ' ') {
          ev.preventDefault();
          activate();
        }
      });
      d.addEventListener('mouseenter', function () { showTip(d); });
      d.addEventListener('mouseleave', hideTip);
      d.addEventListener('focus', function () { showTip(d); });
      d.addEventListener('blur', hideTip);
      marks[lid] = d;
    });
    focusFromHash();
  });
  // The tiles' info.json can meet a passing 503 from GitHub Pages (the
  // editor's report on Mapa dróg 1890, 2026-11-14, the file loading fine a
  // minute later): the opening is tried again three times, after 2, 5 and
  // 10 seconds, before the reader is told the tiles did not load. A failed
  // opening has added no marks, so a retry cannot double them.
  var openTries = 0;
  var RETRY_MS = [2000, 5000, 10000];
  viewer.addHandler('open', function () { if (openTries) say(''); });
  viewer.addHandler('open-failed', function (e) {
    if (openTries < RETRY_MS.length) {
      say(ML === 'de' ? 'Die Karte wird erneut geladen …'
                      : 'Loading the map again …');
      setTimeout(function () { viewer.open(M.tiles); }, RETRY_MS[openTries]);
      openTries += 1;
      return;
    }
    say(ML === 'de'
      ? 'Die Kartenkacheln wurden nicht geladen (' + (e.message || 'Fehler') + '). Bitte die Seite später neu laden.'
      : 'The map tiles did not load (' + (e.message || 'error') + '). Please reload the page later.');
  });

  // ---- the farmsteads' layer ----------------------------------------------
  // The liquidation's farmsteads as name labels over the plan (M.farms,
  // the editor's marks): hidden until the tools button turns the layer on,
  // a label's click opens the farm's row in the table below the map, a
  // row's Locate takes the map to the label.
  var farmLayerBtn = document.getElementById('farm-layer');
  var redsLayerBtn = document.getElementById('reds-layer');
  var redOn = false;
  // The two layers in one place: a name label shows when the farmsteads'
  // layer is on; a red number when its own is. An unsure reading (3[7?])
  // shows like any other - a doubtful number is marked by its brackets,
  // never hidden on a say-so.
  //
  // The visibility is a class, not an inline style: the viewer's own
  // drawHTML writes style.display="block" on every redraw - every zoom and
  // pan frame - which overrode an inline none and brought the labels back
  // while the map moved (the editor's report). A !important class holds.
  function applyLayers() {
    var namesOn = farmLayerBtn &&
      farmLayerBtn.getAttribute('aria-pressed') === 'true';
    Object.keys(farmTags).forEach(function (k) {
      farmTags[k].forEach(function (d) {
        d.classList.toggle('gone', !namesOn);
      });
    });
    redTags.forEach(function (t) {
      t.el.classList.toggle('gone', !redOn);
    });
  }
  function farmLayerOn(on) {
    if (!farmLayerBtn) return;
    layerOn(farmLayerBtn, on);
    applyLayers();
  }
  function redsLayerOn(on) {
    if (!redsLayerBtn) return;
    layerOn(redsLayerBtn, on);
    redOn = on;
    applyLayers();
  }
  if (farms.marks && farms.marks.length && farmLayerBtn) {
    viewer.addHandler('open', function () {
      farms.marks.forEach(function (f) {
        if (f.x == null || f.y == null) return;
        var d = document.createElement('div');
        d.className = 'farm-tag';
        d.setAttribute('role', 'button');
        d.setAttribute('tabindex', '0');
        d.setAttribute('data-farm', f.n);
        // the pill carries the proper spelling where the editor's
        // normalisation is firm (a map label is editorial, not a
        // transcription); institution rows speak the page's language -
        // German on the German page, English otherwise
        var nm = f.name;
        if (f.institution) {
          nm = (ML === 'de' && f.name_de) ? f.name_de : f.name;
        } else if (f.name_norm && f.norm_conf !== 'conjectural') {
          nm = f.name_norm;
        }
        d.textContent = '\u2116 ' + f.n + (nm ? ' \u00b7 ' + nm : '');
        if (f.total) d.setAttribute('data-tip', '\u2116 ' + f.n + ' \u2014 ' + f.total);
        var p = viewer.viewport.imageToViewportCoordinates(
          new OpenSeadragon.Point(f.x, f.y));
        viewer.addOverlay({
          element: d,
          location: p,
          placement: OpenSeadragon.Placement.CENTER,
          rotationMode: OpenSeadragon.OverlayRotationMode.NO_ROTATION
        });
        var act = function () { focusFarm(f.n); };
        d.addEventListener('click', act);
        d.addEventListener('keydown', function (ev) {
          if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); act(); }
        });
        d.addEventListener('mouseenter', function () { showTip(d); });
        d.addEventListener('mouseleave', hideTip);
        d.classList.remove('gone');   // the names layer is on by default
        // a farm number may carry several labels (a farmer can hold more
        // than one farmstead): the tags of one farm live in a list, so the
        // layer toggles and the highlight reach every one of them
        (farmTags[f.n] = farmTags[f.n] || []).push(d);
      });
    });
    farmLayerBtn.addEventListener('click', function () {
      farmLayerOn(farmLayerBtn.getAttribute('aria-pressed') !== 'true');
    });
  }
  if (reds.length && redsLayerBtn) {
    viewer.addHandler('open', function () {
      reds.forEach(function (r) {
        if (r.x == null || r.y == null) return;
        var d = document.createElement('div');
        d.className = 'red-tag' + (r.unsure ? ' unsure' : '');
        d.textContent = r.n;
        if (r.unsure) d.setAttribute('data-tip', r.n + ' (uncertain reading)');
        var p = viewer.viewport.imageToViewportCoordinates(
          new OpenSeadragon.Point(r.x, r.y));
        viewer.addOverlay({
          element: d,
          location: p,
          placement: OpenSeadragon.Placement.CENTER,
          rotationMode: OpenSeadragon.OverlayRotationMode.NO_ROTATION
        });
        d.addEventListener('mouseenter', function () { showTip(d); });
        d.addEventListener('mouseleave', hideTip);
        d.classList.add('gone');
        // the unsure flag rides along: a doubtful reading is NEVER hidden
        // by Hide linked, whatever number it carries - only a firm reading
        // whose farm has a mark goes (an unsure reading's brackets cannot
        // match a farm key anyway, but the flag makes the rule explicit)
        redTags.push({ el: d, n: r.n, unsure: !!r.unsure });
      });
    });
    redsLayerBtn.addEventListener('click', function () {
      redsLayerOn(redsLayerBtn.getAttribute('aria-pressed') !== 'true');
    });
  }

  // ---- the boundary walk, drawn on the map --------------------------------
  // The stretches of the boundary (labels with a role and a trace) as
  // polylines over the map, on a canvas above the viewer's own, redrawn on
  // every view change (the labelling page's overlay pattern).
  var bcanvas = document.createElement('canvas');
  bcanvas.className = 'map-boundary-canvas';
  viewerEl.appendChild(bcanvas);
  var bctx = bcanvas.getContext('2d');
  var bStretches = (M.labels || []).filter(function (l) {
    return l.role === 'boundary' && l.trace && l.trace.length > 1;
  });
  function sizeBCanvas() {
    var r = viewerEl.getBoundingClientRect(), dpr = window.devicePixelRatio || 1;
    bcanvas.style.width = r.width + 'px';
    bcanvas.style.height = r.height + 'px';
    bcanvas.width = Math.round(r.width * dpr);
    bcanvas.height = Math.round(r.height * dpr);
    bctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  function drawBoundary() {
    if (!bcanvas.width) return;
    var r = viewerEl.getBoundingClientRect();
    bctx.clearRect(0, 0, r.width, r.height);
    if (!viewer.world || !viewer.world.getItemCount()) return;
    bStretches.forEach(function (l) {
      var pts = l.trace.map(function (p) {
        var q = viewer.viewport.imageToViewerElementCoordinates(
          new OpenSeadragon.Point(p[0], p[1]));
        return [q.x, q.y];
      });
      bctx.beginPath();
      pts.forEach(function (p, i) { i ? bctx.lineTo(p[0], p[1]) : bctx.moveTo(p[0], p[1]); });
      bctx.strokeStyle = 'rgba(179, 51, 51, .8)';
      bctx.lineWidth = 2;
      bctx.setLineDash([7, 5]);
      bctx.lineJoin = 'round';
      bctx.lineCap = 'round';
      bctx.stroke();
      bctx.setLineDash([]);
      // the from-letter's square at the start
      bctx.fillStyle = '#b33';
      bctx.fillRect(pts[0][0] - 4, pts[0][1] - 4, 8, 8);
    });
  }
  ['animation', 'update-viewport', 'resize', 'rotate', 'open'].forEach(function (ev) {
    viewer.addHandler(ev, function () { sizeBCanvas(); drawBoundary(); });
  });
  window.addEventListener('resize', function () { sizeBCanvas(); drawBoundary(); });

  function highlight(id) {
    Object.keys(marks).forEach(function (k) {
      marks[k].classList.toggle('is-on', k === id);
    });
    document.querySelectorAll('.map-mark-list li').forEach(function (li) {
      li.classList.toggle('is-on', li.getAttribute('data-label') === id);
    });
  }

  // the reader's request: clicking a mark takes them to the spot in the
  // list of place names (the row, centred where the page can)
  function goToRow(id) {
    var row = document.getElementById('mark-' + id);
    if (row && row.scrollIntoView) {
      row.scrollIntoView({ block: 'center', behavior: 'smooth' });
    }
  }

  function focusLabel(id) {
    var l = byId[id];
    if (!l || (!l.point && !(l.trace && l.trace.length))) return;
    if (l.trace && l.trace.length) {
      // a boundary stretch: the map fits the whole line
      var x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
      l.trace.forEach(function (p) {
        x0 = Math.min(x0, p[0]); y0 = Math.min(y0, p[1]);
        x1 = Math.max(x1, p[0]); y1 = Math.max(y1, p[1]);
      });
      var pad = Math.max(120, Math.max(x1 - x0, y1 - y0) * 0.08);
      viewer.viewport.fitBounds(viewer.viewport.imageToViewportRectangle(
        x0 - pad, y0 - pad, (x1 - x0) + 2 * pad, (y1 - y0) + 2 * pad));
      highlight(id);
      return;
    }
    var p = viewer.viewport.imageToViewportCoordinates(
      new OpenSeadragon.Point(l.point[0], l.point[1]));
    // about 0.4 image pixels per screen pixel: a name's lettering readable
    var z = Math.min(viewer.viewport.imageToViewportZoom(0.4),
                     viewer.viewport.getMaxZoom());
    // zoom with no reference point, then pan: zooming about the point first
    // (zoomTo(z, p)) left the pan target to be overridden by the zoom's own
    // anchor, so the mark ended up off centre once the map had been zoomed
    // or dragged
    viewer.viewport.zoomTo(z);
    viewer.viewport.panTo(p);
    viewer.viewport.applyConstraints();
    highlight(id);
  }

  function highlightFarm(n) {
    var s = String(n);
    document.querySelectorAll('.farm-table tr[data-farm]').forEach(function (tr) {
      tr.classList.toggle('is-on', tr.getAttribute('data-farm') === s);
    });
    Object.keys(farmTags).forEach(function (k) {
      farmTags[k].forEach(function (d) {
        d.classList.toggle('is-on', k === s);
      });
    });
  }

  function focusFarm(n, opts) {
    var f = null;
    (farms.marks || []).forEach(function (x) { if (String(x.n) === String(n)) f = x; });
    if (!f || f.x == null) return;
    var p = viewer.viewport.imageToViewportCoordinates(
      new OpenSeadragon.Point(f.x, f.y));
    var z = Math.min(viewer.viewport.imageToViewportZoom(0.4),
                     viewer.viewport.getMaxZoom());
    viewer.viewport.zoomTo(z);
    viewer.viewport.panTo(p);
    viewer.viewport.applyConstraints();
    // the row is the point of the layer: with it off, the label would not
    // be there to meet the reader - turn it on
    if (farmLayerBtn && farmLayerBtn.getAttribute('aria-pressed') !== 'true') {
      farmLayerOn(true);
    }
    // the farmsteads are a tab below the map now: bring the pane forward
    // before any scroll into it
    if (window.__mapTab) window.__mapTab('farms');
    highlightFarm(n);
    var row = document.getElementById('farm-' + n);
    if (row && row.scrollIntoView && (!opts || opts.row !== false)) {
      row.scrollIntoView({ block: 'center', behavior: 'smooth' });
    }
    history.replaceState(null, '', '#farm-' + n);
  }

  function focusFromHash() {
    var h = (location.hash || '').replace(/^#/, '');
    if (h.indexOf('farm-') === 0) { focusFarm(h.slice(5)); return; }
    if (h && byId[h]) focusLabel(h);
  }
  window.addEventListener('hashchange', focusFromHash);

  // The map lives above these tables; a Locate called from down here
  // brings it into view as it flies to the mark (the index moved below
  // the map, 2026-11-06 - without this the reader saw the page scroll
  // nowhere and the map move off screen).
  var viewerEl = document.getElementById('map-viewer');
  function showMap() {
    if (viewerEl && viewerEl.scrollIntoView) {
      viewerEl.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }
  }

  // A farm row's Locate chip takes the map to the farm's mark.
  document.querySelectorAll('.farm-do a[data-farm]').forEach(function (el) {
    el.addEventListener('click', function (ev) {
      ev.preventDefault();
      focusFarm(el.getAttribute('data-farm'), { row: false });
      showMap();
    });
  });

  // A row's Locate (the [data-label] links of the index and the boundary)
  // takes the map to its mark; the row's other links navigate as usual.
  document.querySelectorAll('.map-mark-list a[data-label], .mark-table a[data-label], .map-boundary-letters a[data-label], .map-boundary-list a[data-label]').forEach(function (el) {
    el.addEventListener('click', function (ev) {
      var lid = el.getAttribute('data-label');
      if (byId[lid] && byId[lid].point) {
        ev.preventDefault();
        history.replaceState(null, '', '#' + lid);
        focusLabel(lid);
        showMap();
      }
    });
  });

  // ---- as drawn (the default) / north up ----------------------------------
  // The button names what a click does: "North up" while the map is as drawn,
  // "As drawn" once turned. A map with no view_rotation needs no button.
  var rotbtn = document.getElementById('map-rot');
  if (rotbtn) {
    if (!ROT) rotbtn.hidden = true;
    rotbtn.addEventListener('click', function () {
      var turned = viewer.viewport.getRotation() !== 0;
      viewer.viewport.setRotation(turned ? 0 : ROT, true);
      rotbtn.textContent = turned ? rotbtn.getAttribute('data-north')
                                  : rotbtn.getAttribute('data-drawn');
    });
  }
})();
