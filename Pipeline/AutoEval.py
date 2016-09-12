import matplotlib
matplotlib.use('Agg')
import os
from os import listdir
from os.path import isfile, join
from functools import partial
from multiprocessing import Pool
from subprocess import call, STDOUT, check_call, check_output, Popen, PIPE
from time import time
import pandas as pd
from Clustering import read_module_file
from scipy.stats import chi2, rankdata, spearmanr, pearsonr
from collections import defaultdict
import matplotlib.pyplot as plt
from plotting_util import quant_2_color
from matplotlib.cm import get_cmap

import warnings
import numpy as np
from statsmodels.sandbox.stats.multicomp import multipletests

def test_eval():
    """
    Simple function for testing funcionality of pascal auto testing system
    :return:
    """

    print(test)
    rename_gwas_files('/data/work/swang141/DreamDiseaseModule/Sheng/Data/GWAS/GWAS_Pascal/')

    eval(module_file='sdfbnsfg',
         gwas_dir='/data/work/swang141/DreamDiseaseModule/Sheng/Data/GWAS/GWAS_Pascal/',
         n_workers=40,
         subset=4000)


def safe_run(*args, **kwargs):
    """Call run(), catch exceptions."""
    try: run(*args, **kwargs)
    except Exception as e:
        print("error: %s run(*%r, **%r)" % (e, args, kwargs))


def run(content,threshold=0.05,verbose=False):
    """

    :param gwas_dataset_file:
    :param module_file:
    :param threshold:
    :return:
    """
    cmd,pid = content
    print('Pid: '+str(pid))

    os.chdir('/data/work/swang141/DreamDiseaseModule/Sheng/analysis/Pascal/Data/PASCAL/')
    with open('/data/work/ntrusse2/debug_stdout.txt', 'a') as out:
        with open('/data/work/ntrusse2/debug_stderr.txt', 'a') as err:
            robject = call(cmd,shell=False,stdout=out,stderr=err)

    return robject


def get_sumgenescore_files(in_dir):
    """

    :param in_dir:
    :return:
    """

    genescore_files = [join(in_dir, f) for f in listdir(in_dir) if isfile(join(in_dir, f)) and f.endswith('sum.genescores.txt')]

    return genescore_files






def pathway_score(pval_file,module_file,verbose=False):
    """

    :param pval_file: File of SNP enrichment Scores
    :param module_file: File of gene modules (clusters)
    :return:
    """

    pathway_dict = defaultdict(list)

    if os.path.exists(pval_file) and os.path.exists(module_file):

        pf = pd.read_csv(pval_file,'\t')
        mdict = read_module_file(module_file)

        # Compute Block
        pvals = np.array([np.float64(p) for p in pf['pvalue'].values])
        rank = rankdata(pvals,method='dense')
        max_rank = float(max(rank) + 1)
        rank = max_rank - rank
        uvals =  [float(r)/max_rank for r in rank]
        chivals = [chi2.ppf(u,df=1) for u in uvals]
        geneid = [float(g) for g in pf['gene_id']]
        chi_dict = dict(zip(geneid,chivals))


        if verbose:
            print('max rank: '+str(max(rank)))
            print('max uvals: '+str(max(uvals)))
            print('min rank: ' + str(min(rank)))
            print('min uvals: ' + str(min(uvals)))
            print('# of Genes:'+str(len(chi_dict)))


        for mid in mdict:
            genes = mdict[mid]

            chi_sum = 0
            dropped_genes = []
            M = 0
            for g in genes:
                try:
                    chi_sum += chi_dict[g]
                    M += 1
                except KeyError:
                    dropped_genes.append(g)

            chi_pval = 1 - chi2.cdf(chi_sum, df=M)

            pathway_dict['Module_id'].append(mid)
            pathway_dict['Genes'].append(str(genes))
            pathway_dict['Dropped_Genes'].append(str(dropped_genes))
            pathway_dict['M'].append(M)
            pathway_dict['n_genes'].append(len(genes))
            pathway_dict['n_dropped_genes'].append(len(dropped_genes))
            pathway_dict['chi2_sum'].append(chi_sum)
            pathway_dict['chi2_pval'].append(chi_pval)

            if verbose:
                print('Module # ' + str(mid))
                print('\tGenes: '+str(genes))
                print('\tDropped Genes: '+str(dropped_genes))
                print('\t# of Genes: ' + str(len(genes)))
                print('\tM = '+str(M))
                print('\t# of dropped Genes: ' + str(len(dropped_genes)))
                print('\tChi^2 Sum: '+str(chi_sum))
                print('\tChi^2 Pval: '+str(chi_pval))

        df = pd.DataFrame(pathway_dict)
        df.sort('chi2_pval',axis=0,ascending=True,inplace=True)


        if verbose:
            print(df)
            df.to_csv('/data/work/ntrusse2/test_pathwayscore.csv')
            return df
        else:
            pvals = np.array(pathway_dict['chi2_pval'])
            mids = np.array(pathway_dict['Module_id'])
            mids = mids[~np.isnan(pvals)]
            pvals = pvals[~np.isnan(pvals)]

            reject,fdrp,asidack,abonf = multipletests(pvals,method='bonferroni',alpha=0.05)

            sig_modules = mids[fdrp < 0.05]

            #if len(sig_modules) >= 1:
            #    print('Significant Modules: '+str(sig_modules)+' FDR Pvals: '+str(fdrp[fdrp < 0.05]))

            return sig_modules

    else:
        warnings.warn('File not found '+pval_file+' '+module_file)







