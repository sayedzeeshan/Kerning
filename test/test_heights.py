import source.heights as cgh
import source.collisions as col
import save_load_obj as slo
import numpy as np
import time


def haroof_test():
    numGlyphs = cgh.haroof_glyphs("C:/Ligatures/Haroof_Regular/",10)
    assert numGlyphs == 46
def all_glyphs_test():
    LookUp = cgh.calc_glyph_heights("C:/Ligatures",20,1)
    slo.save_obj(LookUp,'GlyphHeightsDictionary')
def plot_test():
    LookUp = slo.load_obj('GlyphHeightsDictionary')
    cgh.plot_glyph_data(LookUp,"C:/Ligatures/Ligatures_Regular/flsvin.png","flsvin")
    cgh.plot_glyph_data(LookUp,"C:/Ligatures/Haroof_Regular/reh.png","reh")
def test():
    start_time = time.time()
    LookUp = slo.load_obj('GlyphHeightsDictionary')
    Rows = len(LookUp)
    Keys = list(LookUp.keys())
    LeftTable, RightTable, LeftList, RightList = col.collide_glyphs(LookUp,Keys)
    slo.save_obj(LeftTable,'LeftTable')
    slo.save_obj(RightTable,'RightTable')
    slo.save_obj(LeftList,'LeftList')
    slo.save_obj(RightList,'RightList')
    print("--- %s seconds ---" % (time.time() - start_time))

