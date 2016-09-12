path = '/data/work/swang141/DreamDiseaseModule/Sheng/Data/Network'
for NETWORK_name in ['dca50_knn_new5.txt']:#['1_ppi_anonym_v2.txt','2_ppi_anonym_v2.txt','3_signal_anonym_directed_v3.txt','4_coexpr_anonym_v2.txt','5_cancer_anonym_v2.txt','6_homology_anonym_v2.txt','1_ppi_anonym_v2LINE_knn5.txt','2_ppi_anonym_v2LINE_knn5.txt','3_signal_anonym_directed_v3LINE_knn5.txt','4_coexpr_anonym_v2LINE_knn5.txt','5_cancer_anonym_v2LINE_knn5.txt','6_homology_anonym_v2LINE_knn5.txt']:
	NETWORK= path + '/subch2/'+NETWORK_name
	format = 'SA'
	output_NETWORK = path+'/'+format+'_format/'+NETWORK_name

	fin = open(NETWORK)
	edge=set()
	node=set()
	for line in fin:
		w = line.strip().split()
		edge.add(w[0]+'\t'+w[1]+'\t'+w[2]+'\n')
		edge.add(w[1]+'\t'+w[0]+'\t'+w[2]+'\n')
		node.add(w[0])
		node.add(w[1])
	fin.close()
	fout=open(output_NETWORK,'w')
	fout.write('0'+'\n'+str(len(node))+'\n')
	for e in edge:
		fout.write(e)
	fout.close()