def make_command(gwas_dataset_file,module_file):
    cmd = [
        #'cd','/data/work/swang141/DreamDiseaseModule/Sheng/analysis/Pascal/Data/PASCAL/;',
        '/data/work/swang141/DreamDiseaseModule/Sheng/analysis/Pascal/Data/PASCAL/Pascal',
        '--pval=' + gwas_dataset_file,
        '--runpathway=on',
        #'--genesetfile=' + module_file,
        #'--chr=22'
           ]
    #cmd =  ' '.join(cmd)

    return cmd


    """
    # Convert PASCAL Result from diskfile to numpy array
    pascal_dump_location = ''
    p_vals = []
    with open(pascal_dump_location,mode='r') as pvals:
        for p_val in pvals:
            p_vals.append(int(p_val))
    p_vals = np.array(p_vals)


    # Perform multiple testing correction
    adj_p_vals = multipletests(p_vals,alpha=threshold,method='hs')

    # Count Number Significant
    counter = adj_p_vals > threshold
    c = np.sum(counter)

    return c
    """


def rename_gwas_files(gwas_dir):
    """

    :param dir:
    :return:
    """

    print('Renaming Files')
    gwas_files = [join(gwas_dir, f) for f in listdir(gwas_dir) if isfile(join(gwas_dir, f))]
    for pre in gwas_files:


        post = pre.translate(None,";")
        if len(post) != len(pre):
            print('\tPre: ' + pre)
            print('\tPost: ' + post)
            os.rename(pre,post)

def rename_mod_files(gwas_dir):
    """

    :param dir:
    :return:
    """

    print('Renaming Files')
    gwas_files = [join(gwas_dir, f) for f in listdir(gwas_dir) if isfile(join(gwas_dir, f))]
    for pre in gwas_files:


        post = pre.translate(None,"\r\r")
        if len(post) != len(pre):
            print('\tPre: ' + pre)
            print('\tPost: ' + post)
            os.rename(pre,post)

def eval(module_file,gwas_dir,n_workers=2,subset=5):

    gwas_files = [join(gwas_dir, f) for f in listdir(gwas_dir) if isfile(join(gwas_dir, f))]
    module_file = 'mymodules.txt'

    subset = min(subset,len(gwas_files))
    commands = [(make_command(g,module_file),i) for i,g in enumerate(gwas_files[0:subset])]
    print('# of Commands: '+str(len(commands)))


    stdout_path = '/data/work/ntrusse2/debug_stdout.txt'
    stderr_path = '/data/work/ntrusse2/debug_stderr.txt'

    os.chdir('/data/work/swang141/DreamDiseaseModule/Sheng/analysis/Pascal/Data/PASCAL/')

    try:
        os.remove(stderr_path)
        os.remove(stdout_path)
        print("Succesful purging of stderr and stdout")
    except OSError:
        pass

    if n_workers < 1:
        print("Serial")
        os.chdir('/data/work/swang141/DreamDiseaseModule/Sheng/analysis/Pascal/Data/PASCAL/')
        for cmd in commands:
            s = '\n'+'-'*50
            print(s)
            print(cmd)
            call(cmd)
    else:
        print("Parallel")
        print('Num Workers = '+str(n_workers))
        pool = Pool(n_workers)  # two concurrent commands at a time
        print(commands)
        results = pool.map(safe_run,commands)
        print(results)

    print('\n-------------------------------------STDOUT-------------------------------------')
    with open(stdout_path) as f:
        for l in f:
            print(l)
    print('\n-------------------------------------STDERR-------------------------------------')
    with open(stderr_path) as f:
        for l in f:
            print(l)



        #for i, returncode in enumerate(pool.imap(partial(call, shell=True), commands)):
        #    if returncode != 0:
        #        print("%d command failed: %d" % (i, returncode))





    # Evaluate
    #files = [(str(gwas_file),module_file) for gwas_file in gwas_files]
    #p = Pool(n_workers)
    #results = p.map_async(safe_run,files)

