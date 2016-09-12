textin = '/data/work/swang141/DreamDiseaseModule/Sheng/analysis/twanvl/graph-cluster-master/examples/ppi_entrez.out'
textout = '/data/work/swang141/DreamDiseaseModule/Sheng/result/module/ls_ppi_module';
[node,cls] = textread(textin,'%s%d');
ncls = max(cls);
fout = open(textout,'w');
for i=1:cls
	fprintf(fout,'%d\t%d',i,i);
	sel = node(cls==i);
	for s = sel'
		fprintf(fout,'\t%s',s);
	end
	fprintf(fout,'\n')
end
fclose(fout);