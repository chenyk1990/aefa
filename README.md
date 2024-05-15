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

Google Drive link: https://drive.google.com/drive/folders/1WXVB8ytNB4bOaZ97oq6OmMRyAEg95trp?usp=sharing

	wget /address_TBD/AEFA_20231111.h5
	wget /address_TBD/ID_20231111.npy

-----------
## Examples
Print all keys in AEFA

	import h5py
	f = h5py.File("AEFA.h5", 'r')
	print('AEFA keys are:',f.keys())
	
Print all attributes in AEFA

	import h5py
	f = h5py.File("AEFA.h5", 'r')
	keys=list(f.keys())
	idx=keys[0]
	dataset = f.get(idx)
	print('AEFA attributes are:',dataset.attrs.keys())

Plot EM features of one station in AEFA

	import h5py
	import numpy as np
	import matplotlib.pyplot as plt
	plt.rcParams["figure.figsize"] = (7,8.2)
	
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
	
	ax1 = fig.add_subplot(312)
	plt.plot(data[:,2], 'k',label='Z')
	plt.ylabel('Skewness', fontsize=12) 
	
	ax1 = fig.add_subplot(313)
	plt.plot(data[:,3], 'k',label='Z')
	plt.ylabel('Kurtosis', fontsize=12) 
	plt.xlabel('Sample', fontsize=12) 
	plt.show()
	
Plot GA features of one station in AEFA

	import h5py
	import numpy as np
	import matplotlib.pyplot as plt
	plt.rcParams["figure.figsize"] = (7,8.2)
	
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
	
	ax1 = fig.add_subplot(312)
	plt.plot(data[:,2], 'k',label='Z')
	plt.ylabel('Skewness', fontsize=12) 
	
	ax1 = fig.add_subplot(313)
	plt.plot(data[:,3], 'k',label='Z')
	plt.ylabel('Kurtosis', fontsize=12) 
	plt.xlabel('Sample', fontsize=12) 
	plt.show()
	
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
