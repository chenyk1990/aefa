import numpy as np
def shift3c(data,tshift):
	'''
	shift3c: shift a 3C numpy array according to the tshift (scalar)
	
	INPUT
	data: nsample x 3 array
	tshift: shift in samples (>0 -> right shift; <0 -> left shift)
	
	OUTPUT
	data2: shifted array
	'''
	
# 	return np.roll(data, tshift, axis=0) #not best
	data2=np.zeros(data.shape)
	if tshift>0:
		data2[tshift:,:] = data[0:-tshift,:]
	else:
		data2[0:tshift,:]=data[-tshift:,:]
	
	return data2
	
def asciiread(fname):
	'''
	fname: file name
	din:   a list of lines
	withnewline: if with the newline symbol '\n': True: with; False: without
	
	EXAMPLE
	
	from aefa import asciiread
	import os
	
	lines=asciiread(os.getenv('HOME')+'/chenyk.data2/various/cyksmall/texnet_stations_2022_1019.csv');
	'''
	
	f=open(fname,'r')
	lines=f.readlines()
	lines=[ii.strip() for ii in lines]
	
	return lines

def asciiwrite(fname,din,withnewline=False):
	'''
	fname: file name
	din:   a list of lines
	withnewline: if with the newline symbol '\n': True: with; False: without
	
	EXAMPLE
	
	from aefa import asciiwrite
	import os
	
	f=open(os.getenv('HOME')+'/chenyk.data2/various/cyksmall/texnet_stations_2022_1019.csv')
	lines=f.readlines();
	
	asciiwrite('stations.txt',lines,withnewline=True);
	'''
	
	f=open(fname,'w')
	if withnewline:
		for ii in range(len(din)):
			f.write(str(din[ii]))
	else:
		for ii in range(len(din)):
			f.write(str(din[ii])+"\n")

def get_traindata(station='EM_101',aefapath='./'):
	'''
	get_traindata: get station-wise training data (for 203 weeks, no first week)
	
	EXAMPLE
	from aefa import get_traindata
	import os
	data=get_traindata('EM_101',os.getenv('HOME')+"/DATALIB/AEFA.h5")
	
	'''
	from obspy.core.utcdatetime import UTCDateTime
	import h5py
	import numpy as np

	##########################################################################################
	contime= 8 * 60 *60
	t0 = UTCDateTime(1483200000+contime) 	#begin time: 2017-01-01T00:00:00.000000Z
	tend = UTCDateTime(1606751400+contime) 	#end time: 2020-11-30T23:50:00.000000Z
	t0, tend

	v = int(tend-t0)/(10*60)
	t10min=[]
	c=0
	for cv in range(0,int(v)):
		c =t0 + (cv*10*60)
		t10min.append(c)
	
	v = int(tend-t0)/(7*24*60*60)
	tweek=[]
	c=0
	for cv in range(0,int(v)):
		c =t0 + (cv*7*24*60*60)
		tweek.append(c)
	
	f = h5py.File(aefapath, 'r')

# 	keys=list(f.keys())
# 	# id=2 #event NO
# 	keys=[ii for ii in keys if ii[0:2]=='EV']
# 
# 	#sort
# 	def myFunc(e):
#   		return int(e[3:])
# 	keys.sort(key=myFunc)
# 
# ##########################################################################################
# ##extract event info (longitude,latitude,magnitude)
# ##########################################################################################
# 	tweek_lab=np.zeros_like(tweek)
# 	Longall=[]
# 	Latall=[]
# 	magall=[]
# 	for s in range(3,len(keys)):
# 		dataset = f.get(keys[s])
# 		mag=[]
# 		Lat=[]
# 		Long=[]
# 		b = 0
# 		ind=[]
# 		for q in tweek:
# 			d = UTCDateTime(q)-UTCDateTime(dataset.attrs['ev_time'])
# 			if d>=0:
# 				ind=b-1
# 				tweek_lab[ind]=tweek_lab[ind]+1
	
	dataset = f.get('%s'%station)
	data=np.array(dataset['data'])
	data19=[]
	for i in range(1,204):

		a = int(tweek[i-1]-t0)/(10*60)
		b = int(tweek[i]-t0)/(10*60)

		dataE = data[int(a):int(b)]
		dataE = np.reshape(dataE,(dataE.shape[0]*dataE.shape[1]))

		data19.append(dataE)
	data19=np.array(data19)
	if True in np.isnan(np.isnan(data19)):
		print('Running nan check')
		data19=np.nan_to_num(data19, nan=0, posinf=33333333, neginf=33333333)
	data19=np.nan_to_num(data19, nan=0, posinf=33333333, neginf=33333333)
	
	return data19
	
