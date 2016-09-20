addpath '..\data\embedding_vector\Mashup\'

net_file_l ={'1_ppi_anonym_v2.txt',...
        '2_ppi_anonym_v2.txt',...
        '3_signal_anonym_directed_v3.txt',...
        '4_coexpr_anonym_v2.txt',...
        '5_cancer_anonym_v2.txt','6_homology_anonym_v2.txt'};
    network_file = 'dream_ch2';
    output_path = '../Data/Network/embed_network/subch2/';
    [network, gene_map_id,gene_map_name] = read_multiple_network( net_file_l, false);
    
vec = dlmread('dream_ch250.emb');

% mat = vec(:,2:end);
% diff = cell(1,6);
% for i=1:6
%     load(['diff',num2str(i),'.mat']);
%     diff{i} = tA;
%     i
% end
for i=1:6
    s=max(diff{i});
    length(find(s==1))
end
nnode = size(diff{1},1);
s = sum(network{1});
valid_gene = find(s~=0);
mat = log(network{1}(valid_gene,valid_gene) + 1/nnode);
    [V, d] = svds(mat, 10);      
    x = V*sqrt(d);
% [US,QA] = learn_mashup_vector(network,0.5,network_file,dim_l,gene_map_id,output_path);	
% construct_network(mat,gene_map_id,[network_file,num2str(50)],[0.7,0.8,0.9],output_path);	
D = squareform(1-pdist(x,'cosine'));
length(find(D(:)<0.7))