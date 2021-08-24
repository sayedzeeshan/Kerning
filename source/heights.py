#!/usr/bin/env python3
# Author: Sayed Zeeshan Asghar
# Ver 0.1
# Description: Calculate the top and bottom heights for glyphs for horizontal shifts of dX pixels 
import os
import cv2 as cv
import glob
import numpy as np
import matplotlib.pyplot as plt

nBins = 11
minHeight = 710
maxHeight = 780
shiftX = 200
scaling = 4.9 #2048em font assumption 
DESC_RATE = 0.2
ASC_RATE_1 = 4.0
ASC_RATE_2 = 8.0
HAROOF_BOTTOM_DEFAULT = 300
HAROOF_TOP_DEFAULT = 370
HAROOF_TOP_EXCEPTION = 440
SHORT_GLYPH_BOUNDARY = 61
ASC_RATE_EXCEPTION = 4
ASC_RATE_HAROOF = 7
ASC_RATE_DEFAULT_HAROOF = 4
SYMBOL_TOP_DEFAULT = 460
SYMBOL_BOTTOM_DEFAULT = 100
NUM_PIXEL_SCAN = 9
dXValid = [10,20,40,50,100]
LookUp = {} #instantiate an empty dictionary
haroofExceptions = ["alef.png","alefwah"]
animation = "|/-\\"

def calc_glyph_heights(baseDir,dX,enableKasheeda):
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
    numGlyphs += regular_glyphs(ligatureDir,dX)
    print("Number of  glyphs processed: " + str(numGlyphs))
    # regular Haroof processing
    numGlyphs += haroof_glyphs(haroofDir,dX)
    print("Number of glyphs processed: " + str(numGlyphs))
    numGlyphs += symbol_glyphs(symbolDir,dX)
    print("Number of glyphs processed: " + str(numGlyphs))
    if enableKasheeda:
        numGlyphs += regular_glyphs(kasheedaDir,dX)
        print("Number of  glyphs processed: " + str(numGlyphs))
        # regular Haroof processing
        numGlyphs += haroof_glyphs(kasheedaHaroofDir,dX)
        print("Number of glyphs processed: " + str(numGlyphs))

    print("All glyphs processed successfully")
    return LookUp

def remove_numbers(name):
    print("to be implemented")

def regular_glyphs(dir,dX):
     numGlyphs = 0
     idx = 0
     for filepath in glob.iglob(dir + '**/*.png', recursive=True):
        filename = os.path.basename(filepath)
        #print(filename)
        #print('.', end='', flush=True)
        if numGlyphs%10 == 0:
            print(animation[idx % len(animation)], end="\r")
            idx += 1
        if numGlyphs%100 == 0:
            print("%d glyphs processed \n",numGlyphs)
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
        nPixelScan = NUM_PIXEL_SCAN
        nW = int(np.floor((W-nPixelScan)/divisor) + 1)
        if nW < nPixelScan:
            nPixelScan = nW - 2
        
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
            else:
                start_h[j] = a[-1]
                start_h[j] = H - start_h[j]
            a  = np.argwhere(ending[0:H,j] == 0)
            if not a.any():
                end_h[j] = -1
            else:
                end_h[j] = a[1]
                end_h[j] = H - end_h[j]

        
        hmax = start_h[0]
        for k in range(1,nbinsTemp):
            if start_h[k] > hmax:
                start_h[k] = hmax
            else:
                hmax = start_h[k]

        if nW < SHORT_GLYPH_BOUNDARY:
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
        extents[0:nBins,0] = start_h[0::dX]
        extents[0:nBins,1] = end_h[0::dX]

        LookUp[filename[0:-4]] = extents
     return numGlyphs

