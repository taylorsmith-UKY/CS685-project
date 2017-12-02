from __future__ import division
import numpy as np
import pyedflib
import re
from scipy.stats import entropy
import os

def get_windows(conf):
	input_path=conf['input_path']			#input path to csv or edf files
	output_path=conf['output_path']			#top of directory for processed data
	sigfiles=conf['input_files']			#list of csv/edf files†
	hypfiles=conf['hyp_files']				#list of txt files containing sleep stage annotations
	win_dur=conf['win_dur']					#duration of extracted windows
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

		nchan = len(ch_idx)
		fs = int(inFile.getSignalHeader(ch_idx[0])['sample_rate'])
		sig_len = int(inFile.getFileDuration()*fs)
		pts_in_win = int(win_dur * fs)
		win_step = int((1-win_ovlp)*win_dur*fs)

		nwin = (sig_len-(win_dur*fs))/win_step

		hf = pyedflib.EdfReader(input_path+str(hypfiles[i]))
		annot = hf.readAnnotations()
		count = 0
		for start in range(0,sig_len-pts_in_win,win_step):
			count+=1
			stg = str(annot[2][np.where(annot[0]*fs > start)[0][0]])
			outFile.write('Window#'+str(count)+', '+stg+'\n')
			print_segment(inFile,ch_idx,comp_idx,ch_names,start,pts_in_win,outFile)
		outFile.close()
	return output_path

def fft_fe(input_dir,output_dir,nfft):
	print('Extracting features')
	nchan=19
	wlen=int((nfft/2)+1)
	count = 0
	for root,dirs,fnames in os.walk(input_dir):
		for fname in fnames:
			print('Extracting features from windows in '+str(fname))
			this_name = str(fname).split('.')[0]+'_fft_feats.csv'
			win_file = open(os.path.join(root,fname),'r')
			feat_file = open(output_dir+this_name,'w')
			for line in win_file:
				l = line.rstrip().split(',')
				if len(l) <=2:
					count+=1
					feat_file.write('\n')
					feat_file.write(str(count))
				else:
					sig = np.array(l[1:],dtype=float)
					freq = (np.abs(np.fft.fft(sig,nfft))[:wlen]**2)/(len(sig)/2)
					print_line(sig,feat_file)
			feat_file.write('\n')
			feat_file.close()
			win_file.close()
	return output_dir, wlen

def normalize(input_dir,nfeats,output_dir):
	print('Normalizing extracted features')
	inds=f[ds_name]
	nchan=inds.shape[0]
	means,stds = get_stats(input_dir,nfeats)
	count = 0
	minims = means - 3*stds
	maxims = means + 3*stds
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)
	for root,dirs,fnames in os.walk(input_dir):
		for fname in fnames:
			this_name = str(fname).split('.')[0]+'_fft_feats_norm.csv'
			feat_file = open(os.path.join(root,fname),'r')
			norm_file = open(output_dir+this_name,'w')
			for line in win_file:
				l = line.rstrip().split(',')[1:]
				norm = (np.array(l)-minims)/(maxims-minims)
				norm[np.where(norm < 0)] = 0
				norm[np.where(norm > 1)] = 1
				count += 1
				feat_file.write(str(count))
				print_line(norm,norm_file)
				feat_file.write('\n')
			feat_file.close()
			norm_file.close()
	return output_dir

def get_stats(input_dir,nfeats):
	sum_x = np.zeros(nfeats)
	sum_x2 = np.zeros(nfeats)
	nwin = 0
	for root,dirs,fnames in os.walk(input_dir):
		for fname in fnames:
			feat_file = open(os.path.join(root,fname),'r')
			for line in feat_file:
				l = line.rstrip().split(',')[1:]
				sum_x += np.array(l)
				sum_x2 += np.array(l)**2
				nwin += 1
	means = sum_x / nwin
	stds = np.sqrt(sum_x2/n - mean**2)
	return means, stds

def calc_entropy(input_dir,nfeats):
	#From scipy.org:
	#entropy = S = -sum(pk * log(pk), axis=0)
	print('Calculating entropy for each feature')

	en = np.zeros(nfeats)
	for root,dirs,fnames in os.walk(input_dir):
		for fname in fnames:
			feat_file = open(os.path.join(root,fname),'r')
			for line in feat_file:
				l = line.rstrip().split(',')[1:]
				x = np.array(l)
				y = np.log(x)
				en -= x*y
	return en

def print_segment(inFile,chan_idx,comp_idx,ch_names,start,n,outFile):
	comp = inFile.readSignal(comp_idx,start,n)
	for ch in range(len(chan_idx)):
		sig = inFile.readSignal(chan_idx[ch],start,n) - comp
		outFile.write('%s' % (ch_names[ch]))
		for i in range(len(sig)):
			outFile.write(', %.4f' % (sig[i]))
		outFile.write('\n')

def print_line(data,outFile):
		for i in range(len(data)):
			outFile.write(', %.4f' % (data[i]))
