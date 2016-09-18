% [Input]
% A: adjacency matrix (could be weighted)
% method: 'personalized-pagerank' or 'self-diffusion'
% aux: auxiliary parameters, such as max number of iterations and
%      restart probability 
%
% [Output]
% Q: diffusion state matrix. i-th column represents the diffusion
%    state of the i-th node. 
%
function [Q,P] = run_diffusion(A, reset_prob, maxiter)
    n = size(A, 1);

    renorm = @(M) bsxfun(@rdivide, M, sum(M));

    A = A + diag(sum(A) == 0); % Add self-edges to isolated nodes
    P = renorm(A);
    fprintf('rsp=%f\n',reset_prob);      
      reset = eye(n);
      Q = reset;
      for i = 1:maxiter
        Q_new = reset_prob * reset + (1 - reset_prob) * P * Q;
        delta = norm(Q - Q_new, 'fro');
         fprintf('Iter %d. Frobenius norm: %f\n', i, delta);
        Q = Q_new;
        if delta < 1e-6
           fprintf('Converged.\n');
          break
        end
      end

    
    Q = bsxfun(@rdivide, Q, sum(Q));

end
