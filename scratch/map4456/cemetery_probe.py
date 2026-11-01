# Targeted: what numbers stand at the common cemetery (table no. 93,
# 2 des 282 saz per the statement) at mosaic (9942, 8911)?
import numpy as np
import pyvips
import easyocr

FULL = r"J:\Documents\Archive\Genealogy\References\Maps\Congress Poland (1815-1915)\Łazińskie Holendry (Muzeum Narodowe Rolnictwa w Szreniawie)\AN-4456\4456_full.jpg"
CX, CY, R = 9942, 8911, 450
im = pyvips.Image.new_from_file(FULL, access="random")
a = np.frombuffer(im.crop(CX - R, CY - R, 2 * R, 2 * R).write_to_memory(),
                  np.uint8).reshape(2 * R, 2 * R, 3)
Rc = a[:, :, 0].astype(int); G = a[:, :, 1].astype(int); B = a[:, :, 2].astype(int)
redness = np.clip(Rc - np.maximum(G, B), 0, 255)
darkness = 255 - ((Rc * 299 + G * 587 + B * 114) // 1000)

reader = easyocr.Reader(["en"], gpu=False,
                        model_storage_directory=r"C:\Users\Tersnaus\AppData\Local\Temp\opencode\easymodels",
                        user_network_directory=r"C:\Users\Tersnaus\AppData\Local\Temp\opencode\easynets",
                        verbose=False)

def scan(img, tag):
    res = reader.readtext(img, allowlist="0123456789/.,-",
                          text_threshold=0.35, low_text=0.25, link_threshold=0.2)
    print(tag)
    for box, txt, conf in res:
        xs = [p[0] for p in box]; ys = [p[1] for p in box]
        x0, x1 = int(min(xs)), int(max(xs)); y0, y1 = int(min(ys)), int(max(ys))
        print("   %-10s conf %.2f at mosaic (%d,%d) %dx%d" % (
            txt, conf, CX - R + x0, CY - R + y0, x1 - x0, y1 - y0))

scan(a, "colour crop:")
g = (255 - np.clip(redness * 1.8, 0, 255)).astype(np.uint8)
scan(np.stack([g] * 3, -1), "red-isolated:")
d = (255 - np.clip(darkness * 1.4, 0, 255)).astype(np.uint8)
scan(np.stack([d] * 3, -1), "dark-isolated:")
