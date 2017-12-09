#!/usr/bin/env python

import sys
import numpy as np

nchan = 19
nfft = 256
wlen=int((nfft/2)+1)

ch_list=['Fp1-A2','Fp2-A2','F7-A2','F3-A2','Fpz-A2','F4-A2','F8-A2','T3-A2','C3-A2','Cz-A2','C4-A2','T4-A2','T5-A2','P3-A2','Pz-A2','P4-A2','T6-A2','O1-A2','O2-A2']
ch_list = np.array(ch_list)

def read_mapper_output(file, separator='\t'):
    for line in file:
        #split into key - value
        yield line.rstrip().split(separator)

def main(separator='\t'):
    # input comes from STDIN (standard input)
    # key = [source file name, window #, channel name, sleep stage]
    # value = signal amplitude over time
    # package 'CustomMultiOutputFormat.java' to output to different directories
    # based on the first element of the key
    data = read_mapper_output(sys.stdin, separator=separator)

    for line in data:
        #split key into components
        key,val = line
        src_file,win_no,ch_name,lbl = key.split(',')

        #get signal and perform normalized fourier transform
        sig = np.array(val.split(','),dtype=float)
        freq = (np.abs(np.fft.fft(sig,nfft))[:wlen]**2)/(len(sig)/2)
        #print freq
        s = ('%s,%s,%s,%s%s%f' % (src_file,win_no,ch_name,lbl,separator,freq[0]))
        for p in freq[1:]:
            s += ',%f' % (p)
        print s

        #print stats for this window/channel, where the key will be used to
        #distinguish stats data vs. the feature vectors
        this_max = np.max(freq)
        this_min = np.min(freq)
        this_mean = np.mean(freq)
        this_std = np.std(freq)
        print '%s%s%f,%f,%f,%f' % (ch_name,separator,this_max,this_min,this_mean,this_std)


if __name__ == "__main__":
    main()
