# Quick test of the OCR approach on a few tiles.
import importlib.util, sys, time
spec = importlib.util.spec_from_file_location(
    "numbers_ocr", r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\numbers_ocr.py")
# don't execute module (it runs everything); copy the helpers instead
import numpy as np, pyvips, PIL.Image, pytesseract, time
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
FULL = r"J:\Documents\Archive\Genealogy\References\Maps\Congress Poland (1815-1915)\Łazińskie Holendry (Muzeum Narodowe Rolnictwa w Szreniawie)\AN-4456\4456_full.jpg"
im = pyvips.Image.new_from_file(FULL, access="random")
CFG = "--psm 11 -c tessedit_char_whitelist=0123456789/.,-"

def ocr_tile(a, ox, oy):
    R = a[:, :, 0].astype(int); G = a[:, :, 1].astype(int); B = a[:, :, 2].astype(int)
    lum = (R * 299 + G * 587 + B * 114) // 1000
    red = (R > 110) & (R - G > 45) & (R - B > 45)
    dark = (lum < 135) & (R - G < 30) & (R - B < 30)
    out = []
    for kind, mask in (("red", red), ("black", dark)):
        if mask.sum() < 30:
            continue
        img = np.where(mask, 0, 255).astype(np.uint8)
        img = np.stack([img] * 3, axis=-1)
        pil = PIL.Image.fromarray(img)
        t0 = time.time()
        data = pytesseract.image_to_data(pil, config=CFG, output_type=pytesseract.Output.DICT)
        n = 0
        for i in range(len(data["text"])):
            t = data["text"][i].strip(); c = int(data["conf"][i])
            if not t or c < 40:
                continue
            core = t.replace("/", "").replace(".", "").replace(",", "").replace("-", "")
            if not core or not core.isdigit():
                continue
            out.append((kind, t, c, ox + data["left"][i], oy + data["top"][i], data["width"][i], data["height"][i]))
            n += 1
        print("  %s: %d tokens, %.1fs, ink %d px" % (kind, n, time.time() - t0, mask.sum()))
    return out

for (ox, oy) in [(8192, 8192), (12288, 4096), (4096, 4096)]:
    tile = np.frombuffer(im.crop(ox, oy, 2048, 2048).write_to_memory(), np.uint8).reshape(2048, 2048, 3)
    print("tile", ox, oy)
    for t in ocr_tile(tile, ox, oy):
        print("   ", t)
