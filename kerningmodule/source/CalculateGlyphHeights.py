#!/usr/bin/env python3
# Author: Sayed Zeeshan Asghar
# Ver 0.1
# Description: Calculate the top and bottom heights for glyphs for horizontal shifts of dX pixels 
import os
import cv2 as cv
import glob
import numpy as np
import matplotlib as plt

nBins = 11
minHeight = 710
maxHeight = 780
shiftX = 200
scaling = 5
DESC_RATE = 0.2
ASC_RATE_1 = 4.0
ASC_RATE_2 = 8.0
nPixelScan = 9
dXValid = [10,20,40,50,100]
LookUp = {} #instantiate an empty dictionary
def CalculateGlyphHeights(baseDir,dX,debugArgs):
    if dX not in dXValid:
        print("dX value is not correct. It should be one of the folowing values: ")
        print(dXValid)
        print("Program exiting now")
        return 0
    numGlyphs = 0
    haroofDir = baseDir+"/Haroof_Regular/"
    ligatureDir = baseDir+"/Ligatures_Regular/"
    symbolDir = baseDir+"/Symbols/"
    kasheedaDir = baseDir+"/Ligatures_Kashida/"
    kasheedaHaroofDir = baseDir+"/Haroof_Kashida/"
    for filepath in glob.iglob(ligatureDir + '**/*.png', recursive=True):
        filename = os.path.basename(filepath)
        print(filename)
        im = cv.imread(filepath, cv.IMREAD_GRAYSCALE)
        H, W = im.shape
        if H < minHeight or H > maxHeight:
            print("Image height should be between "+str(minHeight)+" pixels and "+str(maxHeight)+" pixels.")
            print("Program exiting now")
            return 0
        numGlyphs += 1
        nbinsTemp = nBins*dX
        shiftXTemp = shiftX/dX
        divisor = int(np.floor(shiftXTemp/scaling))
        nW = int(np.floor((W-nPixelScan)/divisor) + 1)
        
        if nW > nbinsTemp:
            nW = nbinsTemp
       
        starting = np.ones((H,nW),dtype=np.int8) #bottom
        ending = np.ones((H,nW),dtype=np.int8) #top 
        start_h = np.zeros((nbinsTemp,),dtype=int)
        end_h = np.fix(H*0.5)*np.ones((nbinsTemp,),dtype=int)
        extents = np.zeros((nBins,2),dtype=int)
        for j in range(0,nW):
            for i in range(0,nPixelScan):
                starting[0:H,j] = starting[0:H,j] & im[0:H,W - j*divisor - i - 1]
                ending[0:H,j] = ending[0:H,j] & im[0:H,i + j*divisor]

        for j in range(0,nW):
            a  = np.argwhere(starting[0:H,j] == 0)
            if not a.any():
                start_h[j] = -1
                end_h[j] = -1
            else:
                start_h[j] = a[-1]
                end_h[j] = a[1]
                start_h[j] = H - start_h[j]
                end_h[j] = H - end_h[j]
        
        hmax = start_h[0]
        for k in range(1,nbinsTemp):
            if start_h[k] > hmax:
                start_h[k] = hmax
            else:
                hmax = start_h[k]

        if nW < 61:
            rate = ASC_RATE_2
        else:
            rate = ASC_RATE_1

        hmax = start_h[nW-1]
        for k in range(nW,nbinsTemp):
            if(hmax - (k-nW)*DESC_RATE < 0):
                start_h[k] = 0
            else:
                start_h[k] = int(hmax - (k-nW)*DESC_RATE)

        hmin = end_h[0]
        for k in range(1,nbinsTemp):
            if end_h[k] < hmin:
                end_h[k] = hmin
            else:
                hmin = end_h[k]

        hmin = end_h[nW-1]
        for k in range(nW,nbinsTemp):
            if(hmin - (k-nW)*rate > H):
                end_h[k] = 0
            else:
                end_h[k] = int(hmin + (k-nW)*rate)
        extents[0:nW,0] = start_h[0::dX]
        extents[0:nW,1] = end_h[0::dX]

        LookUp[filename[0:-4]] = extents
    print("All glyphs processed successfully")
    return LookUp

def removeNumbers(name):
    print("to be implemented")
