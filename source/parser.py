import os
import pathlib
import source.groups as gp
import source.heights as ht
import re
kasheeda = -1
initialized = 0
base_dir = []
shft = []
rt_th = []
lt_th = []
exstr = []
prof = []
adj = []
def parse_settings_file(file_path):
    count = 0
    exstring = ""
    profile = []
    adjustment = []
    path = os.path.join(pathlib.Path(__file__).parent.resolve(),file_path)
    with open(path) as file_in:
        for line in file_in:
            stripped = line.strip()
            if len(stripped) > 0:
                if stripped[0] != '#': #ignore comments
                    split = stripped.split()
                    if split[0] == "GLYPH_DIR_LOC":
                        if count == 0:
                            base_dir.append(split[1])
                            count += 1
                        else:
                            print("parse error, settings.font file is in incorrect format")
                            return 0
                    if split[0] == "FONT_TYPE":
                        if count == 1:
                            count += 1
                            if(split[1] == 'REGULAR'):
                                kasheeda = 0
                            elif(split[1] == 'KASHEEDA'):
                                kasheeda = 1
                        else:
                            print("parse error, settings.font file is in incorrect format")
                            return 0
                    if split[0] == "HORIZONTAL_SHIFTS":
                        if count == 2:
                            count += 1
                            splitHash = stripped.split("#")
                            text = splitHash[0]
                            text = text[text.find("[")+1 : text.find("]")]
                            shifts = [int(s.strip()) for s in text.split(",") if s.strip().isdigit()]
                            if len(shifts) == 10:
                                shft.append(shifts)
                            else:
                                print("parse error, settings.font file (HORIZONTAL_SHIFTS) is in incorrect format")
                                return 0
                        else:
                            print("parse error, settings.font file is in incorrect format")
                            return 0

                    if split[0] == "LEFT_COLLISION_THRESHOLDS":
                        if count == 3:
                            count += 1
                            splitHash = stripped.split("#")
                            text = splitHash[0]
                            text = text[text.find("[")+1 : text.find("]")]
                            left_th = [int(s.strip()) for s in text.split(",") if s.strip().isdigit()]
                            if len(left_th) == 10:
                                lt_th.append(left_th)
                            else:
                                print("parse error, settings.font file (LEFT_COLLISION_THRESHOLDS) is in incorrect format")
                                return 0
                        else:
                            print("parse error, settings.font file is in incorrect format")
                            return 0

                    if split[0] == "RIGHT_COLLISION_THRESHOLDS":
                        if count == 4:
                            count += 1
                            splitHash = stripped.split("#")
                            text = splitHash[0]
                            text = text[text.find("[")+1 : text.find("]")]
                            right_th = [int(s.strip()) for s in text.split(",") if s.strip().isdigit()]
                            if len(right_th) == 10:
                                rt_th.append(right_th)
                            else:
                                print("parse error, settings.font file (RIGHT_COLLISION_THRESHOLDS) is in incorrect format")
                                return 0
                        else:
                            print("parse error, settings.font file is in incorrect format")
                            return 0

                    if split[0] == "EXCEPTION_STRING":
                        if (count-5)%3 == 0:
                            count += 1
                            text = split[1].strip()
                            exstr.append(text)
                        else:
                            print("parse error, settings.font file is in incorrect format")
                            return 0
                    if split[0] == "EXCEPTION_PROFILE":
                        if (count-6)%3 == 0:
                            count += 1
                            splitHash = stripped.split("#")
                            text = splitHash[0]
                            text = text[text.find("[")+1 : text.find("]")]
                            profile = [int(s.strip()) for s in text.split(",") if s.strip().isdigit()]
                            if len(profile) != 10:
                                print("parse error, settings.font file (EXCEPTION_PROFILE) is in incorrect format")
                                return 0
                            else:
                                prof.append(profile)
                        else:
                            print("parse error, settings.font file is in incorrect format")
                            return 0

                    if split[0] == "EXCEPTION_ADJUSTMENT":
                        if (count-7)%3 == 0:
                            count += 1
                            splitHash = stripped.split("#")
                            text = splitHash[0]
                            text = text[text.find("[")+1 : text.find("]")]
                            adjustment = []
                            for i, value in enumerate(text.split(',')):
                                try:
                                    adjustment.append(int(value))
                                except ValueError:
                                    pass  # not an integer
                            if len(adjustment) != 10:
                                print("parse error, settings.font file (EXCEPTION_ADJUSTMENT) is in incorrect format")
                                return 0
                            else:
                                adj.append(adjustment)
                        else:
                            print("parse error, settings.font file is in incorrect format")
                            return 0
    if(count > 4):                        
        print("successfully parsed settings.txt file")
        initialized = 1
        return 1
    else:
        print("parsed settings file with errors. exiting now")
        initialized = 0
        return 0