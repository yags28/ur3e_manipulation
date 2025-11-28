function Jb = ECE569_JacobianBody(Blist, thetalist)
n = length(thetalist);
Jb = zeros(6, n);
T = eye(4);
% Compute transformation from joint i+1..n to end-effector
for i = n:-1:1
    Jb(:, i) = ECE569_Adjoint(T) * Blist(:, i);
    % Update T <- T * exp([ -B_i * theta_i ]) so next column uses proper adjoint
    exp_neg = ECE569_MatrixExp6( ECE569_VecTose3(-Blist(:, i) * thetalist(i)) );
    T = exp_neg * T;
end
end
