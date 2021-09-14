import source.heights as cgh
import source.collisions as col
import source.save_load_obj as slo
import source.groups as gp
import source.parser as ps
import source.ligature_kerning as lk
import time


def haroof_test():
    GlyphHeight  = []
    GlyphHeight.append(1159)
    numGlyphs = cgh.haroof_glyphs("C:/TestKerning/Haroof_Regular/",10,GlyphHeight)
    #assert numGlyphs == 46
def all_glyphs_test():
    LookUp = cgh.calc_glyph_heights("C:/TestKerning",10,0)
    slo.save_obj(LookUp,'GlyphHeightsDictionary')
def plot_test():
    LookUp = slo.load_obj('GlyphHeightsDictionary')
    cgh.plot_glyph_data(LookUp,"C:/TestKerning/Haroof_Regular/dochashmihay.png","dochashmihay")
    cgh.plot_glyph_data(LookUp,"C:/TestKerning/Haroof_Regular/goalhay.png","goalhay")
    cgh.plot_glyph_data(LookUp,"C:/TestKerning/Haroof_Regular/gooltay.png","gooltay")
    cgh.plot_glyph_data(LookUp,"C:/TestKerning/Haroof_Regular/hamzaold.png","hamzaold")
    cgh.plot_glyph_data(LookUp,"C:/TestKerning/Haroof_Regular/ray.png","ray")
    cgh.plot_glyph_data(LookUp,"C:/TestKerning/Haroof_Regular/vao.png","vao")
    cgh.plot_glyph_data(LookUp,"C:/TestKerning/Haroof_Regular/yay.png","yay")
    cgh.plot_glyph_data(LookUp,"C:/TestKerning/Haroof_Regular/zal.png","zal")
    cgh.plot_glyph_data(LookUp,"C:/TestKerning/Haroof_Regular/zay.png","zay")
    cgh.plot_glyph_data(LookUp,"C:/TestKerning/Haroof_Regular/hamzavao.png","hamzavao")




def test_collisions():
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
def test_groups():
    LeftTable = slo.load_obj('LeftTable')
    RightTable =slo.load_obj('RightTable')
    LeftList=slo.load_obj('LeftList')
    RightList= slo.load_obj('RightList')
    LookUp = slo.load_obj('GlyphHeightsDictionary')
    Keys = list(LookUp.keys())

    gp.form_groups_from_tables(Keys,LookUp,LeftTable,RightTable,LeftList,RightList)
def test_groups_exceptions():
    gp.add_exception("r",[4000,4000,4000,1500,1800,2000,2500,4000,4000,4000],\
    [-100,-100,-100,-350,-350,-350,-550,-550,-550,-550])
    # gp.add_exception("alef",[4000,4000,4000,1000,1600,4000,2200,2400,4000,4000],\
    # [-100,-100,-100,-350,-350,-350,-550,-550,-550,-550])

    LeftTable = slo.load_obj('LeftTable')
    RightTable =slo.load_obj('RightTable')
    LeftList=slo.load_obj('LeftList')
    RightList= slo.load_obj('RightList')
    LookUp = slo.load_obj('GlyphHeightsDictionary')
    Keys = list(LookUp.keys())

    gp.form_groups_from_tables(Keys,LookUp,LeftTable,RightTable,LeftList,RightList)
def test_parse():
    ps.parse_settings_file("settings.txt")
def test_stage_1():
    lk.process_stage_1()
def test_stage_2():
    lk.process_stage_2()
def test_stage_3():
    lk.process_stage_3()
def test_stage_complete():
    lk.generate_volt_outputs()







