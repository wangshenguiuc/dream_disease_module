import sys
def process(network):
	fin=open(network)
	mod = set()
	for line in fin:
		w = line.strip().split()
		if len(w)>100 or len(w)<3:
			continue
		mod.add('\t'.join(w))
	fin.close()
	fout = open(network,'w')
	ct=1
	for m in mod:
		fout.write(str(ct)+'\t1.0\t'+m+'\n')
		ct+=1
	fout.close()
	
def process_SA(network):
	OUTPUT_NETWORK = network+'.dream_format'
	fin = open(network)
	fin.readline()
	#Species 0	Gene 7041	Cluster 178
	cls_dct={}
	for line in fin:
		w = line.strip().split('\t')
		cls = w[2].split(' ')[1]
		gid = w[1].split(' ')[1]
		if cls not in cls_dct:
			cls_dct[cls]=set()
		cls_dct[cls].add(gid)
	fin.close()
	fout = open(network,'w')
	for c in cls_dct:
		fout.write(c+'\t1')
		for d in cls_dct[c]:
			fout.write('\t'+d)
		fout.write('\n')
	fout.close()