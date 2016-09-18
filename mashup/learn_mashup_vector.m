function [x,Q] = learn_mashup_vector(network,rspx,net_name,dim_l,net_i2g,output_path)
nclst_l = [2000,1500,1000,800,500,200,100];
nnet = length(network);
nnode = size(network{1},1);
RR_sum = zeros(nnode);
for i=1:nnet
    Q = run_diffusion(network{i}, rspx, 20); 
    R = log(Q + 1/nnode);
    RR_sum = RR_sum + R * R';
    save(['..\Data\MashUp\diff',num2str(i),',.mat'],'R','-v7.3');
end

for dim = dim_l
    fprintf('run SVD d=%d\n',dim);tic
    [V, d] = eigs(RR_sum, dim);      
    x = V*sqrt(sqrt(d));
    node_id_sorted = values(net_i2g,num2cell(1:nnode))';    
    T = table(node_id_sorted,USA);
    writetable(T,['../Data/Embedding_vector/MashUp/',char(net_name),num2str(dim),'.emb'],'Delimiter','\t','WriteVariableNames',false,'FileType','text');
	agg_cluster( USA,nclst_l,[net_name,num2str(dim),'_'],net_i2g);
	%construct_network(USA,net_i2g,[net_name,num2str(dim)],[0.7,0.8,0.9],output_path);	
end

end

