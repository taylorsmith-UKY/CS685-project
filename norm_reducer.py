#!/usr/bin/env python

import sys
import numpy as np

#Get channel means and stds and calc normalization coefficients
ch_means = np.loadtxt('channel_means.csv')
ch_stds = np.loadtxt('channel_stds.csv')
ch_mins = ch_means - 2*ch_stds
ch_mins(np.where(ch_mins < 0)) = 0
ch_max = ch_means + 2*stds
nchan = 19
npts = 129

ch_list=['Fp1-A2','Fp2-A2','F7-A2','F3-A2','Fpz-A2','F4-A2','F8-A2','T3-A2','C3-A2','Cz-A2','C4-A2','T4-A2','T5-A2','P3-A2','Pz-A2','P4-A2','T6-A2','O1-A2','O2-A2']
ch_list = np.array(ch_list)

def read_mapper_output(file, separator='\t'):
    for line in file:
        #split into key - value
        yield line.rstrip().split(separator)

def main(separator='\t'):
    # input comes from STDIN (standard input)
    # key = [source file name, window #, channel name, sleep stage]
    # value = signal amplitude over frequency
    # package 'CustomMultiOutputFormat.java' to output to different directories
    # based on the first element of the key
    data = read_mapper_output(sys.stdin, separator=separator)
    entropy = np.zeros([nchan,npts],dtype=float)
    cur_file = '01-02-0001'
    cur_win = '1'
    en_order = []
    for line in data:
        #split key into components
        key,val = line.split(separator)
        src_file,win_no,ch_name,lbl = key.split(',')

        #get index for the given channel
        cidx = np.where(ch_list == ch_name)[0]
        if cur_win == 1:
            ch_order.append(cidx)
        sig = np.array(val.split(','),dtype=float)
        norm = (sig - ch_mins[cidx])/(ch_max[cidx]-ch_mins[cidx])

        entropy[cidx,:] -= norm * np.log(norm)

        #if next channel for same window
        if win_no == cur_win:
            for p in norm:
                s += ',%f' % (p)
        else: #new window, print prior and initialize new string
            print s
            cur_win = win_no
            s = 'norm%s%s,%s%s%f' % (separator,src_file,win_no,separator,norm[0])
            for p in norm[1:]:
                s += ',%f' % (p)
    print s

    #print feature order
    s = 'stats%sch_order%s%s' % (separator,separator,ch_list[en_order[0]])
    for i in range(1,nchan):
        s += ',%s' % ch_list[en_order[i]]
    print s

    #print aggregate entropy
    s = 'stats%sentropy,%s%f' % (separator,separator,entropy[nchan[0],0])
    for i in range(nchan):
        for j in range(npts):
            if i == 0:#skip first entry bc printed above
                continue
            s += ',%f' % entropy[en_order[i],j]
    print s


if __name__ == "__main__":
    main()