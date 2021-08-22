# Kerning
A Tool that provides automatic kerning for ligature based OpenType fonts in Microsoft Volt
# Prerequisites
**Development environment**

Latest versions of the following packages are recommended:
 - Python 3
 - NumPy
 - OpenCv
 - Matplotlib
 - Glib

**Glyph setup**

Glyphs should be contained in a base directory (e.g. C:/Ligatures) having the following sub-directories (in PNG format):
- *Ligatures_Regular* This directory contains all the multi character glyph e.g. sbb (سبب), slslo (سلسلہ), etc.
- *Haroof_Regular* This Directory contains all the haroof (alphabets) glyph images in PNG format
- *Symbols* This directory contains all the symbols like parenthesis, period, commas, etc. 
- *Ligatures_Kashida* This directory contains kasheeda (italicised or elongated) glyphs
- *Haroof_Kashida* This directory contains kasheeda alphabets
