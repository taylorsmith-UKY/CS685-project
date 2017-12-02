from __future__ import division
import numpy as np
import pyedflib
import re
import os

def get_windows(conf):
    input_path=conf['input_path']            #input path to csv or edf files
    output_path=conf['output_path']            #top of directory for processed data
    sigfiles=conf['input_files']            #list of csv/edf files
    hypfiles=conf['hyp_files']                #list of txt files containing sleep stage annotations
    win_dur=conf['win_dur']                    #duration of extracted windows
    win_ovlp=conf['win_ovlp']
    chan_list=[['Fp1',re.compile('EEG Fp1-CLE')],
               ['Fp2',re.compile('EEG Fp2-CLE')],
               ['F7',re.compile('EEG F7-CLE')],
               ['F3',re.compile('EEG F3-CLE')],
               ['Fpz',re.compile('EEG Fpz-CLE')],
               ['F4',re.compile('EEG F4-CLE')],
               ['F8',re.compile('EEG F8-CLE')],
               ['T3',re.compile('EEG T3-CLE')],
               ['C3',re.compile('EEG C3-CLE')],
               ['Cz',re.compile('EEG Cz-CLE')],
               ['C4',re.compile('EEG C4-CLE')],
               ['T4',re.compile('EEG T4-CLE')],
               ['T5',re.compile('EEG T5-CLE')],
               ['P3',re.compile('EEG P3-CLE')],
               ['Pz',re.compile('EEG *[Pp]z-CLE')],
               ['P4',re.compile('EEG P4-CLE')],
               ['T6',re.compile('EEG T6-CLE')],
               ['O1',re.compile('EEG O1-CLE')],
               ['O2',re.compile('EEG O2-CLE')],
               ['A2',re.compile('EEG A.-CLE')]]
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    for i in range(len(sigfiles)):
        print('On example #'+str(i+1))
        inFile = pyedflib.EdfReader(input_path+sigfiles[i])
        ch_idx = np.zeros(len(chan_list)-1,dtype=int)
        all_chan=inFile.getSignalLabels()
        for j in range(len(chan_list)-1):
            ch_idx[j] = [x for x in range(len(all_chan)) if chan_list[j][1].match(all_chan[x])][0]
        comp_idx = [x for x in range(len(all_chan)) if chan_list[-1][1].match(all_chan[x])][0]
        ch_names=[chan_list[x][0]+'-'+chan_list[-1][0] for x in range(len(chan_list)-1)]
        base_fname = sigfiles[i].split('.')[0]
        outFile = open(output_path+base_fname+'_windows.csv','w')

        fs = int(inFile.getSignalHeader(ch_idx[0])['sample_rate'])
        sig_len = int(inFile.getFileDuration()*fs)
        pts_in_win = int(win_dur * fs)
        win_step = int((1-win_ovlp)*win_dur*fs)

        hf = pyedflib.EdfReader(input_path+str(hypfiles[i]))
        annot = hf.readAnnotations()
        count = 0
        for start in range(0,sig_len-pts_in_win,win_step):
            try:
                stg = str(annot[2][np.where(annot[0]*fs > start)[0][0]])
                count+=1
                outFile.write('Window#'+str(count)+','+stg+'\n')
                print_segment(inFile,ch_idx,comp_idx,ch_names,start,pts_in_win,outFile)
            except:
                break
        outFile.close()
    return output_path


def print_segment(inFile,chan_idx,comp_idx,ch_names,start,n,outFile):
    comp = inFile.readSignal(comp_idx,start,n)
    for ch in range(len(chan_idx)):
        sig = inFile.readSignal(chan_idx[ch],start,n) - comp
        outFile.write('%s' % (ch_names[ch]))
        for i in range(len(sig)):
            outFile.write(', %.4f' % (sig[i]))
        outFile.write('\n')
