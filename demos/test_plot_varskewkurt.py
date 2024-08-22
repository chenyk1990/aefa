from obspy.core.utcdatetime import UTCDateTime
import matplotlib.pyplot as plt
import numpy as np
import h5py,os
aefapath=os.getenv('HOME')+'/DATALIB/AEFA.h5'
f = h5py.File(aefapath, 'r')

t0=UTCDateTime(2017, 1, 1, 0, 0, 0)
keys=list(f.keys())
keys=[ii for ii in keys if ii[0:2]=='EV']
#extract all event samples
samples=[int((float(UTCDateTime(f.get(ii).attrs['ev_time']))-float(t0))/60/10) for ii in keys]
#extract EM features
keys=list(f.keys())
keys=[ii for ii in keys if ii[0:2]=='EM']

ic=0
for idx in keys:
# idx=keys[0]
	ic=ic+1
	print('ic=',ic)
	dataset = f.get(idx)
	data = np.array(dataset['data'])

	plt.rcParams["figure.figsize"] = (7,4.2)
	fig=plt.figure()
	ax1 = fig.add_subplot(311)
	plt.plot(data[:,0], 'k',label='Z')
	plt.ylabel('Variation', fontsize=12) 
	plt.title('Station: '+idx, fontsize=12) 
	plt.setp(ax1.get_xticklabels(), visible=False)
	plt.plot(samples,50*np.ones(len(samples)),'r*')

	ax1 = fig.add_subplot(312)
	plt.plot(data[:,2], 'k',label='Z')
	plt.ylabel('Skewness', fontsize=12) 
	plt.setp(ax1.get_xticklabels(), visible=False)
	plt.plot(samples,1*np.ones(len(samples)),'r*')

	ax1 = fig.add_subplot(313)
	plt.plot(data[:,3], 'k',label='Z')
	plt.plot(samples,50*np.ones(len(samples)),'r*')
	plt.ylabel('Kurtosis', fontsize=12) 
	plt.xlabel('Sample', fontsize=12) 
	plt.savefig(os.getenv('HOME')+'/DATALIB/AEFAWKfigs/'+'threefeatures_%s.png'%idx)
# 	plt.show()
	plt.close()

#extract GA features
keys=list(f.keys())
keys=[ii for ii in keys if ii[0:2]=='GA']
ic=0
for idx in keys:
# idx=keys[0]
	ic=ic+1
	dataset = f.get(idx)
	data = np.array(dataset['data'])

	plt.rcParams["figure.figsize"] = (7,4.2)
	fig=plt.figure()
	ax1 = fig.add_subplot(311)
	plt.plot(data[:,0], 'k',label='Z')
	plt.ylabel('Variation', fontsize=12) 
	plt.title('Station: '+idx, fontsize=12) 
	plt.setp(ax1.get_xticklabels(), visible=False)
	plt.plot(samples,50*np.ones(len(samples)),'r*')

	ax1 = fig.add_subplot(312)
	plt.plot(data[:,2], 'k',label='Z')
	plt.ylabel('Skewness', fontsize=12) 
	plt.setp(ax1.get_xticklabels(), visible=False)
	plt.plot(samples,1*np.ones(len(samples)),'r*')

	ax1 = fig.add_subplot(313)
	plt.plot(data[:,3], 'k',label='Z')
	plt.plot(samples,50*np.ones(len(samples)),'r*')
	plt.ylabel('Kurtosis', fontsize=12) 
	plt.xlabel('Sample', fontsize=12) 
	plt.savefig(os.getenv('HOME')+'/DATALIB/AEFAWKfigs/'+'threefeatures_%s.png'%idx)
# 	plt.show()
	plt.close()

