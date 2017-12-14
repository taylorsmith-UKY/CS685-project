import numpy as np

n=50

f=open('entropy.txt')
l=f.readline()
_,entropy=l.split(';')
en=np.array(entropy.split(','),dtype=float)
ids = np.argsort(en)[-n:]
np.savetxt(str(n)+'feats.txt',ids,fmt='%d')

