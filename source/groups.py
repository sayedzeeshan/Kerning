#create groups based on collisions and glyph heights
import numpy as np
import os
nCols = 10
nRows = 10

shifts = []
left_threshold = []
right_threshold = []
HeighAdjustment = [0,-200,-100,-100,-50,-20,-20,0,0,-50]; # should always be non-positive
weights = [0.8,0.15,0.05] #must sum up to 1.0
exceptions = {} #needs to be populated first before calling form_groups_from_tables function
def form_groups_from_tables(Keys,Lookup,LHeightsData,RHeightsData,LCollisionList,RCollisionList,VTGFilePath,VTLFilePath):
    lu_len = len(Lookup)
    #table sorting
    LHeightsData =  LHeightsData[LHeightsData[:,0].argsort(),]
    RHeightsData =  RHeightsData[RHeightsData[:,0].argsort(),]

    #exception handling
    if len(exceptions) > 0:
        for key, value in exceptions.items():
            for i in range(0,lu_len):
                l = len(key)
                strippedKey = remove_numbers(Keys[i])
                if strippedKey[-l:] == key:
                    f = 0
                    for j in range(0,nCols):
                        if RHeightsData[i,j+1] > value[0][j]:
                            f = 1
                            break
                    if f == 0:
                        for j in range(0,nCols):
                            RHeightsData[i,j] += value[1][j]
                        print("Exception profile applied to %s"%(strippedKey,))        

    #thresholding operation to prune collisions results
    for j in range(0,nCols):
        for i in range(0,lu_len):
            if(RCollisionList[i,j] > right_threshold[j]):
                RCollisionList[i,j] = 1
            else:
                RCollisionList[i,j] = 0
            if(LCollisionList[i,j] > left_threshold[j]):
                LCollisionList[i,j] = 1
            else:
                LCollisionList[i,j] = 0
    # cleaning up thresholded data
    for j in range(nCols-1,0,-1):
        for i in range(0,lu_len):
            if RCollisionList[i,j] == 1:
                count = 0
                for k in range(0,j):
                    if RCollisionList[i,k] == 1:
                        count = count + 1
                if(float(count/float(j)) > 0.9):
                    for k in range(0,j):
                        RCollisionList[i,k] = 1
                else:
                    RCollisionList[i,j] = 0
    for j in range(nCols-1,0,-1):
        for i in range(0,lu_len):
            if LCollisionList[i,j] == 1:
                count = 0
                for k in range(0,j):
                    if LCollisionList[i,k] == 1:
                        count = count + 1
                if(float(count/float(j))> 0.9):
                    for k in range(0,j):
                        LCollisionList[i,k] = 1
                else:
                    LCollisionList[i,j] = 0

    RTable = {}
    LTable = {}
    #list formation for each value of shift
    for j in range(0,nCols):
        RTable[j] = []
        for i in range(0,lu_len):
            if RCollisionList[i,j] == 1:
                RTable[j].append(i)
    for j in range(0,nCols):
        LTable[j] = []
        for i in range(0,lu_len):
            if LCollisionList[i,j] == 1:
                LTable[j].append(i)

    LMaster = {}
    RMaster = {}
    #left master table formation
    for j  in range(0,nCols):
        L0 = len(LTable[j])
        TLst = np.zeros(shape=(L0,2),dtype=int)
        for i in range(0,L0):
            TLst[i,0] = LTable[j][i]
            TLst[i,1] = LHeightsData[LTable[j][i],j+1]
        LMaster[j]=np.flipud(TLst[TLst[:,1].argsort(),])

    #right master table formation
    for j  in range(0,nCols):
        L0 = len(RTable[j])
        TLst = np.zeros(shape=(L0,3),dtype=int)
        for i in range(0,L0):
            TLst[i,0] = RTable[j][i]
            TLst[i,1] = RHeightsData[RTable[j][i],j+1]*weights[0] + \
            RHeightsData[RTable[j][i],3]*weights[1] + \
            RHeightsData[RTable[j][i],4]*weights[2]
            TLst[i,2] = RHeightsData[RTable[j][i],j+2]
        RMaster[j]=np.flipud(TLst[TLst[:,1].argsort(),])

    cushion = np.zeros(shape=(10,1),dtype=int)
    for j in range(0,nCols):
        if RMaster[j][:,1].any():
            cushion[j] =  np.mean(RMaster[j][:,1] - np.mean(RMaster[j][:,2]))

    #height thresholds to form vertical groups
    thresh = np.zeros(shape=(nRows,nCols),dtype=int)
    dT = 0
    for j in range(0,nCols):
        Left = LMaster[j][:,1]
        Right = RMaster[j][:,1]
        if j > 0:
            for k in range(0,nRows):
                thresh[k,j] = thresh[k,j-1] + HeighAdjustment[j]
        else:
            dT = (max(Right) - min(Left))/(nRows-1)
            thresh[0,j] = max(Right)
            for k in range(1,nRows):
                thresh[k,j] = thresh[0,j] - k*dT
    
    indL = -2*np.ones(shape=(nRows+1,nCols),dtype=int)   
    indR = -2*np.ones(shape=(nRows+1,nCols),dtype=int)   
    for j in range(0,nRows-1):
        for k in range(0,nCols):
            a  = np.argwhere(LMaster[k][:,1] < thresh[j,k]) 
            if a.any():
                indL[j+1,k] = a[0]
    for k  in range(0,nCols):
        indL[nRows,k] = len(LMaster[k])
        for j in range(nRows-1,1,-1):
            if indL[j,k] == -2: 
                indL[j,k] = indL[j+1,k]
                indL[j+1,k] = -2
        indL[0,k] = 0

    for j in range(0,nRows-1):
        for k in range(0,nCols):
            a  = np.argwhere(RMaster[k][:,1] < thresh[j,k]) 
            if a.any():
                indR[j,k] = a[0]
    for k  in range(0,nCols):
        indR[nRows,k] = len(RMaster[k])
        for j in range(nRows-1,1,-1):
            if indR[j,k] == -2: 
                indR[j,k] = indR[j+1,k]
                indR[j+1,k] = -2

    LeftGroups = {}
    RightGroups = {}
    #file writing
    file = open(VTGFilePath,'w')
    for j in range(0,nCols):
        if shifts[j] > 0:
            for i in range(0,nRows):
                st = indL[i,j]
                en = indL[i+1,j]
                if st != -2 and en != -2:
                    LeftGroups[(i,j)] = []
                    file.write('\rDEF_GROUP "left'+str((j+1)*100+i+1)+'"\r')
                    file.write(' ENUM ')
                    for k in range(st,en):
                        name = remove_numbers(Keys[LMaster[j][k,0]])
                        file.write('GLYPH "'+name+'" ')
                        LeftGroups[(i,j)].append(name)
                    file.write('END_ENUM\r')
                    file.write('END_GROUP\r')
    for j in range(0,nCols):
        if shifts[j] > 0:
            for i in range(0,nRows):
                if indR[i,j] >= 0:
                    st = indR[i,j]
                    en = indR[i+1,j]
                    if st != -2 and en != -2:
                        RightGroups[(i,j)] = []
                        file.write('\rDEF_GROUP "right'+str((j+1)*100+i+1)+'"\r')
                        file.write(' ENUM ')
                        if(en == -1):
                            en = indR[nRows,j] - 1
                        for k in range(st,en):
                            name = remove_numbers(Keys[RMaster[j][k,0]])
                            file.write('GLYPH "'+name+'" ')
                            RightGroups[(i,j)].append(name)
                        file.write('END_ENUM\r')
                        file.write('END_GROUP\r')
    file.write('END\r')
    file.close()
    print("VOLT file generated: %s"%VTGFilePath)
    file = open(VTLFilePath,'w')
    for j in range(0,nCols): #loop for horizontal shift
        for i in range(0,nRows): #loop for height groups in horizontal shift groups
            if(shifts[j] > 0):
                TT = np.zeros(shape=(nRows+1-i,),dtype=int)
                count = 0
                for m in range(i,nRows):
                    if(indR[m+1,j] > 0 and indR[m,j] != -2):
                        TT[count] = (j+1)*100 + m + 1
                        count = count + 1
                if(count >= 1 and indL[i+1,j] > 0 and indL[i,j] != -2):
                    for t in range(0,count):
                        fn = 'kernblank'+str((j+1)*100 +i+1)+'_'+str(t+1)
                        file.write('\rDEF_LOOKUP "'+fn+'"  PROCESS_BASE SKIP_MARKS DIRECTION RTL')
                        file.write('\rIN_CONTEXT')
                        arg1 = '"right'+str(TT[t])+'"'
                        file.write('\r LEFT GROUP '+arg1)
                        arg1 = '"left'+str((j+1)*100+i+1)+'"'
                        file.write('\r RIGHT GROUP '+arg1)
                        file.write('\rEND_CONTEXT')
                        file.write('\rAS_POSITION')
                        file.write('\rADJUST_SINGLE GROUP "blank" BY POS ADV -'+str(shifts[j])+' END_POS')
                        file.write('\rEND_ADJUST')
                        file.write('\rEND_POSITION')
    file.write('\rEND')
    file.close()
    print("VOLT file generated: %s"%VTLFilePath)
    #thresholding
# remove numbers from glyphs (artifact of windows not differntiating caps and small letter filr names)
def remove_numbers(name):
    return name.replace("_1","").replace("_2","") \
    .replace("_3","").replace("_4","").replace("_5","")
# exceptions could be words ending in some letter and the profile defines the upper boundary to search for these glyph
#adjustments will be applied to the height profile of these glyphs. 
def add_exception(pattern,profile,adjustment):
    if pattern:
        Cp = len(profile)
        Ca = len(adjustment)
        if Cp == nCols and Ca == nCols:
            exceptions[pattern] = [profile, adjustment]
            print("successfully added exception")
        else:
            print("wrong data format for exceptions. expecting a string and two integer lists")