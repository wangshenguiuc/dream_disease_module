import sys
import AutoEval
sys.path.append('../Pipeline/')
def evaluate_score(genescore_dir,result_file,output_module):
##evaluation
	print genescore_dir
	print result_file
	print output_module
	score = AutoEval.module_eval_python(output_module,genescore_dir,n_workers=40,verbose=False)
	print score,output_module
	fout = open(result_file,'a')
	fout.write(output_module+'\t'+str(score)+'\n')
	print output_module,score
	fout.close()