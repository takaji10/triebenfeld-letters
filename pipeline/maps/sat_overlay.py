# -*- coding: utf-8 -*-
"""The <key> plan warped over satellite imagery, with the farmstead labels.

    python pipeline/maps/sat_overlay.py <key>

Writes MAPS_REPO/<key>/sat_overlay.html (triebenfeld-maps, beside the
map's tiles and its georef.json): the tiles repository's warp test pattern
(warp.html, the Allmaps warp over OpenStreetMap's vector map) with the
base changed to satellite imagery (Esri World Imagery) and the
farmsteads' labels of maps/<key>/farms.yml laid over the warped plan.

A map needs farms.yml (the liquidation's settlers and the editor's yard
marks) for the page to be worth building; the script stops without one.

The labels' positions are the pixels of the mosaic (reference/maps.yml);
the page needs them on the ground, so the builder re-derives the order-1
polynomial fit from the control points of maps/<key>/georef.yml (the same
least squares pipeline/maps/georef.py fits; georef.yml's fit block records
rms_m but carries no coefficients) and converts every mark to lat/lon.
The fit's RMS stands in the page's note, so the reader knows how much to
trust a label's place.

The names follow the site's own farm layer (site/assets/maps/
map-viewer.js): the normalised spelling where the editor's reading is
firm, the tables' transliteration where it is conjectural; the 1896
extent rides the pill's tooltip.

Re-run after every import_farms.py: the page bakes the labels committed
at build time (a moved mark must be rebuilt into the page).
"""
import io
import json
import math
import os
import sys
from datetime import date

import numpy as np
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import MAPS_REPO, ROOT, die, load_map, read_yaml, utf8_stdout

# The edition's site (the page's note links the map's own page there).
SITE_BASE = "https://takaji10.github.io/triebenfeld-letters"


def fit_pixels_to_ground(pts):
    """The order-1 fit from mosaic pixels to lat/lon, georef.py's own
    least squares (lon/lat first differenced about their means, scaled to
    metres); returns (coef, lon0, lat0, kx, ky, rms_m)."""
    lon0 = float(np.mean([p["lon"] for p in pts]))
    lat0 = float(np.mean([p["lat"] for p in pts]))
    kx = math.cos(math.radians(lat0)) * 111320.0
    ky = 110540.0
    src = np.array([[p["x"], p["y"]] for p in pts], float)
    dst = np.array([[(p["lon"] - lon0) * kx, (p["lat"] - lat0) * ky]
                    for p in pts], float)
    A = np.column_stack([np.ones(len(src)), src[:, 0], src[:, 1]])
    coef, *_ = np.linalg.lstsq(A, dst, rcond=None)
    res = np.hypot(*((A @ coef - dst).T))
    return coef, lon0, lat0, kx, ky, float(math.sqrt((res ** 2).mean()))


def main():
    utf8_stdout()
    if len(sys.argv) != 2:
        die("usage: python pipeline/maps/sat_overlay.py <map>")
    key = sys.argv[1]
    m = load_map(key, check_file=False)
    farms_p = os.path.join(ROOT, "maps", key, "farms.yml")
    if not os.path.isfile(farms_p):
        die(f"maps/{key}/farms.yml is missing: the satellite overlay page "
            "shows the farmsteads' labels, and there are none to show")
    farms = read_yaml(farms_p)
    georef = read_yaml(os.path.join(ROOT, "maps", key, "georef.yml"))

    settlers = {s["n"]: s for s in (farms.get("settlers") or [])}
    coef, lon0, lat0, kx, ky, rms = fit_pixels_to_ground(georef["gcps"])
    marks = []
    for mk in (farms.get("marks") or []):
        if mk.get("x") is None:
            continue
        gx, gy = np.array([1.0, mk["x"], mk["y"]]) @ coef
        s = settlers.get(mk["n"]) or {}
        # the pill's name, the site's own rule (map-viewer.js): the
        # normalised spelling only where the editor's reading is firm
        nm = s.get("name")
        if s.get("institution"):
            nm = s.get("name")          # the page here is English
        elif s.get("name_norm") and s.get("norm_conf") != "conjectural":
            nm = s["name_norm"]
        marks.append({
            "n": mk["n"],
            "lat": round(float(lat0 + gy / ky), 6),
            "lon": round(float(lon0 + gx / kx), 6),
            "label": "\u2116 " + str(mk["n"]) + (nm and " \u00b7 " + nm or ""),
            "tip": "\u2116 " + str(mk["n"]) +
                   (s.get("total") and " \u2014 " + s["total"] or ""),
        })
    data = json.dumps({
        # the annotation beside the page (warp.html fetches its key's the
        # same way): relative, so the page serves from the tiles repo
        # locally and from its Pages alike
        "georef": "georef.json",
        "rms": round(rms, 2),
        "marks": marks,
        "page": f"{SITE_BASE}/maps/{key}/",
    }, ensure_ascii=False).replace("<", "\\u003c")
    page = TEMPLATE.replace("__DATA__", data).replace(
        "__TITLE__", (m.get("cited_as") or key)).replace(
        "__SLUG__", key).replace(
        "__TODAY__", date.today().isoformat())
    out = MAPS_REPO / key / "sat_overlay.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(page)
    print(f"sat_overlay.html: {len(marks)} labels, fit RMS {rms:.2f} m "
          f"-> {out}")


