function [USA,QA] = learn_DCA_vector(network,rspx,net_name,dim_l,net_i2g,output_path)
nclst_l = [2000,1500,1000,800,500,200,100];
nnode=size(network,1);
QA = run_diffusion(network, 'personalized-pagerank', struct('maxiter', 5, 'reset_prob', rspx));
alpha = 1/(nnode*nnode);
QA = log(QA+alpha)-log(alpha);

for dim = dim_l
    fprintf('run SVD d=%d\n',dim);tic
    [U,S,~] = svds(QA,dim);
    LA = U;
    USA = LA*sqrt(S);       
    node_id_sorted = values(net_i2g,num2cell(1:nnode))';    
    T = table(node_id_sorted,USA);
    writetable(T,['../Data/Embedding_vector/DCA/',char(net_name),num2str(dim),'.emb'],'Delimiter','\t','WriteVariableNames',false,'FileType','text');
	agg_cluster( USA,nclst_l,[net_name,num2str(dim),'_'],net_i2g);
	%construct_network(USA,net_i2g,[net_name,num2str(dim)],[0.7,0.8,0.9],output_path);	
end

end