def get_label(aefapath='./'):
	'''
	get_label: get earthquake occurence label of AEFA
	
	EXAMPLE
	from aefa import get_label
	import os
	label=get_label(os.getenv('HOME')+"/DATALIB/AEFA.h5")
	
	'''
	from obspy.core.utcdatetime import UTCDateTime
	
	##########################################################################################
	## Set up week
	##########################################################################################
	contime= 8 * 60 *60
	t0 = UTCDateTime(1483200000+contime) 	#begin time: 2017-01-01T00:00:00.000000Z
	tend = UTCDateTime(1606751400+contime) 	#end time: 2020-11-30T23:50:00.000000Z
	t0, tend

	v = int(tend-t0)/(10*60)
	t10min=[]
	c=0
	for cv in range(0,int(v)):
		c =t0 + (cv*10*60)
		t10min.append(c)
	
	v = int(tend-t0)/(7*24*60*60)
	tweek=[]
	c=0
	for cv in range(0,int(v)):
		c =t0 + (cv*7*24*60*60)
		tweek.append(c)
	
	import h5py
	f = h5py.File(aefapath, 'r')
	keys=list(f.keys())
	# id=2 #event NO
	keys=[ii for ii in keys if ii[0:2]=='EV']

	#sort
	def myFunc(e):
  		return int(e[3:])
	keys.sort(key=myFunc)

##########################################################################################
##extract event info (longitude,latitude,magnitude)
##########################################################################################
	tweek_lab=np.zeros_like(tweek)
	Longall=[]
	Latall=[]
	magall=[]
	for s in range(0,len(keys)):
		dataset = f.get(keys[s])
		mag=[]
		Lat=[]
		Long=[]
		b = 0
		ind=[]
		for q in tweek:
			d = UTCDateTime(q)-UTCDateTime(dataset.attrs['ev_time'])
			if d>=0:
				ind=b-1
				tweek_lab[ind]=tweek_lab[ind]+1
				mag.append(dataset.attrs['ev_magnitude'])
				Lat.append(dataset.attrs['ev_latitude'])
				Long.append(dataset.attrs['ev_longitude'])
				break
			b = b+1
		magall.append(mag)
		Longall.append(Long)
		Latall.append(Lat)
	
		magweek = np.zeros_like(tweek_lab)
		latweek = np.zeros_like(tweek_lab)
		longweek = np.zeros_like(tweek_lab)

	v = 0
	c = 0
	for i in tweek_lab:
		if i>0:
			magweek[v] = magall[c:c+i]
			latweek[v] = Latall[c:c+i]
			longweek[v] = Longall[c:c+i]
			c = c +i
		else:
			magweek[v]=0
			latweek[v]=0
			longweek[v]=0
		v = v+1
	
	magweek1 = magweek[1:]
	# np.save('magweekLab.npy',magweek1)

	latweek1 = latweek[1:]
	# np.save('latweekLab.npy',latweek1)

	longweek1 = longweek[1:]
	# np.save('longweekLab.npy',longweek1)
	
	len(tweek_lab), int(tweek[2]-t0)/(10*60), int(tweek[3]-t0)/(10*60)

	tweek_lab1 = tweek_lab[1:]

	lab=tweek_lab
	labclass = np.zeros((len(lab)))
	cc=0
	for i in lab:
		if i>0:
			labclass[cc]=1
		cc = cc+1
	labclass = np.array(labclass)	

	return labclass
	
	
