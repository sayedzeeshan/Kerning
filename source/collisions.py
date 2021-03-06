#create left and right Lists based on collision of glyphs for certain
#right-shift of left glyph
import numpy as np
nBins = 11
HC = 50 #Height cushion to make sure the glyphs have some room to fit over each other
def collide_glyphs(LookUp):
    nRows = len(LookUp)
    LeftTable = np.zeros(shape=(nRows,nBins+1),dtype=int)
    RightTable = np.zeros(shape=(nRows,nBins+1),dtype=int)
    LeftList = np.zeros(shape=(nRows,nBins-1),dtype=int)
    RightList = np.zeros(shape=(nRows,nBins-1),dtype=int)
    i = 0
    for key in LookUp.keys():
        extents = LookUp[key]
        LeftTable[i,0] = i
        RightTable[i,0] = i
        for j in range(0,nBins):
            LeftTable[i,j+1] = extents[j,0]
            RightTable[i,j+1] = extents[j,1] + HC
        i += 1
    LeftTable =  np.flipud(LeftTable[LeftTable[:,1].argsort(),])
    RightTable =  RightTable[RightTable[:,1].argsort(),]
    for i in range(0,nRows):
        a  = np.argwhere(RightTable[:,1] < LeftTable[i,1]) 
        if a.any():
            th = a[-1,0]
            pot = RightTable[0:th,:] #all the glyphs that are lower than glyph i for shift 0 in LeftTable
            #these glyphs form a potential subset to search if they are not collisding for shift k
            Wp, Lp = pot.shape
            for j in range(0,Wp):
                for k in range(0,nBins-1):
                    f = 0
                    for t in range(0,k+1):
                        if pot[j,k-t+2] > LeftTable[i,t+2]:
                            f = 1
                            break
                    if f == 0:
                        LeftList[LeftTable[i,0],k] += 1
                        RightList[pot[j,0],k] += 1
        if(i%200 == 1):
            print(" %d glyphs processed (collisions) \n"%i)


    return LeftTable, RightTable, LeftList, RightList




        