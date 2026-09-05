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
        font[glyph].export(outdir + "/" + font[glyph].glyphname + ".png")
