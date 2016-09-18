function network_integ = integ_network( network )
%INTEG_NETWORK Summary of this function goes here
%   Detailed explanation goes here
nnet = length(network);
nnode = size(network{1},1);
network_sim = zeros(nnet,nnet);
for i=1:nnet
    max_weight = max(network{i});
    network{i} = network{i}/max_weight;
end
mweight = 0.0;
for i=1:nnet
    for j=i+1:nnet
        edge_set1 = network{i}(:);
        edge_set1 = find(edge_set1>mweight);
        edge_set2 = network{j}(:);
        edge_set2 = find(edge_set2>mweight);
        x_and = length(intersect(edge_set1,edge_set2));
        x1 = length(edge_set1);
        x2 = length(edge_set2);
        JD = x_and/(x1+x2-x_and);
        %         size(edge_set1)
        %         JD = 1 - pdist2(edge_set1',edge_set2','jaccard');
        network_sim(i,j) = JD;
        network_sim(j,i) = JD;
    end
end

network_wt = sum(network_sim);
network_wt = network_wt/sum(network_wt);
network_integ = zeros(nnode,nnode);

for i=1:nnet
    network_integ = network_integ + network_wt*network{i};
end

end

