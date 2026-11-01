# EasyOCR on the red cluster patch: what does it read?
import numpy as np
import pyvips
import PIL.Image
import easyocr

FULL = r"J:\Documents\Archive\Genealogy\References\Maps\Congress Poland (1815-1915)\Łazińskie Holendry (Muzeum Narodowe Rolnictwa w Szreniawie)\AN-4456\4456_full.jpg"
X0, Y0, W, H = 12900, 8300, 1500, 1200
im = pyvips.Image.new_from_file(FULL, access="random")
a = np.frombuffer(im.crop(X0, Y0, W, H).write_to_memory(), np.uint8).reshape(H, W, 3)
R = a[:, :, 0].astype(int); G = a[:, :, 1].astype(int); B = a[:, :, 2].astype(int)

reader = easyocr.Reader(["en"], gpu=False,
                        model_storage_directory=r"C:\Users\Tersnaus\AppData\Local\Temp\opencode\easymodels",
                        user_network_directory=r"C:\Users\Tersnaus\AppData\Local\Temp\opencode\easynets",
                        verbose=True)

# plain colour crop, and a red-isolated version
pil = PIL.Image.fromarray(a)
res = reader.readtext(np.array(pil), allowlist="0123456789/.,-", 
                      text_threshold=0.4, low_text=0.25, link_threshold=0.2)
print("colour crop results:")
for box, txt, conf in res:
    xs = [p[0] for p in box]; ys = [p[1] for p in box]
    print("   %-14s conf %.2f  at (%d,%d) size %dx%d" % (
        txt, conf, X0 + min(xs), Y0 + min(ys), max(xs) - min(xs), max(ys) - min(ys)))

redness = np.clip(R - np.maximum(G, B), 0, 255)
g = (255 - np.clip(redness * 1.8, 0, 255)).astype(np.uint8)
pil2 = PIL.Image.fromarray(np.stack([g] * 3, -1))
res2 = reader.readtext(np.array(pil2), allowlist="0123456789/.,-",
                       text_threshold=0.4, low_text=0.25, link_threshold=0.2)
print("red-isolated results:")
for box, txt, conf in res2:
    xs = [p[0] for p in box]; ys = [p[1] for p in box]
    print("   %-14s conf %.2f  at (%d,%d) size %dx%d" % (
        txt, conf, X0 + min(xs), Y0 + min(ys), max(xs) - min(xs), max(ys) - min(ys)))
