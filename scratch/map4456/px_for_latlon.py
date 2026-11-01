# Map the gazetteer's lat/lon points into mosaic pixels via the fit, and
# report where to cut. The fit: order-1 polynomial from georef.yml's fit
# (rms_m) — but georef.yml's fit block has no coefficients! Re-derive the
# order-1 fit from the four gcps here (the same least squares georef.py does),
# then invert it numerically for each target lat/lon.
import numpy as np
import yaml
import pyvips

geo = yaml.safe_load(open('maps/pelzucki1896/georef.yml', encoding='utf-8'))
pts = geo['gcps']
lon0 = np.mean([p['lon'] for p in pts])
lat0 = np.mean([p['lat'] for p in pts])
kx = np.cos(np.radians(lat0)) * 111320.0
ky = 110540.0
src = np.array([[p['x'], p['y']] for p in pts], float)
dst = np.array([[(p['lon'] - lon0) * kx, (p['lat'] - lat0) * ky] for p in pts], float)
A = np.column_stack([np.ones(len(src)), src[:, 0], src[:, 1]])
coef, *_ = np.linalg.lstsq(A, dst, rcond=None)
res = A @ coef - dst
print('rms m:', round(float(np.sqrt((res ** 2).mean())), 2))

targets = {
    'lazinsk-pierwszy cemetery': (17.911389, 52.103333),
    'glinianki mark (check)': (17.905495, 52.116919),
}
for name, (lon, lat) in targets.items():
    gx, gy = (lon - lon0) * kx, (lat - lat0) * ky
    # invert: solve A(x,y) = (gx,gy)
    M = np.array([[coef[1, 0], coef[2, 0]], [coef[1, 1], coef[2, 1]]])
    b = np.array([gx - coef[0, 0], gy - coef[0, 1]])
    x, y = np.linalg.solve(M, b)
    print('%-28s -> mosaic (%7.0f, %7.0f)' % (name, x, y))
