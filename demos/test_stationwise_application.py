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

labclass=get_label(aefapath)[1:]

f = h5py.File(aefapath, 'r')
keys=list(f.keys())
keys=[ii for ii in keys if ii[0:2]=='WK']
idx=keys[0]

keys=keys[1:]
for idx in keys:
	dataset = f.get(idx)
# print('AEFA event attributes are:',dataset.keys())

	keywords=list(f.get(idx).keys())

	ems=[ii for ii in keywords if ii[0:2]=='EM']
	
# ista=106 #ACC:0.5714285714285714
# ista=193 #ACC:0.7619047619047619

##########################################################################################
## Training
##########################################################################################

outall = []
accall = []

if os.path.isdir('./firstmodels') == False:  
	os.makedirs('./firstmodels',exist_ok=True)

keywords=list(f.keys())
ems=[ii for ii in keywords if ii[0:2]=='EM']
gas=[ii for ii in keywords if ii[0:2]=='GA']

from aefa import get_testdata,get_testlabel

ic=0

labclass=get_testlabel()
print(labclass)
# for ista in ems+gas:
accall=[]
outall=[]
# ems=['EM_105']
# ems=[]
# gas=['GA_101']
for ista in ems+gas:
	outtest=[]
# 	filename='./firstmodels/RFmodel_%s.sav'%ista
	filename='./firstmodels/RFmodel_%s.sav'%ista
	for iweek in range(30):		
		try:
			data3=get_testdata(iweek+1,ista,os.getenv('HOME')+"/DATALIB/AEFA.h5")
		except:
			print('ista ',ista,' not available from testing data')
			if ista[0:2]=='EM':
				data3=np.ones([1008,51])
			else:
				data3=np.ones([1008,44])
		
		data3 = np.reshape(data3,(1,data3.shape[0]*data3.shape[1]))
		# test
		regrEM = joblib.load(filename)
		outtestEM = regrEM.predict(data3)
		outtest.append(outtestEM)
	print(outtest)
	
	dif = np.array(outtest).flatten() - np.array(labclass).flatten()
	acc = len(np.where(dif==0)[0])/len(dif)
	print('ista=%s,acc=%g'%(ista,acc))

	accall.append(acc)
	outall.append(outtest)
asciiwrite('accall.txt',accall)
asciiwrite('outall.txt',outall)



	
	
	
	