import numpy as np

ch_list=['Fp1-A2','Fp2-A2','F7-A2','F3-A2','Fpz-A2','F4-A2','F8-A2','T3-A2','C3-A2','Cz-A2','C4-A2','T4-A2','T5-A2','P3-A2','Pz-A2','P4-A2','T6-A2','O1-A2','O2-A2']
ch_list = np.array(ch_list)

f=open('norm_stats.txt','r')
means=np.zeros(len(ch_list))
stds=np.zeros(len(ch_list))
for l in f:
	lsplit = l.rstrip().split(';')
	ch_name,vals = lsplit
	cidx = np.where(ch_list == ch_name)[0][0]
	mean,std=vals.split(',')[2:]
	means[cidx]=float(mean)
	stds[cidx]=float(std)
np.savetxt('means.txt',means)
np.savetxt('stds.txt',stds)
f.close()

