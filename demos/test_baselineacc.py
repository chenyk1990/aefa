from aefa import asciiread
import os


from aefa import acc_occurence
yesnoall=asciiread('../data/output_yesnoall_baseline.txt');
yesnoall=[float(ii) for ii in yesnoall]
aefapath=os.getenv('HOME')+"/DATALIB/AEFA.h5"
pre,rec,acc,f1=acc_occurence(yesnoall,aefapath)


from aefa import acc_mag
magall=asciiread('../data/output_magall_baseline.txt')
magall=[float(ii.split(" ")[0].split("]")[0].split("[")[-1]) for ii in magall] #choose the first one

aefapath=os.getenv('HOME')+"/DATALIB/AEFA.h5"
mae=acc_mag(magall,aefapath)


from aefa import acc_loc
locall=asciiread('../data/output_locall_baseline.txt')
locall=[ii.split("]")[0].split("[")[-1] for ii in locall]
mde=acc_loc(locall,aefapath)

