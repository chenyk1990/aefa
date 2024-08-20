import os
import numpy as np
from obspy.core.utcdatetime import UTCDateTime
import matplotlib.pyplot as plt

t0=UTCDateTime(2017, 1, 1, 0, 0, 0)
t1=UTCDateTime(2017, 1, 1, 0, 10, 0)
sample=int((t1-t0)/(60*10))

aefapath=os.getenv('HOME')+'/DATALIB/AEFA.h5'

#or
import h5py
from obspy.core.utcdatetime import UTCDateTime
f = h5py.File(aefapath, 'r')
t0=UTCDateTime(2017, 1, 1, 0, 0, 0)
keys=list(f.keys())
keys1=[ii for ii in keys if ii[0:2]=='GA']

keys2=[ii for ii in keys if ii[0:2]=='EM']


dataga=np.zeros([30240,len(keys1)])
dataem=np.zeros([30240,len(keys2)])


for iweek in range(1,31,1):
	print(iweek)
	
	idx='WK_%02d'%iweek
	print(idx)
	
	keywords=list(f.get(idx).keys())
	
	ems=[ii for ii in keywords if ii[0:2]=='EM']
	gas=[ii for ii in keywords if ii[0:2]=='GA']

	for ista in keys1:
		emname=[ii for ii in ems if ii.split("_")[-1]==ista.split("_")[-1] ]
		if len(emname)>0:
			print('length',len(f.get(idx).get(emname[0])['timeindex']))


# fig = plt.figure(figsize=(14, 8))
# 
# plt.subplot(2,2,1)
# plt.imshow(dataem,cmap=plt.cm.jet,aspect='auto')
# plt.title('EM station completeness')
# plt.gca().text(-0.15,1,'(a)',transform=plt.gca().transAxes,size=20,weight='normal')
# plt.ylabel('Sample')
# plt.colorbar(orientation='vertical',shrink=0.6,label='1:filled/0:empty');
# 
# plt.subplot(2,2,2)
# plt.plot(dataem.sum(axis=0),marker='o',color='k')
# plt.title('Recorded EM samples')
# plt.gca().invert_yaxis();
# plt.gca().text(-0.15,1,'(b)',transform=plt.gca().transAxes,size=20,weight='normal')
# 
# plt.subplot(2,2,3)
# plt.imshow(dataga,cmap=plt.cm.jet,aspect='auto')
# plt.title('GA station completeness')
# plt.xlabel('Station NO')
# plt.gca().text(-0.15,1,'(c)',transform=plt.gca().transAxes,size=20,weight='normal')
# plt.ylabel('Sample')
# plt.colorbar(orientation='vertical',shrink=0.6,label='1:filled/0:empty');
# 
# plt.subplot(2,2,4)
# plt.plot(dataga.sum(axis=0),marker='o',color='k')
# plt.title('Recorded GA samples')
# plt.gca().invert_yaxis();
# plt.gca().text(-0.15,1,'(d)',transform=plt.gca().transAxes,size=20,weight='normal')
# plt.xlabel('Station NO')
# plt.savefig('test_plot_completeness.png',format='png',dpi=300)
# 
# plt.show()