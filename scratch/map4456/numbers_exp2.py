# Experiment 2: native-res grayscale-ink image of a red cluster region,
# full OCR output with boxes (no whitelist), to see what tesseract can see.
import numpy as np
import pyvips
import PIL.Image
import pytesseract

FULL = r"J:\Documents\Archive\Genealogy\References\Maps\Congress Poland (1815-1915)\Łazińskie Holendry (Muzeum Narodowe Rolnictwa w Szreniawie)\AN-4456\4456_full.jpg"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
OUT = r"C:\Users\Tersnaus\AppData\Local\Temp\opencode\p1896_red1.jpg"

X0, Y0, W, H = 12900, 8300, 1500, 1200
im = pyvips.Image.new_from_file(FULL, access="random")
a = np.frombuffer(im.crop(X0, Y0, W, H).write_to_memory(), np.uint8).reshape(H, W, 3)
R = a[:, :, 0].astype(int); G = a[:, :, 1].astype(int); B = a[:, :, 2].astype(int)

# redness: how far the pixel leans red, clipped
redness = np.clip(R - np.maximum(G, B), 0, 255)
# darken: ink where redness high; keep antialias as gray
g = 255 - np.clip(redness * 1.8, 0, 255).astype(np.uint8)
pil = PIL.Image.fromarray(np.stack([g] * 3, -1))
pil.save(OUT, quality=92)

for cfg in ("--psm 11", "--psm 12"):
    d = pytesseract.image_to_data(pil, config=cfg, output_type=pytesseract.Output.DICT)
    lines = []
    for i in range(len(d["text"])):
        t = d["text"][i].strip()
        if t and int(d["conf"][i]) > 25:
            lines.append((t, d["conf"][i], X0 + d["left"][i], Y0 + d["top"][i], d["width"][i], d["height"][i]))
    print(cfg, "tokens", len(lines))
    for t in lines:
        print("   ", t)
