import os
from fontforge import *

font = open(os.sys.argv[1])
outdir = os.sys.argv[2]
export_chars = {"A", "AE", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
                "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W",
                "X", "Y", "Z", }

os.makedirs(outdir, exist_ok=True)
for glyph in font:
    if font[glyph].glyphname in export_chars:
        name = font[glyph].glyphname
        svg = os.path.join(outdir, name + ".svg")
        png = os.path.join(outdir, name + ".png")
        font[glyph].export(svg)
        os.system(f'rsvg-convert -h 500 -o "{png}" "{svg}" && rm -f "{svg}"')
