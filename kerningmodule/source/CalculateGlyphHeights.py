# Author: Sayed Zeeshan Asghar
# Ver 0.1
# Description: Calculate the top and bottom heights for glyphs for horizontal shifts of dX pixels 
import os
import cv2 as cv
#import matplotlib as plt
import glob
import numpy as np

nBins = 11
minHeight = 710
maxHeight = 780
def CalculateGlyphHeights(baseDir,dX,debugArgs):
    numGlyphs = 0
    haroofDir = baseDir+"/Haroof_Regular/"
    ligatureDir = baseDir+"/Ligatures_Regular/"
    symbolDir = baseDir+"/Symbols/"
    kasheedaDir = baseDir+"/Ligatures_Kashida/"
    kasheedaHaroofDir = baseDir+"/Haroof_Kashida/"
    #fig=plt.figure(figsize=(8, 4))
    for filepath in glob.iglob(ligatureDir + '**/*.png', recursive=True):
        filename = os.path.basename(filepath)
        print(filename)
        numGlyphs += 1
        im = cv.imread(filepath, cv.IMREAD_GRAYSCALE)
        H, W = im.shape
        if H < minHeight or H > maxHeight:
            print("Image height should be between "+str(minHeight)+" pixels and "+str(maxHeight)+" pixels.")
            return 0
        #plt.imshow(im, cmap=plt.cm.gray)
        #plt.show()
        
        new_var = input("Press Enter to continue...")
        new_var

def removeNumbers(name):
    print("to be implemented")