def haroof_glyphs(dir,dX):
    numGlyphs = 0
    for filepath in glob.iglob(dir + '**/*.png', recursive=True):
        exceptionFlag = 0
        filename = os.path.basename(filepath)
        #print(filename)
        #print('.', end='', flush=True)
        print(animation[numGlyphs % len(animation)], end="\r")

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
        nPixelScan = NUM_PIXEL_SCAN
        nW = int(np.floor((W-nPixelScan)/divisor) + 1)
        
        if nW > nbinsTemp:
            nW = nbinsTemp
       
        starting = np.ones((H,nW),dtype=np.int8) #bottom
        ending = np.ones((H,nW),dtype=np.int8) #top 
        start_h = HAROOF_BOTTOM_DEFAULT*np.ones((nbinsTemp,),dtype=int)
        extents = np.zeros((nBins,2),dtype=int)
        if(filename[0:-4] in haroofExceptions):
            end_h = HAROOF_TOP_EXCEPTION*np.ones((nbinsTemp,),dtype=int)
        else:
            end_h = HAROOF_TOP_DEFAULT*np.ones((nbinsTemp,),dtype=int)

        for j in range(0,nW):
            for i in range(0,nPixelScan):
                starting[0:H,j] = starting[0:H,j] & im[0:H,W - j*divisor - i - 1]
                ending[0:H,j] = ending[0:H,j] & im[0:H,i + j*divisor]

        for j in range(0,nW):
            a  = np.argwhere(starting[0:H,j] == 0)
            if not a.any():
                start_h[j] = -1
            else:
                start_h[j] = a[-1]
                start_h[j] = H - start_h[j]
            a  = np.argwhere(ending[0:H,j] == 0)
            if not a.any():
                end_h[j] = -1
            else:
                end_h[j] = a[1]
                end_h[j] = H - end_h[j]
        
        hmax = start_h[0]
        for k in range(1,nbinsTemp):
            if start_h[k] > hmax:
                start_h[k] = hmax
            else:
                hmax = start_h[k]

        if nW < SHORT_GLYPH_BOUNDARY:
            if exceptionFlag:
                rate = ASC_RATE_EXCEPTION
            else:
                rate = ASC_RATE_HAROOF
        else:
            rate = ASC_RATE_DEFAULT_HAROOF

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
        extents[0:nBins,0] = start_h[0::dX]
        extents[0:nBins,1] = end_h[0::dX]

        LookUp[filename[0:-4]] = extents
    return numGlyphs

def symbol_glyphs(dir,dX):
    numGlyphs = 0
    for filepath in glob.iglob(dir + '**/*.png', recursive=True):
        filename = os.path.basename(filepath)
        #print(filename)
        #print('.', end='', flush=True)
        print(animation[numGlyphs % len(animation)], end="\r")

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
        nPixelScan = NUM_PIXEL_SCAN
        nW = int(np.floor((W-nPixelScan)/divisor) + 1)
        
        if nW > nbinsTemp:
            nW = nbinsTemp
       
        starting = np.ones((H,nW),dtype=np.int8) #bottom
        ending = np.ones((H,nW),dtype=np.int8) #top 
        start_h = SYMBOL_BOTTOM_DEFAULT*np.ones((nbinsTemp,),dtype=int)
        extents = np.zeros((nBins,2),dtype=int)
        end_h = SYMBOL_TOP_DEFAULT*np.ones((nbinsTemp,),dtype=int)

        for j in range(0,nW):
            for i in range(0,nPixelScan):
                starting[0:H,j] = starting[0:H,j] & im[0:H,W - j*divisor - i - 1]
                ending[0:H,j] = ending[0:H,j] & im[0:H,i + j*divisor]

        for j in range(0,nW):
            a  = np.argwhere(starting[0:H,j] == 0)
            if not a.any():
                start_h[j] = -1
            else:
                start_h[j] = a[-1]
                start_h[j] = H - start_h[j]
            a  = np.argwhere(ending[0:H,j] == 0)
            if not a.any():
                end_h[j] = -1
            else:
                end_h[j] = a[1]
                end_h[j] = H - end_h[j]
        
        hmax = start_h[0]
        for k in range(1,nbinsTemp):
            if start_h[k] > hmax:
                start_h[k] = hmax
            else:
                hmax = start_h[k]

        hmin = end_h[0]
        for k in range(1,nbinsTemp):
            if end_h[k] < hmin:
                end_h[k] = hmin
            else:
                hmin = end_h[k]

        extents[0:nBins,0] = start_h[0::dX]
        extents[0:nBins,1] = end_h[0::dX]

        LookUp[filename[0:-4]] = extents
    return numGlyphs
def plot_glyph_data(LookUp,path,glyph):
    img = cv.imread(path, cv.IMREAD_GRAYSCALE)
    H, W = img.shape
    extents = LookUp[glyph]
    plt.imshow(img)
    x = np.arange(0,nBins)*shiftX/scaling
    plt.plot(W-x,H-extents[0:nBins,0],"rd")
    plt.plot(x,H-extents[0:nBins,1],"gd")

    plt.show()
