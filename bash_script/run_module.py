import os
import sys

sys.path.append('../misc/')
sys.path.append('../Pipeline/')
import change_format
import evaluate_local

if len(sys.argv) not in [2,3]:
	print 'Usage:python %s network_file method(MCL\cluster_one)' % sys.argv[0]
	exit()
#'/data/work/swang141/DreamDiseaseModule/Sheng/Data/Network/our_network/'
NETWORK = sys.argv[1]
if os.path.isdir(NETWORK):
	NETWORK_l = []
	for dirname, dirnames, filenames in os.walk(NETWORK):
		for filename in filenames:
			NETWORK_l.append(os.path.join(dirname, filename))
else:
	NETWORK_l = [NETWORK]
	
print NETWORK_l
#NETWORK="ppi_entrez.txt"
if len(sys.argv)==2:
	method_l = ['MCL','SA']
else:
	method_l = [sys.argv[2]]

genescore_dir = '/data/work/swang141/DreamDiseaseModule/Sheng/Data/GWAS_geneScore/'
result_file = '/data/work/swang141/DreamDiseaseModule/Sheng/result/local_evaluation/result0910.txt'
print "here"
evaluate_network = False
postprocess_network = True
for network in NETWORK_l:
	network_name = network.split('/')[-1]
	for method in method_l:
		if method == 'MCL':
			for I in [2.0,3.0,4.0,5.0]:				
				output_module = '/data/work/swang141/DreamDiseaseModule/Sheng/Data/Module/MCL/'+network_name+'_mcl_'+str(I)
				command = '/data/work/swang141/DreamDiseaseModule/Sheng/analysis/MCL/mcl/bin/mcl '+network+' --abc -I '+str(I)+' -o '+output_module
				os.system(command)
				print "here",network,output_module
				print "here",output_module
				if postprocess_network:
					change_format.process(output_module)
				if evaluate_network:
					evaluate_local.evaluate_score(genescore_dir,result_file,output_module)
		if method == 'SA':
			for T in [1.0,0.1,0.01,5]:
				output_module = '/data/work/swang141/DreamDiseaseModule/Sheng/Data/Module/SA/'+network_name+'_SA_'+str(T)
				command = './WlogVImplement 500 1 0 orth.txt 1 '+network+' -t 1 2>log > '+output_module
				os.system(command)
				if postprocess_network:
					change_format.process_SA(output_module)
				if evaluate_network:
					evaluate_local.evaluate_score(genescore_dir,result_file,output_module)
		if method == "cluster_one":
			for d in [0.5,0.4,0.3,0.2]:
				output_module = '/data/work/swang141/DreamDiseaseModule/Sheng/Data/Module/cluster_one/'+network_name+'_CO_'+str(d)
				command = ' java -jar /data/work/swang141/DreamDiseaseModule/Sheng/analysis/clusterOne/cluster_one-1.0.jar  '+network+' -d '+str(d)+'>'+output_module
				os.system(command)
				if postprocess_network:
					change_format.process(output_module)
				if evaluate_network:
					evaluate_local.evaluate_score(genescore_dir,result_file,output_module)
		if method == "ls":
			output_module = '/data/work/swang141/DreamDiseaseModule/Sheng/Data/Module/local_search/'+network_name+'_ls'
			command = 'python /data/work/swang141/DreamDiseaseModule/Sheng/src/local_search.py '+network+' '+output_module
			os.system(command)
			if postprocess_network:
				change_format.process(output_module)
				if evaluate_network:
					evaluate_local.evaluate_score(genescore_dir,result_file,output_module)

	
	