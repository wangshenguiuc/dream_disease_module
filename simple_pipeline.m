addpath 'DCA'
[st,ed,wt] = textread('../Data/Network/our_network/ppi_entrez.txt','%s%s%f');
gene_name = unique([st;ed]);
gnum = length(gene_name);
gene_map = containers.Map(gene_name,1:gnum);
gene_map_rev = containers.Map(1:gnum,gene_name);
st_id = cell2mat(values(gene_map,st));
ed_id = cell2mat(values(gene_map,ed));
net = sparse(st_id,ed_id,wt,gnum,gnum);
dim = 50;
US = learn_DCA_vector(net,0.5,dim);
dlmwrite(['../Data/Embedding_vector/DCA/ppi_entrez_US' num2str(dim)],US);
D = (1-pdist(US,'cosine')+1)/2;
D_sp = D(D>0.1);
[a,b,s] = find(net);
dlmwrite(['../Data/Network/our_network/ppi_entrez_US' num2str(dim)],[a-1,b-1,s]);
% nclst = 100;
% ind = kmeans(USA,nclst);
% 
% fout = fopen('../result/module/sample_module.txt','w');
% for i=1:nclst
%     fprintf(fout,'%d\t%d',i,i);
%     for k = find(ind==i)'
%         fprintf(fout,'\t%s',char(values(gene_map_rev,num2cell(k))));
%     end
%     fprintf(fout,'\n');
% end
