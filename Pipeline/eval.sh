#!/bin/bash

clear

# A POSIX variable
OPTIND=1 # Reset in case getopts has been used previously in the shell.

# Initialize Default options
NETWORK="sdf"

# Getoptions
while getopts n: opt; do
  case $opt in
  n)
      NETWORK=$OPTARG
      ;;
  esac
done

shift $((OPTIND - 1))


#GENESETNAME="--cls_one_module--sum.chr22.txt"


GENESETNAME="--"+$NETWORK+"--sum.txt"

GENESETFILE="/data/work/swang141/DreamDiseaseModule/Sheng/Data/Module/local_search/"+$NETWORK+".txt"

echo "Test Gene Module File: $GENESETFILE"
Pascaldir="/data/work/swang141/DreamDiseaseModule/Sheng/analysis/Pascal/Data/PASCAL"
echo $Pascaldir





#: <<'END'
PVAL="EUR.CARDIoGRAM_2010_lipids.HDL_ONE.txt"
cd $Pascaldir
echo "running GWAS test : $PVAL"
pwd
./Pascal --pval=resources/gwas/${PVAL} --runpathway=on --genesetfile=${GENESETFILE} > ${PVAL}log.txt


PVAL="GIANT_HEIGHT_Wood_et_al_2014_pvals.txt"
cd $Pascaldir
echo "running GWAS test : $PVAL"
pwd
./Pascal --pval=resources/gwas/${PVAL} --runpathway=on --chr=22 --genesetfile=${GENESETFILE} > ${PVAL}log.txt
#END

echo "Enrichment test finished.."

Matlabdir="/data/work/swang141/DreamDiseaseModule/Sheng/src/misc"
cd $Matlabdir
matlab -r "genesetfile='$GENESETNAME';compute_fdr"