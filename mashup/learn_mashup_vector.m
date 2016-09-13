function [USA,QA] = learn_mashup_vector(network,rspx,net_name,dim_l,net_i2g)

nnet = length(network);
nnode = size(network{1},1);
for i=1:nnet
    tA = run_diffusion(network{i}, 'personalized-pagerank', struct('maxiter', 1, 'reset_prob', rspx));
    if i==1
        QA = tA;
        continue
    end
    QA = [QA,tA];
    save(['..\Data\MashUp\diff',num2str(i),',.mat'],'tA','-v7.3');
end

alpha = 1/(nnode);
QA = log(QA+alpha)-log(alpha);

QA=QA*QA';
dim_l
for dim = dim_l
    fprintf('run SVD d=%d\n',dim);tic
    [U,S,~] = svds(QA,dim);
    LA = U;
    USA = LA*sqrt(S);       
    node_id_sorted = values(net_i2g,num2cell(1:nnode))';    
    T = table(node_id_sorted,USA);
    writetable(T,['../Data/Embedding_vector/MashUp/',char(net_name),num2str(dim),'.emb'],'Delimiter','\t','WriteVariableNames',false,'FileType','text');
end

end

