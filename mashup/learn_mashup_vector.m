function [USA,QA] = learn_mashup_vector(network,rspx,dim)

nnet = length(network);
nnode = size(network{1},1);
for i=1:nnet
    tA = run_diffusion (network{i}, 'personalized-pagerank', struct('maxiter', 20, 'reset_prob', rspx));
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

fprintf('run SVD d=%d\n',dim);tic
QA = sparse(QA);
[U,S] = svds(QA,dim);
LA = U;
USA = LA*sqrt(sqrt(S));toc


end

