#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 19:21:00 2017

@author: taylorsmith
"""
import numpy as np
separator = '\t'

nex = 50
vlen = 2451

log = open('random_examples.csv','w')

for i in range(nex):
    temp = np.random.random(vlen)
    stg = round(np.random.random()*5)
    s = '%d,%d,%d%s%f' % (1,i,stg,separator,temp[0])
    for p in temp[1:]:
        s += ',%f' % (p)
    log.write(s + '\n')
log.close()
