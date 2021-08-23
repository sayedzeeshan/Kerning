import source.heights as cgh
import save_load_obj as slo

def haroof_test():
    numGlyphs = cgh.haroof_glyphs("C:/Ligatures/Haroof_Regular/",10)
    assert numGlyphs == 46
def all_glyphs_test():
    LookUp = cgh.calc_glyph_heights("C:/Ligatures",20,1)
    slo.save_obj(LookUp,'GlyphHeightsDictionary')