TEMPLATE = r"""<!DOCTYPE html>
<!--
  Generated by pipeline/maps/sat_overlay.py (__TODAY__); do not edit.
  The __TITLE__ plan warped over satellite imagery, with the farmstead
  labels of the liquidation baked in at build time - rebuild after every
  import of the editor's marks.
-->
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__ over satellite imagery</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.css">
<style>
  body { margin: 0; font: 14px/1.4 system-ui, sans-serif; }
  #bar { padding: 6px 10px; display: flex; gap: 12px; align-items: center; flex-wrap: wrap; }
  #bar .title { font-weight: 600; }
  #bar .note { color: #666; font-size: .82rem; }
  #bar a { color: #33628f; }
  #map { height: calc(100vh - 44px); background: #24241f; }
  button { font: inherit; font-size: .82rem; padding: .25rem .7rem;
           border: 1px solid #bbb; border-radius: 4px; background: #fff;
           cursor: pointer; }
  button[aria-pressed="true"] { border-color: #7a3b2e; color: #7a3b2e; font-weight: 600; }
  /* the farm pills, the site's own farm-tag shape (site/_layouts/map.html) */
  .farm-tag { font: 11px/1.25 system-ui, sans-serif; padding: 2px 8px;
              background: rgba(122, 59, 46, .92); color: #fff;
              border-radius: 10px; white-space: nowrap;
              box-shadow: 0 1px 3px rgba(0, 0, 0, .4); }
  .leaflet-control-attribution { font-size: 10px; }
</style>
</head>
<body>
<div id="bar">
  <span class="title">__TITLE__ over satellite imagery</span>
  <label>Plan opacity <input id="op" type="range" min="0" max="1" step="0.05" value="0.7"></label>
  <button id="labels" aria-pressed="true">Farm labels</button>
  <span class="note">the plan warped over Esri World Imagery; labels from the
  liquidation's farmsteads (fit RMS <span id="rms"></span> m) — the plan's own
  page: <a id="pagelink" href="#">/maps/__SLUG__/</a></span>
</div>
<div id="map"></div>
<script type="module">
import L from 'https://cdn.jsdelivr.net/npm/leaflet@1.9.4/+esm'
import { WarpedMapLayer } from 'https://cdn.jsdelivr.net/npm/@allmaps/leaflet@1.0.0-beta.54/+esm'

const D = __DATA__;
document.getElementById('rms').textContent = D.rms.toFixed(2);
document.getElementById('pagelink').href = D.page;

const map = L.map('map', { zoomAnimationThreshold: 1, maxZoom: 20 })
window.map = map
// the satellite base: Esri World Imagery (the image serves to z19 here;
// deeper zoom upscales it)
L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
  maxZoom: 20, maxNativeZoom: 19,
  attribution: 'Imagery &copy; <a href="https://www.esri.com/">Esri</a>, Maxar, Earthstar Geographics'
}).addTo(map)

// the warped plan, the annotation the editor has checked (georef.json)
const layer = new WarpedMapLayer().addTo(map)
window.warpLayer = layer
const annotation = await (await fetch(D.georef)).json()
await layer.addGeoreferenceAnnotation(annotation)
layer.setOpacity(0.7)
document.getElementById('op').addEventListener('input', e => layer.setOpacity(+e.target.value))
try { const b = layer.getBounds(); if (b) map.fitBounds(b) } catch (e) {}

// the farmsteads' labels: the committed marks of farms.yml, carried onto
// the ground by the map's fit (the generating script's note above)
const group = L.layerGroup().addTo(map)
D.marks.forEach(m => {
  L.marker([m.lat, m.lon], {
    icon: L.divIcon({ className: '', html: '<div class="farm-tag">' + m.label + '</div>', iconSize: null }),
    keyboard: false
  }).bindTooltip(m.tip).addTo(group)
})
const btn = document.getElementById('labels')
btn.addEventListener('click', () => {
  const on = btn.getAttribute('aria-pressed') !== 'true'
  btn.setAttribute('aria-pressed', String(on))
  if (on) group.addTo(map); else map.removeLayer(group)
})
</script>
</body>
</html>
"""

main()
