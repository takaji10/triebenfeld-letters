/* The header map of a place page: Leaflet over OpenStreetMap with a
   satellite layer (Esri World Imagery) and one marker. Leaflet is loaded
   from cdnjs only on a page that has the map. Without script the page's
   link to openstreetmap.org stays. */
(function () {
  var el = document.querySelector('.place-leaflet');
  if (!el) return;
  var V = '1.9.4', B = 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/' + V + '/';
  var css = document.createElement('link');
  css.rel = 'stylesheet'; css.href = B + 'leaflet.min.css';
  document.head.appendChild(css);
  var js = document.createElement('script');
  js.src = B + 'leaflet.min.js';
  js.onload = function () {
    var L = window.L;
    var lat = parseFloat(el.dataset.lat), lon = parseFloat(el.dataset.lon);
    var zoom = parseInt(el.dataset.zoom || '13', 10);
    L.Icon.Default.imagePath = B + 'images/';
    var map = L.map(el, { scrollWheelZoom: false }).setView([lat, lon], zoom);
    var street = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    var sat = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
      maxZoom: 19, attribution: 'Esri, Maxar, Earthstar Geographics'
    });
    var names = {};
    names[el.dataset.street || 'Map'] = street;
    names[el.dataset.sat || 'Satellite'] = sat;
    L.control.layers(names, null, { collapsed: false }).addTo(map);
    L.marker([lat, lon], { title: el.dataset.title || '' }).addTo(map);
    el._leaflet = map;
    el.classList.add('is-ready');
  };
  document.head.appendChild(js);
})();
