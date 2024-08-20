import os
import numpy as np
from obspy.core.utcdatetime import UTCDateTime
import matplotlib.pyplot as plt

		
def framebox(x1,x2,y1,y2,c=None,lw=None):
	'''
	framebox: for drawing a frame box
	
	By Yangkang Chen
	June, 2022
	
	INPUT
	x1,x2,y1,y2: intuitive
	
	EXAMPLE I
	from pyseistr.plot import framebox
	from pyseistr.synthetics import gensyn
	from matplotlib import pyplot as plt
	d=gensyn();
	plt.imshow(d);
	framebox(200,400,200,300);
	plt.show()

	EXAMPLE II
	from pyseistr.plot import framebox
	from pyseistr.synthetics import gensyn
	from matplotlib import pyplot as plt
	d=gensyn();
	plt.imshow(d);
	framebox(200,400,200,300,c='g',lw=4);
	plt.show()
	
	'''
	
	if c is None:
		c='r';
	if lw is None:
		lw=2;

	plt.plot([x1,x2],[y1,y1],linestyle='-',color=c,linewidth=lw);
	plt.plot([x1,x2],[y2,y2],linestyle='-',color=c,linewidth=lw);
	plt.plot([x1,x1],[y1,y2],linestyle='-',color=c,linewidth=lw);
	plt.plot([x2,x2],[y1,y2],linestyle='-',color=c,linewidth=lw);

	
	return
	
t0=UTCDateTime(2017, 1, 1, 0, 0, 0)
t1=UTCDateTime(2017, 1, 1, 0, 10, 0)
sample=int((t1-t0)/(60*10))

aefapath=os.getenv('HOME')+'/DATALIB/AEFA.h5'

#or
import h5py
from obspy.core.utcdatetime import UTCDateTime
f = h5py.File(aefapath, 'r')
keys=list(f.keys())
keys1=[ii for ii in keys if ii[0:2]=='GA'] #GA station names
keys2=[ii for ii in keys if ii[0:2]=='EM'] #EM station names

# numpy array
dataga=np.zeros([30240,len(keys1)])
dataem=np.zeros([30240,len(keys2)])


for iweek in range(1,31,1):
	idx='WK_%02d'%iweek
	print(idx)
	
	keywords=list(f.get(idx).keys())
	
	gas=[ii for ii in keywords if ii[0:2]=='GA']
	
	ic=-1
	for ista in keys1:
		print('ic=',ic)
		ic=ic+1;
		ganame=[ii for ii in gas if ii.split("_")[-1]==ista.split("_")[-1] ]
		if len(ganame)>0:
# 			print('length',len(f.get(idx).get(ganame[0])['timeindex']))
			timeindex=f.get(idx).get(ganame[0])['timeindex']
	
			inds=[int((ii-1616860800)/600) for ii in timeindex]
			dataga[inds,ic]=np.ones(len(inds))


for iweek in range(1,31,1):
	idx='WK_%02d'%iweek
	print(idx)
	
	keywords=list(f.get(idx).keys())
	
	ems=[ii for ii in keywords if ii[0:2]=='EM']
	
	ic=-1
	for ista in keys2:
		print('ic=',ic)
		ic=ic+1;
		emname=[ii for ii in ems if ii.split("_")[-1]==ista.split("_")[-1] ]
		if len(emname)>0:
# 			print('length',len(f.get(idx).get(emname[0])['timeindex']))
			timeindex=f.get(idx).get(emname[0])['timeindex']
	
			inds=[int((ii-1616860800)/600) for ii in timeindex]
			dataem[inds,ic]=np.ones(len(inds))
			
			
fig = plt.figure(figsize=(14, 8))

plt.subplot(2,2,1)
plt.imshow(dataem,cmap=plt.cm.jet,aspect='auto')
plt.title('EM station completeness')
plt.gca().text(-0.15,1,'(a)',transform=plt.gca().transAxes,size=20,weight='normal')
plt.ylabel('Sample')
plt.colorbar(orientation='vertical',shrink=0.6,label='1:filled/0:empty');
framebox(0,157,1008*6,1008*7,'w',2)
plt.gca().set_xlim(xmin=0,xmax=157)

plt.subplot(2,2,2)
plt.plot(dataem.sum(axis=0),marker='o',color='k')
plt.title('Recorded EM samples')
plt.gca().invert_yaxis();
plt.gca().text(-0.15,1,'(b)',transform=plt.gca().transAxes,size=20,weight='normal')

plt.subplot(2,2,3)
plt.imshow(dataga,cmap=plt.cm.jet,aspect='auto')
plt.title('GA station completeness')
plt.xlabel('Station NO')
plt.gca().text(-0.15,1,'(c)',transform=plt.gca().transAxes,size=20,weight='normal')
plt.ylabel('Sample')
plt.colorbar(orientation='vertical',shrink=0.6,label='1:filled/0:empty');
framebox(0,150,1008*6,1008*7,'w',2)
plt.gca().set_xlim(xmin=0,xmax=149)

plt.subplot(2,2,4)
plt.plot(dataga.sum(axis=0),marker='o',color='k')
plt.title('Recorded GA samples')
plt.gca().invert_yaxis();
plt.gca().text(-0.15,1,'(d)',transform=plt.gca().transAxes,size=20,weight='normal')
plt.xlabel('Station NO')
plt.savefig('test_plot_completeness_testing.png',format='png',dpi=300)

plt.show()