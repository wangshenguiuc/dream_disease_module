function [network,gene_map_id,gene_map_name] = read_multiple_network( network_file_l, typed)
%READ_NETWORK Summary of this function goes here
%   Detailed explanation goes here
geneset =[];
for file=network_file_l
    [network,gene_map_id,gene_map_name] = read_network(char(file), typed);
    gene_l = keys(gene_map_name);
    geneset = [geneset,gene_l];
    geneset = unique(geneset);
end

ngene = length(geneset);

gene_map_name = containers.Map(geneset,1:ngene);
gene_map_id = containers.Map(1:ngene,geneset);
network = cell(1,length(network_file_l));
i=1;
for file=network_file_l
    if typed
        [g1,g2,wt,~] = textread(char(file),'%s%s%f%s');
    else
        [g1,g2,wt] = textread(char(file),'%s%s%f');
    end
    g1 = cell2mat(values(gene_map_name,g1));
    g2 = cell2mat(values(gene_map_name,g2));
    
    network{i} = sparse(g1,g2,wt,ngene,ngene);
    i=i+1;
end


end

