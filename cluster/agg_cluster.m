function agg_cluster( US,nclst_l,output_file,net_i2g)
%AGG_CLUSTER Summary of this function goes here
%   Detailed explanation goes here
Z = linkage(US,'average','cosine');
for nclst = nclst_l
    c = cluster(Z,'maxclust',nclst);
    fout = fopen(['../Data/Module/agg/',output_file,num2str(nclst)],'w');
    for i=1:nclst
        fprintf(fout,'%d\t1.0',i);
        id = find(c==i);
        for k = id'
            fprintf(fout,'\t%s',char(values(net_i2g,num2cell(k))));
        end
        fprintf(fout,'\n');
    end
    fclose(fout);
end

end

