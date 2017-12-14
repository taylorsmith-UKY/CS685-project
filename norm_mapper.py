#!/usr/bin/env python
from __future__ import print_function
import sys

def read_input(file):
    for line in file:
        lsplit = line.rstrip().split(';')
        #if this is a new window
	key = lsplit[0]
	ks = key.split(',')
        if len(ks) > 1:
            yield line

def main(separator=';'):
    # input comes from STDIN (standard input)
    data = read_input(sys.stdin)
    for point in data:
        # write the results to STDOUT (standard output);
        # what we output here will be the input for the
        # Reduce step, i.e. the input for reducer.py
        #
        # tab-delimited; the trivial word count is 1
	print(point,file=sys.stderr)
        print(point)

if __name__ == "__main__":
    main()
