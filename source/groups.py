#create groups based on collisions and glyph heights
import numpy as np
import os
nCols = 10
nRows = 10

shifts = [150, 175, 175, 175, 175, 200, 200, 200, 200, 200]
left_threshold = [100, 100, 100, 100, 100, 100, 50, 50, 50, 100]
right_threshold = [200, 200, 200, 200, 200, 200, 200, 200, 150, 100]
HeighAdjustment = [0,-200,-100,-100,-50,-20,-20,0,0,-50]; # should always be non-positive
weights = [0.6,0.25,0.15] #must sum up to 1.0
def form_groups_from_tables(Keys,Lookup,LeftTable,RightTable,LeftList,RightList):
    lu_len = len(Lookup)
    #exception handling

    #table sorting
    LeftTable =  LeftTable[LeftTable[:,0].argsort(),]
    RightTable =  RightTable[RightTable[:,0].argsort(),]

    #thresholding operation to prune collisions results
    for j in range(0,nCols):
        for i in range(0,lu_len):
            if(RightList[i,j] > right_threshold[j]):
                RightList[i,j] = 1
            else:
                RightList[i,j] = 0
            if(LeftList[i,j] > left_threshold[j]):
                LeftList[i,j] = 1
            else:
                LeftList[i,j] = 0
    # cleaning up thresholded data
    for j in range(nCols-1,0,-1):
        for i in range(0,lu_len):
            if RightList[i,j] == 1:
                count = 0
                for k in range(0,j):
                    if RightList[i,k] == 1:
                        count = count + 1
                if(count/j > 0.9):
                    for k in range(0,j):
                        RightList[i,k] = 1
                else:
                    RightList[i,j] = 0
    for j in range(nCols-1,0,-1):
        for i in range(0,lu_len):
            if LeftList[i,j] == 1:
                count = 0
                for k in range(0,j):
                    if LeftList[i,k] == 1:
                        count = count + 1
                if(count/j > 0.9):
                    for k in range(0,j):
                        LeftList[i,k] = 1
                else:
                    LeftList[i,j] = 0

    RTable = {}
    LTable = {}
    #list formation for each value of shift
    for j in range(0,nCols):
        RTable[j] = []
        for i in range(0,lu_len):
            if RightList[i,j] == 1:
                RTable[j].append(i)
    for j in range(0,nCols):
        LTable[j] = []
        for i in range(0,lu_len):
            if LeftList[i,j] == 1:
                LTable[j].append(i)

    LMaster = {}
    RMaster = {}
    #left master table formation
    for j  in range(0,nCols):
        L0 = len(LTable[j])
        TLst = np.zeros(shape=(L0,2),dtype=int)
        for i in range(0,L0):
            TLst[i,0] = LTable[j][i]
            TLst[i,1] = LeftTable[LTable[j][i],j+2]
        LMaster[j]=np.flipud(TLst[TLst[:,1].argsort(),])

    #right master table formation
    for j  in range(0,nCols):
        L0 = len(RTable[j])
        TLst = np.zeros(shape=(L0,3),dtype=int)
        for i in range(0,L0):
            TLst[i,0] = RTable[j][i]
            TLst[i,1] = RightTable[RTable[j][i],j+2]*weights[0] + \
            RightTable[RTable[j][i],3]*weights[1] + \
            RightTable[RTable[j][i],4]*weights[2]
            TLst[i,2] = RightTable[RTable[j][i],j+2]
        RMaster[j]=np.flipud(TLst[TLst[:,1].argsort(),])

    cushion = np.zeros(shape=(10,1),dtype=int)
    for j in range(0,nCols):
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
        indL[0,k] = 0

    for j in range(0,nRows-1):
        for k in range(0,nCols):
            a  = np.argwhere(RMaster[k][:,1] < thresh[j,k]) 
            if a.any():
                indR[j+1,k] = a[0]
    for k  in range(0,nCols):
        indR[nRows,k] = len(RMaster[k])
        indR[0,k] = 0

    LeftGroups = {}
    RightGroups = {}
    #file writing
    file = open('C:\kerning\kern_groups.vtg','w')
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
    file = open('C:/kerning/blank_kerning_groups.vtl','w')
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
                        file.write('\rDEF_LOOKUP "'+fn+'"  PROCESS_BASE PROCESS_MARKS ALL DIRECTION RTL')
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

    print("ok")
    #thresholding

def remove_numbers(name):
    return name.replace("_1","").replace("_2","") \
    .replace("_3","").replace("_4","").replace("_5","")