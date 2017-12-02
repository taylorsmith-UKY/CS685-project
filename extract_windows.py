import extract_funcs as ef
import json
import sys
import h5py

nfft=256

nfeats = [10,20,30,50,100]
ham_win=114

def main():
	f=open(sys.argv[1],'r')
	conf=json.load(f)
	f.close()

	window_dir=ef.get_windows(conf)
	feat_dir,nfeats=ef.fft_fe(windo_dir,'fft_features/',nfft)
	norm_dir=ef.normalize(feat_dir,nfeats,'fft_features_norm/')
	entropy=ef.calc_entropy(norm_dir,nfeats)

main()