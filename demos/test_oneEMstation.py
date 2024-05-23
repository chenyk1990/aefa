from obspy.core.utcdatetime import UTCDateTime
import numpy as np

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
# print(tweek)

##########################################################################################
##extract info from h5 file
##########################################################################################
import h5py
f = h5py.File("AEFA.h5", 'r')
keys=list(f.keys())
# id=2 #event NO
keys=[ii for ii in keys if ii[0:2]=='EV']

#sort
def myFunc(e):
  return int(e[3:])
keys.sort(key=myFunc)

# idx=keys[0]
# dataset = f.get(idx)
# print('AEFA event attributes are:',dataset.attrs.keys())
# print('longitude=%g,latitude=%g,magnitude=%g,time=%s,week=%d'%(dataset.attrs['ev_longitude'],dataset.attrs['ev_latitude'],dataset.attrs['ev_magnitude'],dataset.attrs['ev_time'],dataset.attrs['ev_week']))
# 

##########################################################################################
##extract event info (longitude,latitude,magnitude)
##########################################################################################
tweek_lab=np.zeros_like(tweek)
Longall=[]
Latall=[]
magall=[]
for s in range(3,len(keys)):
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

tweek_lab, len(tweek)

len(tweek_lab), int(tweek[2]-t0)/(10*60), int(tweek[3]-t0)/(10*60)

tweek_lab1 = tweek_lab[1:]
# np.save('labelEvent.npy',tweek_lab1)

##########################################################################################
#### select one station (given station number), EM is given as an example
##########################################################################################
ista=106 #ACC:0.5714285714285714
ista=193 #ACC:0.7619047619047619
dataset = f.get('EM_%d'%ista)
print('It has these datasets',dataset.keys())
dataset['data']
dataset['time']
dataset['timeindex']

if 1:

    data=dataset['data']
    data19=[]
    for i in range(1,len(tweek_lab)):

        a = int(tweek[i-1]-t0)/(10*60)
        b = int(tweek[i]-t0)/(10*60)

        dataE = data[int(a):int(b)]
        dataE = np.reshape(dataE,(dataE.shape[0]*dataE.shape[1]))

        data19.append(dataE)
data19=np.array(data19)

##########################################################################################
## Training
##########################################################################################
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import joblib

lab=tweek_lab1
labclass = np.zeros((len(lab)))
cc=0
for i in lab:
    if i>0:
        labclass[cc]=1
    cc = cc+1
labclass = np.array(labclass)    
outall = []
accall = []
if 1:
    
    dataEM = data19
    dataEM = np.array(dataEM)


    ix = int(len(dataEM)*0.9)
    labclass = np.array(labclass)  

    data1 = np.reshape(dataEM,(203,1008,51))
    data2 = data1[1:,:,25:40]	#These two are different
#     data2 = data1[1:,:,:] 		#These two are different
    
    data2 = np.reshape(data2,(data2.shape[0],data2.shape[1]*data2.shape[2]))
    labclass1 = np.reshape(labclass,(labclass.shape[0],1))
    lab1 = np.reshape(lab,(lab.shape[0],1))

    data2 = np.concatenate([data2,lab1[0:-1]], axis=-1)
    labclassx = labclass[1:]
    labx = lab[1:]


    data3=data2
    labclass3=labclassx
    regrEM = RandomForestClassifier(n_estimators=1000, ccp_alpha=0.001,oob_score=True,criterion='gini',random_state=123456)
    ix = int(len(data2)*0.9)
    regrEM.fit(data3[0:ix],labclass3[0:ix])  
    filename='RFmodel.sav'
    joblib.dump(regrEM, filename)


    # test
    regrEM = joblib.load(filename)
    outtestEM = regrEM.predict(data3[ix:])
    dif = outtestEM - labclass3[ix:]
    acc = len(np.where(dif==0)[0])/len(dif)
    print(acc)
    accall.append(acc)
    outall.append(outtestEM)
    

















