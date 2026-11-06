<script>
  // The Leaflet wrapper: circle markers sized by event count, a popup per
  // place linking to the place page. Two raster tile layers, switched
  // from the control in the corner: OpenStreetMap and Esri World
  // Imagery (satellite) - both keyless.
  import { onMount, onDestroy } from 'svelte'
  import * as L from 'leaflet'
  import 'leaflet/dist/leaflet.css'

  let { points = [], height = '60vh', focus = null, zoom = 5 } = $props()

  let el
  let map
  let layers = {}
  let layer = $state('osm')

  onMount(() => {
    map = L.map(el, { preferCanvas: true }).setView([52, 19], zoom)
    layers = {
      osm: L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      }),
      sat: L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        maxZoom: 19,
        attribution: 'Tiles &copy; Esri — Source: Esri, Maxar, Earthstar Geographics',
      }),
    }
    layers[layer].addTo(map)
  })

  $effect(() => {
    if (!map || !layers[layer]) return
    for (const key of Object.keys(layers)) {
      if (key === layer) layers[key].addTo(map)
      else map.removeLayer(layers[key])
    }
  })

  onDestroy(() => { if (map) map.remove() })

  let drawn = []
  $effect(() => {
    if (!map) return
    for (const m of drawn) m.remove()
    drawn = []
    if (!points.length) return
    const byCount = points.slice().sort((a, b) => a.n - b.n)
    const lo = byCount[0].n, hi = byCount[byCount.length - 1].n
    for (const p of points) {
      const t = hi > lo ? (Math.log(p.n) - Math.log(lo)) / (Math.log(hi) - Math.log(lo)) : 1
      const m = L.circleMarker(p.coords, {
        radius: 4 + t * 8,
        color: '#7a3b2e', weight: 1, fillColor: '#a3543f',
        fillOpacity: 0.65,
      }).addTo(map)
      m.bindPopup(
        `<b>${p.name.replace(/</g, '&lt;')}</b><br>` +
        `${p.n} event${p.n === 1 ? '' : 's'} · ` +
        `<a href="#/place/${encodeURIComponent(p.name)}">open</a>`)
      drawn.push(m)
    }
    if (focus) {
      map.setView(focus, 12)
    } else {
      map.fitBounds(L.latLngBounds(points.map(p => p.coords)), {
        padding: [20, 20], maxZoom: 9,
      })
    }
  })
</script>

<div class="wrap" style:height>
  <div bind:this={el} class="map"></div>
  <div class="layers">
    <button class:active={layer === 'osm'} onclick={() => { layer = 'osm' }}>Map</button>
    <button class:active={layer === 'sat'} onclick={() => { layer = 'sat' }}>Satellite</button>
  </div>
</div>

<style>
  .wrap { position: relative; }
  .map { height: 100%; border: 1px solid var(--rule);
    border-radius: 3px; background: #dfe8ef; }
  .layers { position: absolute; top: .5rem; right: .5rem; z-index: 500;
    display: flex; gap: 2px; }
  .layers button { font: inherit; font-size: .72rem; padding: .15rem .5rem;
    border: 1px solid var(--rule); background: #fff; color: var(--ink);
    cursor: pointer; }
  .layers button.active { background: var(--accent); color: #fff;
    border-color: var(--accent); }
</style>
