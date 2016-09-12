import sys
NETWORK = sys.argv[1]

OUTPUT_NETWORK = NETWORK+'.dream_format'
fin = open(NETWORK)
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

fout = open(OUTPUT_NETWORK,'w')
for c in cls_dct:
	fout.write(c+'\t1')
	for d in cls_dct[c]:
		fout.write('\t'+d)
	fout.write('\n')
fout.close()