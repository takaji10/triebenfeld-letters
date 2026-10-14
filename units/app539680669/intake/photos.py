# -*- coding: utf-8 -*-
"""The second notebook of APP 53/968/0/-/669: the editor's raw photos IMG_5192 to IMG_5205, made into page images.

    python units/app539680669/intake/photos.py

The editor photographed the notebook "V. Grodziec Juli 1936" on a table in
April 2023 as Canon raw files (.CR2), in the unit's folder, one opening to a
photo. They are added to the holding as its document 2 (editor, 2026-10-14).

No raw converter is installed here. Each CR2 carries a full-size JPEG preview
(5184 x 3456), the camera's own rendering; it is taken out of the file (the
largest embedded JPEG that opens) and cut to the notebook by BOXES, found by
the saturation of the wood against the paper and checked by eye, with a
margin. The results go to PHOTOS (a folder beside the archive's scans) as
IMG_5192.jpg ...; holding.py cuts them at the fold like the scans.

IMG_5205 carries the orientation flag 6 (turn 90 degrees clockwise), which is
why a viewer shows it on its side: the camera took it for an upright shot.
The preview inside the file is stored unturned and is the right way up, so
the flag is ignored here.
"""
import io
import os
import struct

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_FOLDER = (r"J:\Documents\Archive\Genealogy\References\Poznań State Archives"
               r"\Grodziec [Notatki dotyczące Grodźca, Józefowa Zamentu, Łazińska] (53.968.0.-.669)")
RAW = os.path.join(UNIT_FOLDER, 'Notes on Łazińsk (53.968.0.-.669)')
PHOTOS = 'photos_V_Grodziec'          # under RAW

# The notebook in each preview: (left, top, right, bottom), margin included.
BOXES = {
    5192: (1716, 764, 3196, 3028),
    5193: (884, 604, 3892, 3052),
    5194: (1108, 740, 3948, 3100),
    5195: (1084, 748, 3988, 3148),
    5196: (1116, 676, 4020, 3084),
    5197: (1172, 820, 3972, 3140),
    5198: (1240, 540, 4140, 3080),
    5199: (1348, 796, 4060, 3060),
    5200: (1268, 868, 3996, 3140),
    5201: (1196, 764, 3956, 3060),
    5202: (1100, 692, 3876, 2932),
    5203: (1180, 884, 3836, 3092),
    5204: (1320, 760, 3960, 3010),
    5205: (1436, 804, 3200, 3036),
}


def tiff_offsets(b):
    end = '<' if b[:2] == b'II' else '>'
    u16 = lambda o: struct.unpack(end + 'H', b[o:o + 2])[0]
    u32 = lambda o: struct.unpack(end + 'I', b[o:o + 4])[0]
    out, ifd, seen = [], u32(4), set()
    while ifd and ifd not in seen and ifd < len(b):
        seen.add(ifd)
        n = u16(ifd)
        tags = {u16(ifd + 2 + 12 * i): u32(ifd + 2 + 12 * i + 8) for i in range(n)}
        off, ln = tags.get(0x111) or tags.get(0x201), tags.get(0x117) or tags.get(0x202)
        if off and ln:
            out.append((off, ln))
        ifd = u32(ifd + 2 + 12 * n)
    return out


def preview(path):
    b = open(path, 'rb').read()
    for off, ln in sorted(tiff_offsets(b), key=lambda x: -x[1]):
        if b[off:off + 2] != b'\xff\xd8':
            continue
        try:
            im = Image.open(io.BytesIO(b[off:off + ln]))
            im.load()
            return im
        except Exception:
            continue
    raise SystemExit('no preview in ' + path)


def main():
    out = os.path.join(RAW, PHOTOS)
    os.makedirs(out, exist_ok=True)
    for n, box in sorted(BOXES.items()):
        im = preview(os.path.join(UNIT_FOLDER, 'IMG_%d.CR2' % n)).convert('RGB')
        assert im.size == (5184, 3456), im.size
        im.crop(box).save(os.path.join(out, 'IMG_%d.jpg' % n), quality=93)
    print(len(BOXES), 'photos cut to the notebook in', out)


if __name__ == '__main__':
    main()
