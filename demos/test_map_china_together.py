import os
import matplotlib.pyplot as plt

if os.path.isdir('./Fig') == False:  
    os.makedirs('./Fig',exist_ok=True)
    
def plotmap(stas,events,lat1, lat2, lon0, lon1,lon2,lat0,dlat=10.,dlon=20., reso='c', plot=False, plot_filename=None, title=None, ifsta=True,ifcolor=True,iflegend=True):
    '''
    INPUT
    stas: station list
    events: event list
    others are intuitive

    '''
    
    import numpy as np

    from mpl_toolkits.basemap import Basemap

    from obspy.imaging.beachball import beach

    minlat=lat1
    maxlat=lat2
    minlon=lon1
    maxlon=lon2

    m = Basemap(
    projection='cyl', resolution='l',
    llcrnrlon=lon1,llcrnrlat=lat1,urcrnrlon=lon2,urcrnrlat=lat2,lat_1=lat1, lat_2=lat2, lat_0=lat0, lon_1=lon1,lon_2=lon2,lon_0=lon0)

    # read in topo data (on a regular lat/lon grid)
    etopo=np.loadtxt(os.environ["HOME"]+'/chenyk.data/cyk_small_dataset/etopo20data.gz')
    lons=np.loadtxt(os.environ["HOME"]+'/chenyk.data/cyk_small_dataset/etopo20lons.gz')
    lats=np.loadtxt(os.environ["HOME"]+'/chenyk.data/cyk_small_dataset/etopo20lats.gz')

    x, y = m(*np.meshgrid(lons, lats)) #strange here (1081,540)->meshgrid-> [540,1081)
    cs = m.contourf(x,y,etopo,30,cmap=plt.cm.jet)

    if ifcolor==True:
        m.colorbar(location='bottom',pad='10%',label='Elevation (m)')
        
    # add a title.
#     plt.title('AEFA station and event distribution')

    if ifsta: #just for legend
        x_s,y_s=m(stas[0][0],stas[0][1])
        plt.plot(x_s,y_s,'v',color='b',markersize=5)
        x_s,y_s=m(events[0][0],events[0][1])
        plt.plot(x_s,y_s,'*',color='m',markersize=5)
        
    for istation in stas:
        x_s,y_s=m(istation[0],istation[1])
        if ifsta:
            plt.plot(x_s,y_s,'v',color='b',markersize=5)#,label='Stations')
        
    for ievent in events:
        x_s,y_s=m(ievent[0],ievent[1])
        plt.plot(x_s,y_s,'*',color='m',markersize=5)#,label='Events')
        
    if iflegend==True:
        if ifsta:
            plt.legend(['Stations', 'Events'], loc='upper left')
        else:
            plt.legend(['Events'], loc='upper left')
        
#         plt.legend(loc='upper left')
    m.drawcoastlines()
    m.drawcountries()
#     m.fillcontinents()
    m.drawparallels(np.arange(minlat, maxlat+dlat, dlat),labels=[1,1,0,0],fontsize=10)
    m.drawmeridians(np.arange(minlon, maxlon+dlon, dlon),labels=[0,0,1,1],fontsize=10)
    m.drawmapboundary()
#     m.drawmapscale()
    
#     m.etopo()
#     ax = plt.gca()

    if title is not None:
        plt.rcParams['axes.titley'] = 1.04 
        plt.gca().set_title(title)
    
    if plot:
        if plot_filename is not None:
            plt.savefig(plot_filename,format='png',dpi=1000)
#         plt.show()
    else: 
        if plot_filename is None:
#             plt.show()
            pass
        else:
            plt.savefig(plot_filename,format='pdf',dpi=1000)
            

stas=[[80,30],[90,40]]
events=[[80,30],[90,40]]

import h5py
aefapath=os.getenv('HOME')+"/DATALIB/AEFA.h5"
f = h5py.File(aefapath, 'r')
keys=list(f.keys())
keys=[ii for ii in keys if ii[0:2]=='EV']
events=[[f.get(ii).attrs['ev_longitude'],f.get(ii).attrs['ev_latitude']] for ii in keys]
# import matplotlib.pyplot as plt
# lons=[ii[0] for ii in events];lats=[ii[1] for ii in events]
# plt.plot(lons,lats,'*',color='r',markersize=10)
# plt.show()

import h5py
f = h5py.File(aefapath, 'r')
keys=list(f.keys())
keys=[ii for ii in keys if ii[0:2]=='EM']
stations=[[f.get(ii).attrs['sta_longitude'],f.get(ii).attrs['sta_latitude']] for ii in keys]
# import matplotlib.pyplot as plt
# lons=[ii[0] for ii in stations];lats=[ii[1] for ii in stations]
# plt.plot(lons,lats,'v',color='b',markersize=10)
# plt.show()



fig = plt.figure(figsize=(8, 12))
ax=plt.subplot(2,1,1)
plt.gca().text(-0.15,1,'(a)',transform=plt.gca().transAxes,size=20,weight='normal')

plotmap(stations,events,lat1=15.,lat2=55.,dlat=10.,lon1=70.,lon2=140.,dlon=10.,lon0=105., lat0=35, reso='c',plot=True,title='Training data',plot_filename="./Fig/china_regional.png",ifcolor=False,iflegend=True)


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

events2=[[lons[ii],lats[ii]] for ii in range(len(lons))]

ax=plt.subplot(2,1,2)
plt.gca().text(-0.15,1,'(b)',transform=plt.gca().transAxes,size=20,weight='normal')
plotmap(stations,events2,lat1=15.,lat2=55.,dlat=10.,lon1=70.,lon2=140.,dlon=10.,lon0=105., lat0=35, reso='c',plot=True,title='Testing data',ifsta=False,plot_filename="./Fig/china_regional_testing.png",ifcolor=True,iflegend=True)






