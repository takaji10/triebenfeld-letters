# Shared helper: mosaic pixel -> lat/lon via the georef fit (same method as
# scratch/map4456/px_for_latlon.py). import: from geo_fit import px_to_ll
import numpy as np
import yaml

_GEO = yaml.safe_load(open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\maps\pelzucki1896\georef.yml", encoding="utf-8"))
_pts = _GEO["gcps"]
lon0 = np.mean([p["lon"] for p in _pts])
lat0 = np.mean([p["lat"] for p in _pts])
kx = np.cos(np.radians(lat0)) * 111320.0
ky = 110540.0
src = np.array([[p["x"], p["y"]] for p in _pts], float)
dst = np.array([[(p["lon"] - lon0) * kx, (p["lat"] - lat0) * ky] for p in _pts], float)
A = np.column_stack([np.ones(len(src)), src[:, 0], src[:, 1]])
coef, *_ = np.linalg.lstsq(A, dst, rcond=None)
M = np.array([[coef[1, 0], coef[2, 0]], [coef[1, 1], coef[2, 1]]])
c0 = coef[0]

def px_to_ll(x, y):
    """mosaic pixel -> (lon, lat): the order-1 fit evaluated forward"""
    gx, gy = c0 + M @ np.array([x, y])
    return (lon0 + gx / kx, lat0 + gy / ky)
