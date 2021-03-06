addpath 'mashup'
addpath 'read_data'
addpath 'cluster'
addpath 'DCA'
addpath 'build_network'
addpath '../Data/Network/subch2/subchallenge2'

dim_l = [50,500,1000,2000];

net_file_l ={'1_ppi_anonym_aligned_v2.txt',...
    '2_ppi_anonym_aligned_v2.txt',...
        '3_signal_anonym_aligned_directed_v3.txt',...
        '4_coexpr_anonym_aligned_v2.txt',...
        '5_cancer_anonym_aligned_v2.txt','6_homology_anonym_aligned_v2.txt'};
    network_file = 'dream_ch2';
    output_path = '../Data/Network/embed_network/subch2/';
    [network, gene_map_id,gene_map_name] = read_multiple_network( net_file_l, false);
    

[US,QA] = learn_mashup_vector(network,0.5,network_file,dim_l,gene_map_id,output_path);		
