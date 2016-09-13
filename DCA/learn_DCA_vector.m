function [USA,QA] = learn_DCA_vector(network,rspx,net_name,dim_l,net_i2g)

nnode=size(network,1);
QA = run_diffusion(network, 'personalized-pagerank', struct('maxiter', 10, 'reset_prob', rspx));
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
end
end

