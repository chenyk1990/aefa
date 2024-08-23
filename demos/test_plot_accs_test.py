

file1='../data/output_test_stationwise_application.txt'
file2='../data/output_test_stationwise_application_pca.txt'

from aefa import asciiread
import numpy as np
import matplotlib.pyplot as plt

lines=asciiread(file1);
lines2=asciiread(file2);

# accs_EM=[float(ii.split(",")[-1].split("=")[1]) for ii in lines if 'EM' in ii and 'acc' in ii]
# accs_GA=[float(ii.split(",")[-1].split("=")[1]) for ii in lines if 'GA' in ii and 'acc' in ii]
# 
# accs_EMPCA=[float(ii.split(",")[-1].split("=")[1]) for ii in lines2 if 'EM' in ii and 'acc' in ii]
# accs_GAPCA=[float(ii.split(",")[-1].split("=")[1]) for ii in lines2 if 'GA' in ii and 'acc' in ii]

accs_EM=[float(ii) for ii in lines[0:158]]
accs_GA=[float(ii) for ii in lines[158:]]

accs_EMPCA=[float(ii) for ii in lines2[0:158]]
accs_GAPCA=[float(ii) for ii in lines2[158:]]

fig = plt.figure(figsize=(6, 8))

plt.subplot(2,1,1)
plt.plot(accs_EM,color='b',linestyle='dashed',label='EM')
plt.plot(accs_EMPCA,color='b',label='EM_PCA')
plt.title('EM accuracy')
plt.gca().legend(loc='lower left')
plt.gca().text(-0.15,1,'(a)',transform=plt.gca().transAxes,size=20,weight='normal')
plt.ylabel('Accuracy')

plt.subplot(2,1,2)
plt.plot(accs_GA,color='g',linestyle='dashed',label='GA')
plt.plot(accs_GAPCA,color='g',label='GA_PCA')
plt.title('GA accuracy')
plt.xlabel('Station NO')
plt.ylabel('Accuracy')

plt.gca().legend(loc='lower left')
plt.gca().text(-0.15,1,'(b)',transform=plt.gca().transAxes,size=20,weight='normal')

plt.savefig('test_plot_accs_test.png',format='png',dpi=300)

plt.show()


print('GA mean accuracy:',np.mean(accs_GA))
print('GA PCA mean accuracy:',np.mean(accs_GAPCA))

print('EM mean accuracy:',np.mean(accs_EM))
print('EM PCA mean accuracy:',np.mean(accs_EMPCA))


print('GA max accuracy:',np.max(accs_GA))
print('GA PCA max accuracy:',np.max(accs_GA))

print('EM max accuracy:',np.max(accs_EM))
print('EM PCA max accuracy:',np.max(accs_EMPCA))

print('GA min accuracy:',np.min(accs_GA))
print('GA PCA min accuracy:',np.min(accs_GA))

print('EM min accuracy:',np.min(accs_EM))
print('EM PCA min accuracy:',np.min(accs_EMPCA))

