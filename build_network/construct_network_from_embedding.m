addpath 'mashup'
addpath 'read_data'
addpath 'cluster'
addpath 'DCA'
addpath 'build_network'
addpath '../Data/Network/subch2/subchallenge2'
file_head = 'dream_ch2';
dim_l = [50,500,1000,2000];
net_file_l ={'1_ppi_anonym_aligned_v2.txt',...
    '2_ppi_anonym_aligned_v2.txt',...
    '3_signal_anonym_aligned_directed_v3.txt',...
    '4_coexpr_anonym_aligned_v2.txt',...
    '5_cancer_anonym_aligned_v2.txt','6_homology_anonym_aligned_v2.txt'};
network_file = 'dream_ch2';
output_path = '../Data/Network/embed_network/subch2/';
[network,i2g,g2i] = read_multiple_network( net_file_l, false);

for dim = dim_l
    embed_file = ['../Data/Embedding_vector/MashUp/',char(file_head),num2str(dim),'.newy'];
    x = dlmread(embed_file);
    x = x(:,2:end);
    construct_network(x,i2g,[file_head,num2str(dim)],[0.7,0.8,0.9],output_path);
end
