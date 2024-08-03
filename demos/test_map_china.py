import os
if os.path.isdir('./Fig') == False:  
	os.makedirs('./Fig',exist_ok=True)
	
def plotmap(stas,events,lat1, lat2, lon0, lon1,lon2,lat0,dlat=10.,dlon=20., reso='c', plot=False, plot_filename=None):
    '''
	INPUT
	stas: station list
	events: event list
	others are intuitive

    '''
    
    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits.basemap import Basemap

    from obspy.imaging.beachball import beach

    minlat=lat1
    maxlat=lat2
    minlon=lon1
    maxlon=lon2

    fig = plt.figure(figsize=(8, 6))
    m = Basemap(
    projection='cyl', resolution='l',
    llcrnrlon=lon1,llcrnrlat=lat1,urcrnrlon=lon2,urcrnrlat=lat2,lat_1=lat1, lat_2=lat2, lat_0=lat0, lon_1=lon1,lon_2=lon2,lon_0=lon0)

    # read in topo data (on a regular lat/lon grid)
    etopo=np.loadtxt(os.environ["HOME"]+'/chenyk.data/cyk_small_dataset/etopo20data.gz')
    lons=np.loadtxt(os.environ["HOME"]+'/chenyk.data/cyk_small_dataset/etopo20lons.gz')
    lats=np.loadtxt(os.environ["HOME"]+'/chenyk.data/cyk_small_dataset/etopo20lats.gz')

    x, y = m(*np.meshgrid(lons, lats)) #strange here (1081,540)->meshgrid-> [540,1081)
    cs = m.contourf(x,y,etopo,30,cmap=plt.cm.jet)

    m.colorbar(location='bottom',pad='10%',label='Elevation (m)')
    # add a title.
#     plt.title('AEFA station and event distribution')

    for ievent in events:
        
        x_s,y_s=m(ievent[0],ievent[1])
        plt.plot(x_s,y_s,'*',color='m',markersize=5)

    for istation in stas:
        x_s,y_s=m(istation[0],istation[1])
        plt.plot(x_s,y_s,'v',color='b',markersize=5)
        
        
    m.drawcoastlines()
    m.drawcountries()
#     m.fillcontinents()
    m.drawparallels(np.arange(minlat, maxlat+dlat, dlat),labels=[1,1,0,0],fontsize=10)
    m.drawmeridians(np.arange(minlon, maxlon+dlon, dlon),labels=[0,0,1,1],fontsize=10)
    m.drawmapboundary()
#     m.drawmapscale()
    
#     m.etopo()
#     ax = plt.gca()

    if plot:
        if plot_filename is not None:
            plt.savefig(plot_filename,format='png',dpi=1000)
        plt.show()
    else: 
        if plot_filename is None:
            plt.show()
        else:
            plt.savefig(plot_filename,format='pdf',dpi=1000)
            

stas=[[80,30],[90,40]]
events=[[80,30],[90,40]]

import h5py
f = h5py.File("AEFA.h5", 'r')
keys=list(f.keys())
keys=[ii for ii in keys if ii[0:2]=='EV']
events=[[f.get(ii).attrs['ev_longitude'],f.get(ii).attrs['ev_latitude']] for ii in keys]
# import matplotlib.pyplot as plt
# lons=[ii[0] for ii in events];lats=[ii[1] for ii in events]
# plt.plot(lons,lats,'*',color='r',markersize=10)
# plt.show()

import h5py
f = h5py.File("AEFA.h5", 'r')
keys=list(f.keys())
keys=[ii for ii in keys if ii[0:2]=='EM']
stations=[[f.get(ii).attrs['sta_longitude'],f.get(ii).attrs['sta_latitude']] for ii in keys]
# import matplotlib.pyplot as plt
# lons=[ii[0] for ii in stations];lats=[ii[1] for ii in stations]
# plt.plot(lons,lats,'v',color='b',markersize=10)
# plt.show()

plotmap(stations,events,lat1=15.,lat2=55.,dlat=10.,lon1=70.,lon2=140.,dlon=10.,lon0=105., lat0=35, reso='c',plot=True,plot_filename="./Fig/china_regional.png")




