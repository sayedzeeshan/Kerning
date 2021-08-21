import kerningmodule.source.CalculateGlyphHeights as CGH
import SaveLoadObjects as SLO

LookUp = CGH.CalculateGlyphHeights("C:/Ligatures",10,0)
SLO.save_obj(LookUp,'GlyphHeightsDictionary')
