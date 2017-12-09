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
        yield line

def main(separator='\t'):
    # input comes from STDIN (standard input)
    # key = [source file name, window #, channel name, sleep stage]
    # value = signal amplitude over time
    # package 'CustomMultiOutputFormat.java' to output to different directories
    # based on the first element of the key
    data = read_mapper_output(sys.stdin, separator=separator)

    for line in data:
        print line


if __name__ == "__main__":
    main()
