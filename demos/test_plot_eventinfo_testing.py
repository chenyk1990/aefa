import h5py
import os
import matplotlib.pyplot as plt
import numpy as np

aefapath=os.getenv('HOME')+'/DATALIB/AEFA.h5'

f = h5py.File(aefapath, 'r')
keys=list(f.keys())
keys=[ii for ii in keys if ii[0:2]=='WK']


mags=[]
lons=[]
lats=[]
weeks=[]
for ii in range(len(keys)):
	idx=keys[ii]
	keywords=list(f.get(idx).keys())
	print(keywords[-1])
	yesno=f.get(idx).get('Label_EV').attrs['yesno']
	if yesno=='yes':
		print('Week with EQs:',idx)
		Neqs=len(f.get(idx).get('Label_EV').keys())
		keys2=list(f.get(idx).get('Label_EV').keys())

		if Neqs==0:
				mags.append(f.get(idx).get('Label_EV').attrs['ev_magnitude'])
				lons.append(f.get(idx).get('Label_EV').attrs['ev_longitude'])
				lats.append(f.get(idx).get('Label_EV').attrs['ev_latitude'])
				weeks.append(f.get(idx).get('Label_EV').attrs['ev_week'])
		else:
			for jj in range(Neqs):
				mags.append(f.get(idx).get('Label_EV').get(keys2[jj]).attrs['ev_magnitude'])
				lons.append(f.get(idx).get('Label_EV').get(keys2[jj]).attrs['ev_longitude'])
				lats.append(f.get(idx).get('Label_EV').get(keys2[jj]).attrs['ev_latitude'])
				weeks.append(f.get(idx).get('Label_EV').get(keys2[jj]).attrs['ev_week'])
	
		
	
# import h5py
# import matplotlib.pyplot as plt
# 
# f = h5py.File("AEFA.h5", 'r')
# idx='WK_01'
# ista='EM_101'
# keywords=list(f.get(idx).keys())
# ems=[ii for ii in keywords if ii[0:2]=='EM']
# gas=[ii for ii in keywords if ii[0:2]=='GA']
# 
# emname=[ii for ii in ems if ii.split("_")[-1]==ista.split("_")[-1] ]
# if len(emname) > 0:
# 	data_em=np.array(f.get(idx).get(emname[0])['data'])
# 	plt.imshow(data_em,clim=(-100,100),cmap='jet',aspect='auto',extent=[0,data_em.shape[1],data_em.shape[0],0])
# 	plt.xlabel('Feature #');plt.ylabel('Sample #');plt.title('%s'%emname[0])
# 	plt.show()
	
	


# mags=[]
# for ii in range(len(keys)):
# 	idx='EV_%d'%(ii+1)
# 	print(idx)
# 	mags.append(f.get(idx).attrs['ev_magnitude'])
# 
# weeks=[]
# for ii in range(len(keys)):
# 	idx='EV_%d'%(ii+1)
# 	print(idx)
# 	weeks.append(f.get(idx).attrs['ev_week'])
# print('Week NO min=',min(weeks),'max=',max(weeks))
# 
# lons=[]
# for ii in range(len(keys)):
# 	idx='EV_%d'%(ii+1)
# 	print(idx)
# 	lons.append(f.get(idx).attrs['ev_longitude'])
# 	
# lats=[]
# for ii in range(len(keys)):
# 	idx='EV_%d'%(ii+1)
# 	print(idx)
# 	lats.append(f.get(idx).attrs['ev_latitude'])	
# 	


eventids=np.linspace(1,len(mags),len(mags));

fig = plt.figure(figsize=(14, 8))
plt.subplot(2,2,1)
plt.plot(eventids,mags,'-o',color='k',markersize=10)
plt.xlabel('Event NO')
plt.ylabel('Magnitude (Ml)')

plt.title('Magnitudes of the testing data')
plt.gca().text(-0.18,1,'(a)',transform=plt.gca().transAxes,size=20,weight='normal')
# plt.gca().text(-0.18,1,'(a)',transform=plt.gca().transAxes,size=20,weight='normal')
# plt.ylabel('Sample')
# plt.colorbar(orientation='vertical',shrink=0.6,label='1:filled/0:empty');

plt.subplot(2,2,2)
# plt.plot(dataem.sum(axis=0),marker='o',color='k')
# plt.plot(weeks)

plt.plot(eventids,weeks,'-o',color='k',markersize=8, alpha=0.3)
plt.xlabel('Event NO');
plt.ylabel('Week NO')
plt.title('Occurence weeks of the testing data')
plt.gca().text(-0.18,1,'(b)',transform=plt.gca().transAxes,size=20,weight='normal')

plt.subplot(2,3,4)
plt.hist(lons,10,label='Longitude distribution',color='b')

plt.gca().set_xlim(xmin=98,xmax=108);
plt.gca().legend(loc='upper right');
plt.gca().set_ylabel("Count",fontsize='large', fontweight='normal')
plt.gca().set_xlabel("Longitude (deg)",fontsize='large', fontweight='normal')
plt.gca().text(-0.18,1,'(c)',transform=plt.gca().transAxes,size=20,weight='normal')

plt.subplot(2,3,5)
plt.hist(lats,10,label='Latitude distribution',color='b')
plt.gca().set_xlim(xmin=22,xmax=34);
plt.gca().legend(loc='upper right');
plt.gca().set_ylabel("Count",fontsize='large', fontweight='normal')
plt.gca().set_xlabel("Latitude (deg)",fontsize='large', fontweight='normal')
plt.gca().text(-0.18,1,'(d)',transform=plt.gca().transAxes,size=20,weight='normal')

plt.subplot(2,3,6)
plt.hist(mags,10,label='Magnitude',color='b')
plt.gca().set_xlim(xmin=2,xmax=8);
plt.gca().legend(loc='upper right');
plt.gca().set_ylabel("Count",fontsize='large', fontweight='normal')
plt.gca().set_xlabel("Magnitude (Ml)",fontsize='large', fontweight='normal')
plt.gca().text(-0.18,1,'(e)',transform=plt.gca().transAxes,size=20,weight='normal')

plt.savefig('test_plot_eventinfo_testing.png',format='png',dpi=300)
plt.show() 







