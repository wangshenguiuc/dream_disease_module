function [Q,P] = fast_diffusion( A, restart_prob )
%FAST_DIFFUSION Summary of this function goes here
%   Detailed explanation goes here


  n = size(A, 1);
  A = A - diag(diag(A));
  A = A + diag(sum(A) == 0);
  P = bsxfun(@rdivide, A, sum(A));
  Q = (eye(n) - (1 - restart_prob) * P) \ (restart_prob * eye(n));


end

