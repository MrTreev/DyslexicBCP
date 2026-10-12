import builtins
import os
import re
import fontforge
import psMat


def square_viewbox(svg_path):
    with builtins.open(svg_path) as f:
        content = f.read()
    m = re.search(
        r'viewBox="([\d.\-]+) ([\d.\-]+) ([\d.\-]+) ([\d.\-]+)"',
        content,
    )
    if not m:
        return
    x, y, w, h = map(float, m.groups())
    size = max(w, h)
    x -= (size - w) / 2
    y -= (size - h) / 2
    new_vb = f'viewBox="{x} {y} {size} {size}"'
    begin = m.start()
    end = m.end()
    content = content[:begin] + new_vb + content[end:]
    with builtins.open(svg_path, "w") as f:
        f.write(content)


font = fontforge.open(os.sys.argv[1])
outdir = os.sys.argv[2]
# fmt: off
export_chars = {"A", "AE", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
                "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W",
                "X", "Y", "Z", }
# fmt: on

max_y = font.ascent
min_y = -font.descent
for glyph in font:
    g = font[glyph]
    if g.glyphname in export_chars:
        bb = g.boundingBox()
        max_y = max(max_y, bb[3])
        min_y = min(min_y, bb[1])
font.ascent = int(max_y + 20)
font.descent = int(-min_y + 20)

os.makedirs(outdir, exist_ok=True)
target = font.ascent + font.descent

for glyph in font:
    g = font[glyph]
    if g.glyphname not in export_chars:
        continue
    bb = g.boundingBox()
    gw = bb[2] - bb[0]
    gh = bb[3] - bb[1]
    if gw == 0 or gh == 0:
        continue
    scale = target / max(gw, gh)
    cx = (bb[0] + bb[2]) / 2
    cy = (bb[1] + bb[3]) / 2
    g.transform(psMat.translate(-cx, -cy))
    g.transform(psMat.scale(scale))
    g.transform(psMat.translate(0, font.ascent - (bb[3] - cy) * scale))

    name = g.glyphname
    svg = os.path.join(outdir, name + ".svg")
    png = os.path.join(outdir, name + ".png")
    g.export(svg)
    square_viewbox(svg)
    os.system(f'rsvg-convert -h 500 -o "{png}" "{svg}" && rm -f "{svg}"')
