/* The Places page: the text search, the "Near" search, the A-Z / Z-A buttons
   of each section, and the map (Leaflet 1.9.4 from cdnjs, as place-map.js
   loads it) with its markers by type. Data: window.PLACES_DATA and
   window.PLACES_CFG, written by _includes/places.html. A place with a
   three-part entry in place_coords.yml ("near X") is approximate: it counts in
   the distance search but gets no marker. */
(function () {
  var D = window.PLACES_DATA || [], C = window.PLACES_CFG || {};
  var form = document.getElementById('places-filters');
  if (!form) return;
  var q = document.getElementById('pl-q'), nearSel = document.getElementById('pl-near'),
      distSel = document.getElementById('pl-dist'), count = document.getElementById('pl-count'),
      note = document.getElementById('pl-note'), reset = document.getElementById('pl-reset');
  var bySlug = {};
  D.forEach(function (p) { bySlug[p.slug] = p; });

  /* kind_en -> group */
  var GROUP_OF = {
    'City': 'town', 'Town': 'town',
    'Village': 'village', 'Hamlet': 'village', 'Settlement': 'village', 'Isolated dwellings': 'village',
    'Olęder settlement': 'colony',
    'Estate': 'manor', 'Folwark': 'manor',
    'Water mill': 'craft', 'Windmills': 'craft', 'Tavern': 'craft',
    'Forest': 'land', 'Forest precinct': 'land', 'Field': 'land', 'Mound': 'land', 'Mounds': 'land', 'hill': 'land'
  };
  function groupOf(p) {
    var k = p.kind_en || '';
    if (GROUP_OF[k]) return GROUP_OF[k];
    if (/church|parish|chapel|kirche|kościół/i.test(k + ' ' + p.name)) return 'church';
    return 'other';
  }
  D.forEach(function (p) { p.group = groupOf(p); });

  function fold(s) {
    return (s || '').toLowerCase().replace(/ł/g, 'l').normalize('NFD').replace(/[̀-ͯ]/g, '');
  }

  /* the list items */
  var secs = [];
  document.querySelectorAll('.place-tier').forEach(function (sec) {
    var ul = sec.querySelector('.place-index'), bar = sec.querySelector('.place-sort');
    var items = Array.prototype.slice.call(ul.children).map(function (li, i) {
      var p = bySlug[li.dataset.slug || ''];
      return { li: li, p: p, i: i, text: fold(li.textContent + ' ' + (p ? p.kind_en + ' ' + p.german : '')), dist: null };
    });
    var s = { sec: sec, ul: ul, bar: bar, items: items, dir: 'az' };
    secs.push(s);
    if (bar) {
      bar.hidden = false;
      bar.addEventListener('click', function (e) {
        var b = e.target.closest('button[data-dir]');
        if (!b || b.dataset.dir === s.dir) return;
        s.dir = b.dataset.dir;
        bar.querySelectorAll('button').forEach(function (x) {
          var on = x === b; x.classList.toggle('is-on', on); x.setAttribute('aria-pressed', on);
        });
        render();
      });
    }
    var none = document.createElement('p');
    none.className = 'place-none'; none.hidden = true; none.textContent = C.none || 'No places.';
    ul.parentNode.appendChild(none);
    s.none = none;
  });

  /* the Near picker: the placed places, alphabetical */
  D.filter(function (p) { return p.lat !== null; })
    .sort(function (a, b) { return a.name.localeCompare(b.name, C.lang === 'de' ? 'de' : 'pl'); })
    .forEach(function (p) {
      var o = document.createElement('option'); o.value = p.slug; o.textContent = p.name; nearSel.appendChild(o);
    });

  function hav(a, b) {
    var R = 6371, r = Math.PI / 180;
    var dl = (b.lat - a.lat) * r, dn = (b.lon - a.lon) * r;
    var x = Math.sin(dl / 2) * Math.sin(dl / 2) +
      Math.cos(a.lat * r) * Math.cos(b.lat * r) * Math.sin(dn / 2) * Math.sin(dn / 2);
    return 2 * R * Math.asin(Math.min(1, Math.sqrt(x)));
  }
  function fmt(d) { return (d < 10 ? d.toFixed(1) : String(Math.round(d))) + ' ' + (C.km || 'km'); }

  var visible = {};   /* slug -> true while its list item shows */

  function render() {
    var terms = fold(q.value).split(/\s+/).filter(Boolean);
    var origin = nearSel.value ? bySlug[nearSel.value] : null;
    var maxd = parseFloat(distSel.value);
    var shown = 0;
    visible = {};
    secs.forEach(function (s) {
      var list = [];
      s.items.forEach(function (it) {
        var d = it.li.querySelector('.dist'); if (d) d.remove();
        it.dist = null;
        var ok = terms.every(function (t) { return it.text.indexOf(t) >= 0; });
        if (ok && origin) {
          if (!it.p || it.p.lat === null) ok = false;
          else { it.dist = hav(origin, it.p); if (it.dist > maxd) ok = false; }
        }
        it.li.hidden = !ok;
        if (ok) { list.push(it); if (it.p) visible[it.p.slug] = true; }
      });
      list.sort(function (a, b) {
        if (origin) return a.dist - b.dist || a.i - b.i;
        return s.dir === 'az' ? a.i - b.i : b.i - a.i;
      });
      s.items.forEach(function (it) { if (it.li.hidden) s.ul.appendChild(it.li); });
      list.forEach(function (it) {
        s.ul.insertBefore(it.li, s.ul.querySelector('li[hidden]'));
        if (origin) {
          var sp = document.createElement('span'); sp.className = 'dist';
          /* an approximate position (the gazetteer's "north of Łukom") gives
             only a rough distance: "c. 3 km", or "close by" under 1.5 km */
          if (it.p.approx || origin.approx) {
            var de = C.lang === 'de';
            sp.textContent = it.dist < 1.5 ? (de ? 'in der Nähe' : 'close by')
              : (de ? 'ca. ' : 'c. ') + Math.round(it.dist) + ' ' + (C.km || 'km');
          } else sp.textContent = fmt(it.dist);
          var kind = it.li.querySelector('.kind');
          if (kind) { it.li.insertBefore(sp, kind); it.li.insertBefore(document.createTextNode(' '), kind); } else it.li.appendChild(sp);
          it.li.insertBefore(document.createTextNode(' '), sp);
        }
      });
      shown += list.length;
      s.none.hidden = list.length > 0;
      if (s.bar) s.bar.hidden = !!origin;
    });
    note.hidden = !origin;
    count.textContent = shown + ' ' + (C.n_places || 'places');
    updateMap();
  }

  q.addEventListener('input', render);
  nearSel.addEventListener('change', function () { render(); if (map) fitVisible(); });
  distSel.addEventListener('change', function () { render(); if (map) fitVisible(); });
  reset.addEventListener('click', function () {
    q.value = ''; nearSel.value = ''; distSel.value = '10';
    secs.forEach(function (s) {
      s.dir = 'az';
      if (s.bar) s.bar.querySelectorAll('button').forEach(function (x) {
        var on = x.dataset.dir === 'az'; x.classList.toggle('is-on', on); x.setAttribute('aria-pressed', on);
      });
    });
    render(); if (map) fitArea();
  });

  /* ---------------- the map ---------------- */
  var map = null, markers = {}, layer = null;
  var tierOn = { tier1: true, tier2: true }, groupOn = {};
  var ICONS = {
    town: 'M4 20V9l5-3v14M9 20V4l6 3v13M15 20v-8l5 2v6M3 20h18',
    village: 'M4 11l8-6 8 6M6 10v9h12v-9M10 19v-5h4v5',
    colony: 'M2 12l5-4 5 4M3.5 11.5V18h7v-6.5M12 15l5-4 5 4M13.5 14.5V19h7v-4.5',
    manor: 'M3 20h18M5 20V10l7-5 7 5v10M9 20v-6h6v6M9 10h.01M15 10h.01',
    craft: 'M9 12a3 3 0 1 0 6 0a3 3 0 1 0-6 0M12 3v4M12 17v4M3 12h4M17 12h4M5.6 5.6l2.8 2.8M15.6 15.6l2.8 2.8M18.4 5.6l-2.8 2.8M8.4 15.6l-2.8 2.8',
    church: 'M12 2v5M10 4.5h4M7 21V12l5-4 5 4v9M10 21v-4a2 2 0 0 1 4 0v4M4 21h16',
    land: 'M12 3l5 8h-3l4 6H6l4-6H7zM12 17v4',
    other: 'M8 12a4 4 0 1 0 8 0a4 4 0 1 0-8 0M12 2v3M12 19v3M2 12h3M19 12h3'
  };
  var ORDER = ['town', 'village', 'colony', 'manor', 'craft', 'church', 'land', 'other'];
  function svg(g, size) {
    return '<svg viewBox="0 0 24 24" width="' + size + '" height="' + size + '" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="' + ICONS[g] + '"/></svg>';
  }

  /* the legend: a checkbox per group that has markers */
  var present = {};
  D.forEach(function (p) { if (p.lat !== null && !p.approx) present[p.group] = true; });
  var lg = document.getElementById('pl-groups');
  ORDER.forEach(function (g) {
    if (!present[g]) return;
    groupOn[g] = true;
    var lab = document.createElement('label'); lab.className = 'chk';
    lab.innerHTML = '<input type="checkbox" data-group="' + g + '" checked><span class="pl-ico">' + svg(g, 18) + '</span><span></span>';
    lab.lastChild.textContent = (C.groups || {})[g] || g;
    lg.appendChild(lab);
  });
  document.getElementById('places-legend').addEventListener('change', function (e) {
    var t = e.target;
    if (t.dataset.tier) tierOn[t.dataset.tier] = t.checked;
    if (t.dataset.group) groupOn[t.dataset.group] = t.checked;
    updateMap();
  });

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]; }); }

  function updateMap() {
    if (!map) return;
    Object.keys(markers).forEach(function (slug) {
      var m = markers[slug], p = bySlug[slug];
      var on = visible[slug] && tierOn[p.tier] && groupOn[p.group];
      if (on && !layer.hasLayer(m)) layer.addLayer(m);
      if (!on && layer.hasLayer(m)) layer.removeLayer(m);
    });
  }
  function fitTo(list) {
    if (!list.length) return;
    map.fitBounds(list.map(function (p) { return [p.lat, p.lon]; }), { padding: [30, 30], maxZoom: 14 });
  }
  function fitArea() {
    fitTo(D.filter(function (p) { return p.tier === 'tier1' && p.lat !== null && !p.approx; }));
  }
  function fitVisible() {
    var origin = nearSel.value ? bySlug[nearSel.value] : null;
    if (!origin) { fitArea(); return; }
    var l = Object.keys(markers).filter(function (s) { return visible[s]; }).map(function (s) { return bySlug[s]; });
    if (origin.lat !== null) l.push(origin);
    fitTo(l);
  }

  var el = document.getElementById('places-map');
  if (!el) return;
  var V = '1.9.4', B = 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/' + V + '/';
  var css = document.createElement('link'); css.rel = 'stylesheet'; css.href = B + 'leaflet.min.css';
  document.head.appendChild(css);
  var js = document.createElement('script'); js.src = B + 'leaflet.min.js';
  js.onload = function () {
    var L = window.L;
    L.Icon.Default.imagePath = B + 'images/';
    map = L.map(el, { scrollWheelZoom: false }).setView([52.2, 18.0], 10);
    var street = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19, attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    var sat = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
      maxZoom: 19, attribution: 'Esri, Maxar, Earthstar Geographics'
    });
    var names = {}; names[C.street || 'Map'] = street; names[C.sat || 'Satellite'] = sat;
    L.control.layers(names, null, { collapsed: true }).addTo(map);
    layer = L.layerGroup().addTo(map);
    D.forEach(function (p) {
      if (p.lat === null || p.approx) return;
      var icon = L.divIcon({
        className: 'pm pm-' + (p.tier === 'tier1' ? 't1' : 't2'),
        html: svg(p.group, 16), iconSize: [26, 26], iconAnchor: [13, 13], popupAnchor: [0, -13]
      });
      var m = L.marker([p.lat, p.lon], { icon: icon, title: p.name, alt: p.name, keyboard: true });
      m.bindPopup('<strong>' + (p.url ? '<a href="' + esc(p.url) + '">' + esc(p.name) + '</a>' : esc(p.name)) + '</strong>' +
        (p.kind ? '<br><span class="pm-kind">' + esc(p.kind) + '</span>' : ''));
      markers[p.slug] = m;
    });
    el.classList.add('is-ready');
    fitArea();
    updateMap();
  };
  document.head.appendChild(js);
  render();
})();
