addpath 'DCA'
addpath 'read_data'
addpath 'cluster'
addpath 'build_network'
dim_l = [100,500,1000];

for nfile ={'1_ppi_anonym_v2.txt',...
        '2_ppi_anonym_v2.txt',...
        '3_signal_anonym_directed_v3.txt',...
        '4_coexpr_anonym_v2.txt',...
        '5_cancer_anonym_v2.txt','6_homology_anonym_v2.txt'}
    network_file = char(nfile);
    output_path = '../Data/Network/embed_network/subch1/';
    [network,gene_map_id,gene_map_name] = read_network( network_file, true);
    
    [US,QA] = learn_DCA_vector(network,0.5,network_file,dim_l,gene_map_id,output_path);

end