def compare_pascal_v_python(pascal_file,python_df):
    """

    :param pascal_file:
    :param python_df:
    :return:
    """

    print('Building Pascal Chi2 Module Score Dict')
    pascal_dict = defaultdict(float)
    with open(pascal_file) as f:
        c = 0
        for line in f:
            if c > 0:
                m_id, chi2, emp = line.split()
                if chi2 == 'NA':
                    print('Module: '+str(m_id))
                    pass
                else:
                    pascal_dict[m_id] = float(chi2)
            else:
                pass
            c += 1

    print('Syncing Pascal and Python Scores')
    pascal = []
    python = []
    extra = []
    for m,chi,d in zip(df['Module_id'].values,df['chi2_pval'].values,df['n_genes'].values):
        pascal.append(float(pascal_dict[m]))
        python.append(float(chi))
        extra.append(float(d))

    plt.figure()
    plt.scatter(python,pascal,c=quant_2_color(extra,cmap=get_cmap('plasma')),alpha=0.7,edgecolors='none')
    plt.xlabel('python')
    plt.ylabel('pascal')
    plt.savefig('/data/work/ntrusse2/pascal_v_python.png')
    print('plot succesful')


    print('Computing Rank Correlation')
    rho,pval = spearmanr(pascal,python)
    print('rho: '+str(rho))
    print('pval: '+str(pval))

    print('Computing  Correlation')
    rho, pval = pearsonr(pascal, python)
    print('Corr: ' + str(rho))
    print('pval: ' + str(pval))

def quick_pathscore(x):
    """

    :param x:
    :return:
    """
    #print('quick_pathscore...')
    #print(1),

    return pathway_score(x[0],x[1],verbose=False)

def module_eval_python(modulefile,genescore_dir,n_workers=40,verbose=True):
    """

    :param modulefile:
    :param genescore_dir:
    :return:
    """

    genescore_files = get_sumgenescore_files(genescore_dir)
    print('# of gene score files: '+str(len(genescore_files)))

    if n_workers > 1:
        pool = Pool(n_workers)  # two concurrent commands at a time
        results = pool.map(quick_pathscore,[(g,modulefile) for g in genescore_files])
    else:
        results = []
        for g in genescore_files:
            results.append(pathway_score(pval_file=g,
                                     module_file=modulefile,
                                     verbose=False))

    print("Checking significant modules...")
    num_significant = 0
    all_sig_mods = defaultdict()
    for r in results:
        if len(r) > 0:
            for module in r:
                if module in all_sig_mods:
                    #print(str(module)+' has been found prevoiusly =(')
                    pass
                else:
                    num_significant += 1
                    all_sig_mods[module] = 1


    return num_significant



def test_modules(module_dir,genescores_dir):
    """

    :param module_dir:
    :param genescores_dir:
    :return:
    """
    print('Testing Module Files!')

    module_files = [join(module_dir, f) for f in listdir(module_dir) if isfile(join(module_dir, f))]
    module_files.sort()

    print(len(module_files))
    print(module_files)
    spacer = '\n'+'-'*100 + '\n'

    for m in module_files:
        score = module_eval_python(m, genescores_dir)
        print(spacer+'Module file: '+m)
        print('# Significant: '+str(score)+spacer)






if __name__ == "__main__":

    rename_mod_files('/data/work/swang141/DreamDiseaseModule/Sheng/Data/Module/MCL/')


    test_modules(module_dir='/data/work/swang141/DreamDiseaseModule/Sheng/Data/Module/local_search',
                 genescores_dir='/data/work/swang141/DreamDiseaseModule/Sheng/Data/GWAS_geneScore/'
                 )

    test_modules(module_dir='/data/work/swang141/DreamDiseaseModule/Sheng/Data/Module/cluster_one',
                 genescores_dir='/data/work/swang141/DreamDiseaseModule/Sheng/Data/GWAS_geneScore/')


    print(taco)

    test_modules(module_dir='/data/work/swang141/DreamDiseaseModule/Sheng/Data/Module/MCL/',
                 genescores_dir='/data/work/swang141/DreamDiseaseModule/Sheng/Data/GWAS_geneScore/')

    '''

    df = pathway_score(
        pval_file='/data/work/swang141/DreamDiseaseModule/Sheng/Data/GWAS_geneScore/EUR.CARDIoGRAM_2010_lipids.HDL_ONE.sum.genescores.txt',
        module_file='/data/work/swang141/DreamDiseaseModule/Sheng/Data/Module/cls_one_module.txt')

    compare_pascal_v_python(pascal_file='/data/work/swang141/DreamDiseaseModule/Sheng/analysis/Pascal/Data/PASCAL/output/EUR.CARDIoGRAM_2010_lipids.HDL_ONE.PathwaySet--cls_one_module--sum.txt',
                            python_df=df)


    #pathway_score(pval_file='/data/work/swang141/DreamDiseaseModule/Sheng/analysis/Pascal/Data/PASCAL/output/EUR.CARDIoGRAM_2010_lipids.HDL_ONE.sum.genescores.txt',
    #              module_file='/data/work/swang141/DreamDiseaseModule/Sheng/Data/Module/cls_one_module.txt')

    #test_eval()
    '''

