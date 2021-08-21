#!/usr/bin/env python3
import pickle
from kerningmodule.source.CalculateGlyphHeights import CalculateGlyphHeights as CGH
import SaveLoadObjects as SLO

LookUp = CGH("C:/Ligatures",10,0)
SLO.save_obj(LookUp,'GlyphHeightsDictionary')
