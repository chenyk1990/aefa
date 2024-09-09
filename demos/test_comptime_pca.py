##########################################################################################
## Compare the training time between raw data and PCA-reduced data
##########################################################################################

from sklearn.decomposition import PCA
import warnings
warnings.simplefilter("ignore")

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import joblib

import numpy as np
import os
# import h5py
from aefa import get_label,get_traindata
from aefa import asciiwrite

aefapath=os.getenv('HOME')+'/DATALIB/AEFA.h5'

##########################################################################################
#### Get training labels (earthquake occurence)
##########################################################################################



import time

tic = time.perf_counter()
toc = time.perf_counter()
print(f"The time is {toc - tic:0.4f} seconds");

##########################################################################################
## Training
##########################################################################################
ista='EM_101'
labclass=get_label(aefapath)
dataEM=get_traindata(ista,aefapath)

## Prepare for RF
ix = int(len(dataEM)*0.9)
labclass = np.array(labclass)  
data1 = np.reshape(dataEM,(204,1008,51))
data2 = data1[1:-1,:,:] 
data2 = np.reshape(data2,(data2.shape[0],data2.shape[1]*data2.shape[2]))

inputdata=data2
inputlabel=labclass[2:]
regrEM = RandomForestClassifier(n_estimators=1000, ccp_alpha=0.001,oob_score=True,criterion='gini',random_state=123456)
ix = int(len(data2)*0.9)

## count time
tic = time.perf_counter()
regrEM.fit(inputdata[0:ix],inputlabel[0:ix])  
toc = time.perf_counter()
print(f"Raw data take {toc - tic:0.4f} seconds");

## PCA preparation
inputdata=[]
data2 = data1[1:-1,:,:] 
for ii in range(data2.shape[0]):
	pca = PCA(n_components=51)
	data2pca = []
	pca.fit(np.transpose(data2[ii,:,:]))
	
	data2pca.append(pca.singular_values_)
	data22 = np.array(data2pca)
	data22 = np.concatenate([data22[0,:]], axis=-1)
	inputdata.append(data22)
inputdata=np.array(inputdata)

## count time
tic = time.perf_counter()
regrEM.fit(inputdata[0:ix],inputlabel[0:ix])  
toc = time.perf_counter()
print(f"PCA data take {toc - tic:0.4f} seconds");
















