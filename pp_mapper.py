#!/usr/bin/env python

import sys

ch_list=['Fp1-A2','Fp2-A2','F7-A2','F3-A2','Fpz-A2','F4-A2','F8-A2',
		 'T3-A2','C3-A2','Cz-A2','C4-A2','T4-A2','T5-A2',
		 'P3-A2','Pz-A2','P4-A2','T6-A2','O1-A2','O2-A2']

def read_input(file):
    for line in file:
            yield line

def main(separator=';'):
    # input comes from STDIN (standard input)
    data = read_input(sys.stdin)
    for point in data:
        # write the results to STDOUT (standard output);
        # what we output here will be the input for the
        # Reduce step, i.e. the input for reducer.py
        #
        print point

if __name__ == "__main__":
    main()
