

import numpy as np
import pandas as pd
from RF_Utils_newnew import Prediction_Grouping
Mod = './'
# from RF_Utils import Prediction_Grouping
# Mod = 'Models/'

yesnoall = []
locall = []
magall = []
outthreall=[]

pa = '20210404-20210410'
# Mod = './'
WKNO=1
# WKNO=13
# Probability of previous week (Here, week 1).
# prob = [0.55555556,0.70833333,0.7125,0.7,0.625,0.67857143]
# The Main Program for Prediction, Magnitude and Location.


## Put it whereever you like
import os
aefadir=os.getenv('HOME')+"/DATALIB/AEFA.h5"
# aefadir="AEFA.h5"
for WKNO in range(1,31,1):
    if WKNO == 1:
        loc, mag, outthreP = Prediction_Grouping(WKNO,Mod, [0], h5fname=aefadir)
    else:
        
        prob = outthreP
        print('Week'+ str(WKNO)+'prob is',prob)
        loc, mag, outthreP = Prediction_Grouping(WKNO,Mod, prob, h5fname=aefadir)


    if len(loc)==0:
        yesnoall.append(0)
        locall.append(0)
        magall.append(0)
        outthreall.append(outthreP)
    else:

        locall.append(loc)
        magall.append(mag)
        yesnoall.append(1)
        outthreall.append(outthreP)



## Below is for evaluating the accuracy
import h5py
aetalab=[]
f = h5py.File(aefadir, 'r')
for WKNO in range(1,31,1): 
    idx='WK_%02d'%(WKNO)
    g=f.get(idx)
    
    if g.get('Label_EV').attrs['yesno'] == 'yes':
        aetalab.append(1)
    else:
        aetalab.append(0)
    
print('aetalab size is',len(aetalab))
print('yesnoall size is',len(yesnoall))

from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score

accuracy=accuracy_score(aetalab,yesnoall)
f1=f1_score(aetalab,yesnoall)
precision=precision_score(aetalab,yesnoall)
recall=recall_score(aetalab,yesnoall)

print("Precision=",precision)
print("Recall=",recall)
print("Accuracy=",accuracy)
print("F1-score=",f1)


from pylib.io import asciiwrite

## setting an array element with a sequence. The requested array has an inhomogeneous shape after 1 dimensions. The detected shape was (30,) + inhomogeneous part.
# np.save('locall.npy',locall)
# np.save('magall.npy',magall)

asciiwrite('locall_cyk_new.txt',locall)
asciiwrite('magall_cyk_new.txt',magall)
asciiwrite('yesnoall_cyk_new.txt',yesnoall)
asciiwrite('outthreall_cyk_new.txt',outthreall)

np.save('yesnoall_cyk_new.npy',yesnoall)
np.save('outthreall_cyk_new.npy',outthreall)