def get_time():
	'''
	get_time: get the time axis for AEFA
	
	The length of the time vector is 205920
	The format of time is UTC time format but in local time (CST = UTC + 8 hours)
	
	Written by Yangkang Chen
	Aug, 21, 2024
	
	EXAMPLE
	from aefa import get_time
	times=get_time()
	print(times[0],times[-1])
	
	'''
	from obspy.core.utcdatetime import UTCDateTime
	import numpy as np
	
	##########################################################################################
	## Set up week
	##########################################################################################
	contime= 8 * 60 *60
	t0 = UTCDateTime(1483200000+contime) 	#begin time: 2017-01-01T00:00:00.000000Z
	tend = UTCDateTime(1606751400+contime) 	#end time: 2020-11-30T23:50:00.000000Z
	t0, tend
	
	nsample=204*7*24*6+2*24*6; #205920
	
	timestamps=np.linspace(1483200000+contime,1606751400+contime,nsample);
	
	times=[UTCDateTime(ii) for ii in timestamps]
	
	return times
	
	
def get_testdata(week=1,station='EM_101',aefapath='./'):
	'''
	get_testdata: get station-wise training data (for 203 weeks, no first week)
	
	EXAMPLE:
	
	exe1
	from aefa import get_testdata
	import os
	data=get_testdata(1,'EM_101',os.getenv('HOME')+"/DATALIB/AEFA.h5")

	exe2
	from aefa import get_testdata
	import os
	data=get_testdata(1,'GA_101',os.getenv('HOME')+"/DATALIB/AEFA.h5")
	
	'''
	import h5py
	f = h5py.File(aefapath, 'r')
	idx="WK_%02d"%week
	dataset = f.get(idx)
	print('idx:',idx)
	
	keywords=list(f.get(idx).keys())

	ems=[ii for ii in keywords if ii[0:2]=='EM']
	gas=[ii for ii in keywords if ii[0:2]=='GA']
	
	ems=ems+gas

	# wkno='WK_01'
	allstas=[station]
	for ista in range(len(allstas)):
		print(idx,ista,len(allstas))
	
		emname=[ii for ii in ems if ii.split("_")[0]+'_'+ii.split("_")[-1]==allstas[ista] ]
		
		if len(emname) > 0:
			print(idx,emname)
			data_em=np.array(f.get(idx).get(emname[0])['data'])
			data_em=np.nan_to_num(data_em, nan=0, posinf=33333333, neginf=33333333)
			
# 		ganame=[ii for ii in gas if ii.split("_")[-1]==allstas[ista] ]
# 	
# 		if len(ganame) > 0:
# 			data_ga=np.array(f.get(idx).get(ganame[0])['data'])
# 			print('Max/Min GA values: ',data_ga.max(),data_ga.min())
			
	return data_em


def get_testlabel(aefapath='./',mode='occurence'):
	'''
	get_testlabel: get earthquake occurence label of AEFA for the testing data (30 weeks)
	
	
	mode: occurence, magnitude, location
	
	EXAMPLE:
	from aefa import get_testlabel
	import os
	label=get_testlabel(os.getenv('HOME')+"/DATALIB/AEFA.h5")
	
	'''
	import os,h5py
	
	aefapath=os.getenv('HOME')+'/DATALIB/AEFA.h5'

	f = h5py.File(aefapath, 'r')
	keys=list(f.keys())
	keys=[ii for ii in keys if ii[0:2]=='WK']

	
	labclass=[]
	mags=[]
	lons=[]
	lats=[]
	for ii in range(len(keys)):
		idx=keys[ii]
		keywords=list(f.get(idx).keys())
# 		print(keywords[-1])
		yesno=f.get(idx).get('Label_EV').attrs['yesno']
		
		if yesno=='yes':
			labclass.append(1)
			mags.append(f.get(idx).get('Label_EV').attrs['ev_magnitude'])
			lons.append(f.get(idx).get('Label_EV').attrs['ev_longitude'])
			lats.append(f.get(idx).get('Label_EV').attrs['ev_latitude'])
		else:
			labclass.append(0)
			mags.append(0)
			lons.append(0)
			lats.append(0)

	
	if mode=='occurence':
		return labclass
	elif mode=='magnitude':
		return mags
	elif mode=='location':
		return [(lons[ii],lats[ii]) for ii in range(len(lons))]
	else:
		return labclass
	
	
	
	