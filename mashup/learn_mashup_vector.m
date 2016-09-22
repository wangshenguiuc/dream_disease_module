function [x,QA] = learn_mashup_vector(network,rspx,net_name,dim_l,net_i2g,output_path)
nclst_l = [2000,1500,1000,800,500,200,100];
nnet = length(network);
nnode = size(network{1},1);
% RR_sum = zeros(nnode);
% for i=1:nnet
%     Q = run_diffusion(network{i}, rspx, 20);
%     R = log(Q + 1/nnode);
%     RR_sum = RR_sum + R * R';
%     save(['..\Data\MashUp\diff',num2str(i),',.mat'],'R','-v7.3');
% end
R_sum = zeros(nnode);
alpha = 1/(nnode);
for i=1:nnet
%     tA = run_diffusion(network{i}, 'personalized-pagerank', struct('maxiter', 7, 'reset_prob', rspx));
    load(['../Data/Embedding_vector/MashUp/diff',num2str(i),'.mat'],'tA');
QA = log(tA+alpha)-log(alpha);
R_sum = R_sum + QA*QA';
end

save(['../Data/Embedding_vector/MashUp/R_sum.mat'],'R_sum','-v7.3');

for dim = dim_l
    %     fprintf('run SVD d=%d\n',dim);tic
    %     [V, d] = eigs(RR_sum, dim);
    %     x = V*sqrt(sqrt(d));fprintf('run SVD d=%d\n',dim);tic
    R_sum = sparse(R_sum);
    [U,S] = svds(R_sum,dim);
    LA = U;
    x = LA*sqrt(sqrt(S));
    y = LA;
    node_id_sorted = values(net_i2g,num2cell(1:nnode))';
    T = table(node_id_sorted,x);
    writetable(T,['../Data/Embedding_vector/MashUp/',char(net_name),num2str(dim),'.newx'],'Delimiter','\t','WriteVariableNames',false,'FileType','text');
    T = table(node_id_sorted,y);
    writetable(T,['../Data/Embedding_vector/MashUp/',char(net_name),num2str(dim),'.newy'],'Delimiter','\t','WriteVariableNames',false,'FileType','text');
    
    agg_cluster( x,nclst_l,[net_name,num2str(dim),'US_'],net_i2g);
    agg_cluster( y ,nclst_l,[net_name,num2str(dim),'U_'],net_i2g);
    % 	construct_network(x,net_i2g,[net_name,num2str(dim)],[0.9],output_path);
end

end

