import kerningmodule.source.CalculateGlyphHeights as CGH
import SaveLoadObjects as SLO

def HaroofHeightTest():
    numGlyphs = CGH.ProcessHaroofGlyphs("C:/Ligatures/Haroof_Regular/",10)
    assert numGlyphs == 46
def AllGlyphsHeighTest():
    LookUp = CGH.CalculateGlyphHeights("C:/Ligatures",10,0)
    SLO.save_obj(LookUp,'GlyphHeightsDictionary')
