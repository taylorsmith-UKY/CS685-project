#!/usr/bin/env python

import sys
import numpy as np

nchan = 19
nfft = 256
wlen=int((nfft/2)+1)

ch_list=np.array(['Fp1-A2','Fp2-A2','F7-A2','F3-A2','Fpz-A2','F4-A2','F8-A2',
		 'T3-A2','C3-A2','Cz-A2','C4-A2','T4-A2','T5-A2',
		 'P3-A2','Pz-A2','P4-A2','T6-A2','O1-A2','O2-A2'])

def read_mapper_output(file, separator='\t'):
    for line in file:
        #split into key - value
        yield line.rstrip().split(separator)

def main(separator='\t'):
    # input comes from STDIN (standard input)
    # key = [source file name, window #, channel name, sleep stage]
    # value = signal amplitude over time
    data = read_mapper_output(sys.stdin, separator=separator)
    ch_max = ch_min = ch_mean = ch_std = np.zeros(nchan,dtype=float)
    ch_counts = np.zeros(nchan,dtype=int)

    for line in data:
        #split key into components
        src_file,win_no,ch_name,lbl = line[0].split(',')
        #get index for the given channel
        cidx = np.where(ch_list == ch_name)[0]
        ch_counts[cidx] += 1

        sig = np.array(line[1].split(','),dtype=float)
        freq = (np.abs(np.fft.fft(sig,nfft))[:wlen]**2)/(len(sig)/2)
        #print freq
        s = ('%s,%s,%s,%s%s%f' % (src_file,win_no,ch_name,lbl,separator,freq[0]))
        for p in freq[1:]:
            s += ',%f' % (p)
        print s

        #aggregate statistics for each channel
        ch_max[cidx] = np.max(ch_max[cidx],np.max(freq))
        ch_min[cidx] = np.max(ch_min[cidx],np.max(freq))
        ch_mean[cidx] = ((ch_counts[cidx]-1)*ch_mean[cidx] + np.mean(freq))/ch_counts[cidx]
        ch_std[cidx] = ((ch_counts[cidx]-1)*ch_std[cidx] + np.std(freq))/ch_counts[cidx]

    #print aggregate values
    for i in range(nchan):
        print '%s%s%f,%f,%f,%f' % (ch_name[i],separator,ch_max[i],ch_min[i],ch_mean[i],ch_std[i])


if __name__ == "__main__":
    main()