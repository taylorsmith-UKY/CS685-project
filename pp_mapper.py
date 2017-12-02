#!/usr/bin/env python

import sys

lines_per_window = 20

ch_list=['Fp1-A2','Fp2-A2','F7-A2','F3-A2','Fpz-A2','F4-A2','F8-A2',
		 'T3-A2','C3-A2','Cz-A2','C4-A2','T4-A2','T5-A2',
		 'P3-A2','Pz-A2','P4-A2','T6-A2','O1-A2','O2-A2']

def read_input(file):
    window_no = 0
    count = 0
    for line in file:
        count += 1
        #if this is a new window
        if count == 1:
            window_no += 1
            lbl = line.rstrip()[-1]
        #if this is the last line for this window
        else:
            data = [file.name.split('_')[0],window_no,ch_list[count],lbl] + \
            [line.rstrip().split(',')[x] for x in range(len(line.rstrip().split(',')))]
            if count == 20:
                count = 0
                yield data

def main(separator='\t'):
    # input comes from STDIN (standard input)
    data = read_input(sys.stdin)
    for point in data:
        # write the results to STDOUT (standard output);
        # what we output here will be the input for the
        # Reduce step, i.e. the input for reducer.py
        #
        # tab-delimited; the trivial word count is 1
        s = ('%s,%s,%s,%s%s%s' % (point[0],point[1],point[2],point[3],separator,point[4]))
        for p in point[5:]:
            s += ',%s' % (p)
        print s

if __name__ == "__main__":
    main()