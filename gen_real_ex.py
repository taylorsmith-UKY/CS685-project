#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 20:45:31 2017

@author: taylorsmith
"""
import os

n_per_file = 50

count = 0
for root,dirs,fnames in os.walk('windows/'):
    for fname in fnames:
        count+=1
        f = open(os.path.join(root,fname),'r')
        ef = open('ex_files/ex'+str(count)+'.csv','w')
        for i in range(n_per_file):
            for j in range(20):
                l = f.readline()
                ef.write(l)
        f.close()
        ef.close()
