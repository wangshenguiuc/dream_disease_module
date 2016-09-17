import os
dir = 'E:\\swang141\project\DreamDiseaseModule\Sheng\\analysis\submission\\round2\ch1\\r2_ch1_sub6\\'
name = ['1_ppi_anonym_v2.txt','2_ppi_anonym_v2.txt','3_signal_anonym_directed_v3.txt','4_coexpr_anonym_v2.txt','5_cancer_anonym_v2.txt','6_homology_anonym_v2.txt']
for filename in os.listdir(dir):
	if len(filename)<3:
		continue
	a = int(filename[0])
	print filename,name[a-1]
	os.rename(dir+filename, dir+name[a-1])
