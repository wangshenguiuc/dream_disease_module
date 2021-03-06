function [network,gene_map_id,gene_map_name] = read_network( file_name, typed)
%READ_NETWORK Summary of this function goes here
%   Detailed explanation goes here
addpath('../Data/Network/our_network/subch1/');
addpath('../Data/Network/Eddie_network/');
if typed
    [g1,g2,wt,~] = textread(file_name,'%s%s%f%s');
else
    [g1,g2,wt] = textread(file_name,'%s%s%f');
end

geneset = unique([g1;g2]);
ngene = length(geneset);

gene_map_name = containers.Map(geneset,1:ngene);
gene_map_id = containers.Map(1:ngene,geneset);

g1 = cell2mat(values(gene_map_name,g1));
g2 = cell2mat(values(gene_map_name,g2));

network = sparse(g1,g2,wt,ngene,ngene);

end

