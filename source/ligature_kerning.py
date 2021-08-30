import source.heights as cgh
import source.collisions as col
import source.save_load_obj as slo
import source.groups as gp
import source.parser as ps
import time

def process_stage_1():
    if ps.parse_settings_file("settings.txt") == 1:
        LookUp = cgh.calc_glyph_heights(ps.base_dir[0],10,0)
        if len(LookUp) > 0:
            slo.save_obj(LookUp,'GlyphHeightsDictionary')
        else:
            print("Failed to process, no image data found ... exiting now")
    else:
        print("settings read error. unable to proceed further")

def process_stage_2():
    if ps.parse_settings_file("settings.txt") == 1:
        LookUp = slo.load_obj('GlyphHeightsDictionary')
        LeftTable, RightTable, LeftList, RightList = col.collide_glyphs(LookUp)
        slo.save_obj(LeftTable,'LeftTable')
        slo.save_obj(RightTable,'RightTable')
        slo.save_obj(LeftList,'LeftList')
        slo.save_obj(RightList,'RightList')
        if len(LookUp) > 0:
            slo.save_obj(LookUp,'GlyphHeightsDictionary')
        else:
            print("Failed to process, no image data found ... exiting now")
    else:
        print("settings read error. unable to proceed further")
def process_stage_3():
    if ps.parse_settings_file("settings.txt") == 1:
        for count, str in enumerate(ps.exstr):
            gp.add_exception(str,ps.prof[count],ps.adj[count])
        LeftTable = slo.load_obj('LeftTable')
        RightTable =slo.load_obj('RightTable')
        LeftList=slo.load_obj('LeftList')
        RightList= slo.load_obj('RightList')
        LookUp = slo.load_obj('GlyphHeightsDictionary')
        Keys = list(LookUp.keys())

        gp.form_groups_from_tables(Keys,LookUp,LeftTable,RightTable,LeftList,RightList,ps.base_dir[0]+"/kern_groups.vtg",ps.base_dir[0]+"/kern_tables.vtl")
        if len(LookUp) > 0:
                slo.save_obj(LookUp,'GlyphHeightsDictionary')
        else:
                print("Failed to process, no image data found ... exiting now")
    else:
        print("settings read error. unable to proceed further")

def generate_volt_outputs():
    print("Processing started. WARNING: It might take very long (a few hours) to generate output")
    process_stage_1()
    process_stage_2()
    process_stage_3()