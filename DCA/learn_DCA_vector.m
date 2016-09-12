function [USA,QA] = learn_DCA_vector(network,rspx,dim)

nnode=size(network,1);
QA = run_diffusion(network, 'personalized-pagerank', struct('maxiter', 10, 'reset_prob', rspx));
alpha = 1/(nnode*nnode);
QA = log(QA+alpha)-log(alpha);

fprintf('run SVD d=%d\n',dim);tic
[U,S] = svds(QA,dim);
LA = U;
USA = LA*sqrt(S);

end

