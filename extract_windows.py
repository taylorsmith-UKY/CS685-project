import extract_funcs as ef
import json
import sys

nfft=256

nfeats = [10,20,30,50,100]
ham_win=114

def main():
	f=open('conf.json','r')
	conf=json.load(f)
	f.close()

	ef.get_windows(conf)

main()