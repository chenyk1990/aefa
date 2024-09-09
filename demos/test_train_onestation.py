from sklearn.decomposition import PCA
import warnings
warnings.simplefilter("ignore")

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import joblib

import numpy as np
import os
import h5py
from aefa import get_label,get_traindata
from aefa import asciiwrite

aefapath=os.getenv('HOME')+'/DATALIB/AEFA.h5'

##########################################################################################
#### Get training labels (earthquake occurence)
##########################################################################################

labclass=get_label(aefapath)

f = h5py.File(aefapath, 'r')
keys=list(f.keys())
keys=[ii for ii in keys if ii[0:2]=='WK']
idx=keys[0]

keys=keys[1:]
for idx in keys:
	dataset = f.get(idx)

	keywords=list(f.get(idx).keys())

	ems=[ii for ii in keywords if ii[0:2]=='EM']

##########################################################################################
## Training
##########################################################################################
outall = []
accall = []

from pylib.io import asciiwrite
if os.path.isdir('./firstmodels') == False:  
	os.makedirs('./firstmodels',exist_ok=True)

keywords=list(f.keys())
ems=[ii for ii in keywords if ii[0:2]=='EM']
gas=[ii for ii in keywords if ii[0:2]=='GA']

# ems=ems[0:2]
# ems=['EM_193','EM_106']
# # gas=gas[0:2]
# # ems=[]
# gas=['GA_101']

gas=['GA_101']
gas=['EM_193']
ic=0
for ista in gas:
	ic=ic+1;
	print('ista=%s, ic=%d/%d'%(ista,ic,len(ems+gas)))
	dataEM=get_traindata(ista,aefapath)

	ix = int(len(dataEM)*0.9)
	labclass = np.array(labclass)  

	if ista[0:2]=='EM':
		data1 = np.reshape(dataEM,(204,1008,51))
	else:
		data1 = np.reshape(dataEM,(204,1008,44))
		
	#The following is to select the Week2-203 for training
	#Correspondingly, the label for EQ occurence is Week3-204 
	#NOTE: Actual EQ label week is one week after the ML label in a forecasting-classification problem

# 	data2 = data1[1:-1,:,25:40]		#These two are different
	data2 = data1[1:-1,:,:] 		#These two are different
	data2 = np.reshape(data2,(data2.shape[0],data2.shape[1]*data2.shape[2]))
	inputlabel = labclass[2:]
	inputdata=data2
	
	regrEM = RandomForestClassifier(n_estimators=1000, ccp_alpha=0.001,oob_score=True,criterion='gini',random_state=123456)
	ix = int(len(data2)*0.9)
	regrEM.fit(inputdata[0:ix],inputlabel[0:ix])  
	filename='./firstmodels/RFmodel_%s.sav'%ista
	joblib.dump(regrEM, filename)

	# test
	regrEM = joblib.load(filename)
	outtestEM = regrEM.predict(inputdata[ix:])
	dif = outtestEM - inputlabel[ix:]
	acc = len(np.where(dif==0)[0])/len(dif)
	print('ista=%s,acc=%g'%(ista,acc))
	accall.append(acc)		 #accuracy
	outall.append(outtestEM) #prediction results
	
asciiwrite('accall.txt',accall)
asciiwrite('outall.txt',outall)














