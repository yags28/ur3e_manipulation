function [thetalist, success] = ECE569_IKinBody(Blist, M, T, thetalist0, eomg, ev)
thetalist = thetalist0;
i = 0;
maxiterations = 20;

% Compute initial error twist Vb = se3ToVec(MatrixLog6( TransInv(FKinBody(M,B,thetalist)) * T ))
Tsb = ECE569_FKinBody(M, Blist, thetalist);
Vb_se3 = ECE569_MatrixLog6( ECE569_TransInv(Tsb) * T );
Vb = ECE569_se3ToVec(Vb_se3);

err = norm(Vb(1:3)) > eomg || norm(Vb(4:6)) > ev;
while err && i < maxiterations
    Jb = ECE569_JacobianBody(Blist, thetalist);
    % Damped-less pseudo-inverse update (pinv)
    thetalist = thetalist + pinv(Jb) * Vb;
    i = i + 1;
    Tsb = ECE569_FKinBody(M, Blist, thetalist);
    Vb_se3 = ECE569_MatrixLog6( ECE569_TransInv(Tsb) * T );
    Vb = ECE569_se3ToVec(Vb_se3);
    err = norm(Vb(1:3)) > eomg || norm(Vb(4:6)) > ev;
end

success = ~err;
end
