addpath 'DCA'
addpath 'read_data'
addpath 'cluster'
addpath 'build_network'
construct_network = false;
dim_l = [500,1000];
for nfile ={'1_ppi_anonym_v2.txt',...
        '2_ppi_anonym_v2.txt',...
        '3_signal_anonym_directed_v3.txt',...
        '4_coexpr_anonym_v2.txt',...
        '5_cancer_anonym_v2.txt','6_homology_anonym_v2.txt'}
    network_file = char(nfile);
    output_path = '../Data/Network/embed_network/subch1/';
    [network,gene_map_id,gene_map_name] = read_network( network_file, true);
    
    if construct_network
        for dim = dim_l
            [US,QA] = learn_DCA_vector(network,0.5,[dim],gene_map_id);
            construct_network(US,gene_map_id,[network_file,num2str(dim)],[0.7,0.8,0.9],output_path);
        end
    else
        [US,QA] = learn_DCA_vector(network,0.5,dim_l,gene_map_id);
    end  
    agg_cluster( US,nclst_l,network_file);
end