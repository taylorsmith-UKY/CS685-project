#!/usr/bin/env python
import sys
import numpy as np

mask = np.array([],dtype=bool)

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
        key,val = line
        feat = np.array(val.split(','),dtype=float)
        feat = feat[mask]
        s = key + separator + arr2str(feat)
        print s

def arr2str(a):
    s = str(a[0])
    for i in range(1,len(a)):
        s += ',' + str(a[i])
    return s

if __name__ == "__main__":
    main()
