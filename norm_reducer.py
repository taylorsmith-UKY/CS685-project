#!/usr/bin/env python

import sys
import numpy as np

#Get channel means and stds and calc normalization coefficients
ch_means = np.array([],dtype=float)
ch_stds = np.array([],dtype=float)
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
    cur_win = None
    count = 0
    for line in data:
        #split key into components
        keyt,val = line.split(separator)
        src_file,win_no,ch_name,lbl = key.split(',')
        cidx = np.where(ch_list == ch_name)[0][0]
        sig = np.array(val.split(','),dtype=float)
        norm = (sig - ch_mins[cidx])/(ch_max[cidx]-ch_mins[cidx])
        norm[np.where(norm < 0)] = 0
        norm[np.where(norm > 1)] = 1
        norm_str = arr2str(norm)

        if cur_win != win_no:
            cur_win = win_no
            if count != 0:
                s = key + separator + feats
                print s
            feats = norm_str
            ks = keyt.split(',')
            key = '%s,%s,%s' % (ks[0],ks[1],ks[3])
        else:
            feats += ',' + norm_str
        count+=1

    #print last window
    s = key + separator + feats
    print s


def arr2str(a):
    s = str(a[0])
    for i in range(1,len(a)):
        s += ',' + str(a[i])
    return s


if __name__ == "__main__":
    main()