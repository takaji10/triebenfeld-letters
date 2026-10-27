/*
The viewer of a map in the edition (docs/MAPS_SITE_PLAN.md, section 3):
OpenSeadragon over the map's IIIF tiles in the second repository, the map
turned by the register's view_rotation so the lettering reads upright, the
editor's marks drawn at their points. A mark names its place on hover,
and clicking it takes the reader to its row in the list below the details;
a row's crop takes the map to the mark; the address #<label-id> opens the
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
    maxZoomPixelRatio: 4,
    visibilityRatio: 0.5,
    animationTime: 0.6,
    gestureSettingsMouse: { clickToZoom: false, dblClickToZoom: true }
  });

  var ROT = M.view_rotation || 0;
  var byId = {};
  (M.labels || []).forEach(function (l) { if (l.id) byId[l.id] = l; });

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
    if (ROT) viewer.viewport.setRotation(ROT, true);
    (M.labels || []).forEach(function (l) {
      if (!l.point) return;
      var lid = l.id;
      var d = document.createElement('div');
      d.className = 'map-mark';
      d.setAttribute('role', 'button');
      d.setAttribute('tabindex', '0');
      var tip = l.form || '';
      if (l.place_name && l.place_name !== l.form) tip += ' — ' + l.place_name;
      d.setAttribute('data-tip', tip);
      d.setAttribute('aria-label', tip);
      d.setAttribute('data-label', lid);
      var p = viewer.viewport.imageToViewportCoordinates(
        new OpenSeadragon.Point(l.point[0], l.point[1]));
      viewer.addOverlay({ element: d, location: p });
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
  viewer.addHandler('open-failed', function (e) {
    say('The map tiles did not load (' + (e.message || 'error') + ').');
  });

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
    if (!l || !l.point) return;
    var p = viewer.viewport.imageToViewportCoordinates(
      new OpenSeadragon.Point(l.point[0], l.point[1]));
    // about 0.4 image pixels per screen pixel: a name's lettering readable
    var z = Math.min(viewer.viewport.imageToViewportZoom(0.4),
                     viewer.viewport.getMaxZoom());
    viewer.viewport.zoomTo(z, p);
    viewer.viewport.panTo(p);
    highlight(id);
  }

  function focusFromHash() {
    var h = (location.hash || '').replace(/^#/, '');
    if (h && byId[h]) focusLabel(h);
  }
  window.addEventListener('hashchange', focusFromHash);

  // A row's crop (the [data-label] links of the list) takes the map to its
  // mark; the row's other links (the place's page) navigate as usual.
  document.querySelectorAll('.map-mark-list a[data-label]').forEach(function (el) {
    el.addEventListener('click', function (ev) {
      var lid = el.getAttribute('data-label');
      if (byId[lid] && byId[lid].point) {
        ev.preventDefault();
        history.replaceState(null, '', '#' + lid);
        focusLabel(lid);
      }
    });
  });

  // ---- as drawn / north up ----------------------------------------------
  var rotbtn = document.getElementById('map-rot');
  if (rotbtn) {
    rotbtn.addEventListener('click', function () {
      var north = viewer.viewport.getRotation() !== 0;
      viewer.viewport.setRotation(north ? 0 : ROT, true);
      rotbtn.textContent = north ? rotbtn.getAttribute('data-drawn')
                                 : rotbtn.getAttribute('data-north');
    });
  }
})();
