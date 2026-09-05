import os
from fontforge import *

font = open(os.sys.argv[1])
for glyph in font:
    if font[glyph].isWorthOutputting():
        font[glyph].export("exp/" + font[glyph].glyphname + ".png")
