# Kerning
A Tool that provides automatic kerning for ligature based OpenType fonts in Microsoft Volt

There are three stages of the algorithm. 
- The first stage is to process every single glyph image and extract the extents of the strokes in terms of height at several horizontal locations, defined by the variable *dX*
- The second stage of processing is to detect how much collisions a single glyph has for the complete set of glyphs, for a particular shift of the glyph.
- The last stage of processing is to form groups of glyphs based on collision data (output of stage 2) and the glyph height data (output of stage 1) in order to generate volt files (that can be used to implement kerning in OpenType fonts.)
# Prerequisites
**Development environment**

Latest versions of the following packages are recommended:
 - Python 3.6 or higher
 - NumPy
 - OpenCv
 - Matplotlib
 - Glib

**Glyph setup**

Ligatures/Glyphs should be contained in a base directory (e.g. C:/Ligatures) having the following sub-directories (in PNG format):
- *Ligatures_Regular* This directory contains all the multi character glyph e.g. sbb (سبب), slslo (سلسلہ), etc.
- *Haroof_Regular* This Directory contains all the haroof (alphabets) glyph images in PNG format
- *Symbols* This directory contains all the symbols like parenthesis, period, commas, etc. 
- *Ligatures_Kashida* This directory contains kasheeda (italicised or elongated) glyphs
- *Haroof_Kashida* This directory contains kasheeda alphabets

**Assumptions about input images**

We assume that the glyphs are 2048 upm and the PNG Images generated are 300 dpi. This setting roughly gives image height of ~750 pixels. 