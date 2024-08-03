# AEFA

## Description

**AEFA** An Earthquake Forecasting Dataset for AI

## Reference
	Chen, Y., et al., “AEFA: An Earthquake Forecasting Dataset for AI,” TBD.

    
BibTeX:

	@Article{aefa,
	  author={Yangkang Chen et al.},
	  title = {{AEFA}: An Earthquake Forecasting Dataset for {AI}},
	  journal={TBD},
	  year=2024,
	  volume=1,
	  issue=1,
	  number=1,
	  pages={},
	  doi={},
	}

-----------
## Copyright
    Developers of the AEFA package, 2021-present
-----------

## License
    GNU General Public License, Version 3
    (http://www.gnu.org/copyleft/gpl.html)   

-----------

## Install
Using the latest version

    git clone https://github.com/chenyk1990/aefa

-----------
## Download

https://utexas.box.com/s/gjuwy25mnfql177gninfwn3lh6iq2d7m

-----------
## Examples
Print all keys in AEFA

	import h5py
	f = h5py.File("AEFA.h5", 'r')
	print('AEFA keys are:',f.keys())
	
Print attributes in AEFA

	import h5py
	f = h5py.File("AEFA.h5", 'r')
	keys=list(f.keys())
	idx=keys[0]
	dataset = f.get(idx)
	print('AEFA attributes are:',dataset.attrs.keys())

Print all event attributes in AEFA

	import h5py
	f = h5py.File("AEFA.h5", 'r')
	keys=list(f.keys())
	keys=[ii for ii in keys if ii[0:2]=='EV']
	idx=keys[0]
	dataset = f.get(idx)
	print('AEFA event attributes are:',dataset.attrs.keys())
	
Print event (idth) information in AEFA

	import h5py
	f = h5py.File("AEFA.h5", 'r')
	keys=list(f.keys())
	id=2 #event NO
	keys=[ii for ii in keys if ii=='EV_%d'%id]
	idx=keys[0]
	dataset = f.get(idx)
	print('AEFA event attributes are:',dataset.attrs.keys())
	print('longitude=%g,latitude=%g,magnitude=%g,time=%s,week=%d'%(dataset.attrs['ev_longitude'],dataset.attrs['ev_latitude'],dataset.attrs['ev_magnitude'],dataset.attrs['ev_time'],dataset.attrs['ev_week']))

Plot Events (quickly) of AEFA

	import h5py
	f = h5py.File("AEFA.h5", 'r')
	keys=list(f.keys())
	keys=[ii for ii in keys if ii[0:2]=='EV']
	events=[[f.get(ii).attrs['ev_longitude'],f.get(ii).attrs['ev_latitude']] for ii in keys]
	import matplotlib.pyplot as plt
	lons=[ii[0] for ii in events];lats=[ii[1] for ii in events]
	plt.plot(lons,lats,'*',color='r',markersize=10)
	plt.show()
 
<img src='https://github.com/chenyk1990/gallery/blob/main/aefa/events.png' alt='Slicing' width=500/>

Plot stations (quickly) of AEFA

	import h5py
	f = h5py.File("AEFA.h5", 'r')
	keys=list(f.keys())
	keys=[ii for ii in keys if ii[0:2]=='EM']
	stations=[[f.get(ii).attrs['sta_longitude'],f.get(ii).attrs['sta_latitude']] for ii in keys]
	import matplotlib.pyplot as plt
	lons=[ii[0] for ii in stations];lats=[ii[1] for ii in stations]
	plt.plot(lons,lats,'v',color='b',markersize=10)
	plt.show()
 
<img src='https://github.com/chenyk1990/gallery/blob/main/aefa/stations.png' alt='Slicing' width=500/>

Plot EM features of one station in AEFA

	import h5py
	import numpy as np
	import matplotlib.pyplot as plt
	plt.rcParams["figure.figsize"] = (7,4.2)
	
	f = h5py.File("AEFA.h5", 'r')
	keys=list(f.keys())
	keys=[ii for ii in keys if ii[0:2]=='EM']
	idx=keys[0]
	dataset = f.get(idx)
	data = np.array(dataset['data'])
	fig=plt.figure()
	ax1 = fig.add_subplot(311)
	plt.plot(data[:,0], 'k',label='Z')
	plt.ylabel('Variation', fontsize=12) 
	plt.title('Station: '+idx, fontsize=12) 
	plt.setp(ax1.get_xticklabels(), visible=False)
 
	ax1 = fig.add_subplot(312)
	plt.plot(data[:,2], 'k',label='Z')
	plt.ylabel('Skewness', fontsize=12) 
	plt.setp(ax1.get_xticklabels(), visible=False)
 
	ax1 = fig.add_subplot(313)
	plt.plot(data[:,3], 'k',label='Z')
	plt.ylabel('Kurtosis', fontsize=12) 
	plt.xlabel('Sample', fontsize=12) 
	plt.show()

<img src='https://github.com/chenyk1990/gallery/blob/main/aefa/em101.png' alt='Slicing' width=960/>

Plot GA features of one station in AEFA

	import h5py
	import numpy as np
	import matplotlib.pyplot as plt
	plt.rcParams["figure.figsize"] = (7,4.2)
	
	f = h5py.File("AEFA.h5", 'r')
	keys=list(f.keys())
	keys=[ii for ii in keys if ii[0:2]=='GA']
	idx=keys[0]
	dataset = f.get(idx)
	data = np.array(dataset['data'])
	fig=plt.figure()
	ax1 = fig.add_subplot(311)
	plt.plot(data[:,0], 'k',label='Z')
	plt.ylabel('Variation', fontsize=12) 
	plt.title('Station: '+idx, fontsize=12) 
	plt.setp(ax1.get_xticklabels(), visible=False)
  
	ax1 = fig.add_subplot(312)
	plt.plot(data[:,2], 'k',label='Z')
	plt.ylabel('Skewness', fontsize=12) 
	plt.setp(ax1.get_xticklabels(), visible=False)
  
	ax1 = fig.add_subplot(313)
	plt.plot(data[:,3], 'k',label='Z')
	plt.ylabel('Kurtosis', fontsize=12) 
	plt.xlabel('Sample', fontsize=12) 
	plt.show()

<img src='https://github.com/chenyk1990/gallery/blob/main/aefa/ga101.png' alt='Slicing' width=960/>

-----------
## Development
    The development team welcomes voluntary contributions from any open-source enthusiast. 
    If you want to make contribution to this project, feel free to contact the development team. 

-----------
## Contact
    Regarding any questions, bugs, developments, collaborations, please contact  
    Yangkang Chen
    chenyk2016@gmail.com

-----------
## NOTES:


Each EM station (e.g., EM_101) has a 205920 x 51 array. 
51 indicates 51 EM features detailed in Chen et al. (2025), 205920 indicates (204 weeks + 2 days)'s feature recordings. 
A simple math gives: 205920 = 204*7*24*6 + 2*24*6;
try:

	import h5py;import numpy as np;
	f = h5py.File("AEFA.h5", 'r');
	keys=list(f.keys());keys=[ii for ii in keys if ii=='EM_101'];
	idx=keys[0];dataset = f.get(idx);
	data = np.array(dataset['data']);
	print(data.shape) #(205920, 51);

Similarly, for each GA station (e.g., GA_101) has a 205920 x 44 array. 
44 indicates 44 GA features detailed in Chen et al. (2025), 205920 indicates (204 weeks + 2 days)'s feature recordings. 
A simple math gives: 205920 = 204*7*24*6 + 2*24*6;
try:

	import h5py;import numpy as np;
	f = h5py.File("AEFA.h5", 'r');
	keys=list(f.keys());keys=[ii for ii in keys if ii=='GA_101'];
	idx=keys[0];dataset = f.get(idx);
	data = np.array(dataset['data']);
	print(data.shape) #(205920, 44);

The starting time for the AEFA training data is 2017-01-01T00:00:00.000000Z (Sunday);
the ending time is 2020-11-30T23:50:00.000000Z (Monday); (1430 days in total);
Features are given 0 values if the sensors malfunction at any time sample.

-----------
## Gallery
The gallery figures of the aefa package can be found at
    https://github.com/chenyk1990/gallery/tree/main/aefa

These gallery figures are also presented below. 


<!-- 
A sample signal waveform Generated by [test_signal.py](https://github.com/chenyk1990/aefa/tree/main/demos/test_signal.py)
<img src='https://github.com/chenyk1990/gallery/blob/main/aefa/signal-texnet2023ncwh-PB10.png' alt='Slicing' width=960/>

A sample noise waveform Generated by [test_noise.py](https://github.com/chenyk1990/aefa/tree/main/demos/test_noise.py)
<img src='https://github.com/chenyk1990/gallery/blob/main/aefa/noise-24634-PECS.png' alt='Slicing' width=960/>

Waveforms of an arbitrary TexNet event extracted from AEFA Generated by [test_event.py](https://github.com/chenyk1990/aefa/tree/main/demos/test_event.py)
<img src='https://github.com/chenyk1990/gallery/blob/main/aefa/texnet2020kijr-Z.png' alt='Slicing' width=960/>
 -->
