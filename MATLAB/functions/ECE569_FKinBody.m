function T = ECE569_FKinBody(M, Blist, thetalist)
% *** CHAPTER 4: FORWARD KINEMATICS (BODY FRAME) ***
% Takes:
%   M: home configuration (SE3)
%   Blist: screw axes in the BODY frame
%   thetalist: joint angles
% Returns:
%   T: end-effector configuration in current body frame

T = M;
n = length(thetalist);

for i = n:-1:1
    Bi = Blist(:, i);
    theta = thetalist(i);
    T = ECE569_MatrixExp6(ECE569_vecTose3(Bi * theta)) * T;
end

end