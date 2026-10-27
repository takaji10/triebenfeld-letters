/*
The viewer of a map in the edition (docs/MAPS_SITE_PLAN.md, section 3):
OpenSeadragon over the map's IIIF tiles in the second repository, the map
turned by the register's view_rotation so the lettering reads upright, the
editor's marks drawn at their points, and a mark's address (#<label-id>)
opening the map at it. The marks are in the pixels of the tiles' image
(the original's, adjusted for the map's crop by the build), so a new crop
or a better scan does not move them.
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

  // ---- the marks ---------------------------------------------------------
  var marks = {};
  viewer.addHandler('open', function () {
    if (ROT) viewer.viewport.setRotation(ROT, true);
    (M.labels || []).forEach(function (l) {
      if (!l.point) return;
      var d = document.createElement('div');
      d.className = 'map-mark';
      d.title = (l.form || '') + (l.place_name ? ' — ' + l.place_name : '');
      d.setAttribute('data-label', l.id);
      var p = viewer.viewport.imageToViewportCoordinates(
        new OpenSeadragon.Point(l.point[0], l.point[1]));
      viewer.addOverlay({ element: d, location: p });
      d.addEventListener('click', function () {
        location.hash = l.id;
        highlight(l.id);
      });
      marks[l.id] = d;
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
    var row = document.getElementById('mark-' + id);
    if (row && row.scrollIntoView) {
      row.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
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
    var id = (location.hash || '').replace(/^#/, '');
    if (id && byId[id]) focusLabel(id);
  }
  window.addEventListener('hashchange', focusFromHash);

  // A row's crop (the [data-label] links of the list) focuses the map on
  // its mark; the row's other links (the place's page) navigate as usual.
  document.querySelectorAll('.map-mark-list a[data-label]').forEach(function (el) {
    el.addEventListener('click', function (ev) {
      var id = el.getAttribute('data-label');
      if (byId[id] && byId[id].point) {
        ev.preventDefault();
        history.replaceState(null, '', '#' + id);
        focusLabel(id);
        viewerEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
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
