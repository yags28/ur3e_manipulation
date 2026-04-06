function AdT = ECE569_Adjoint(T)
% *** CHAPTER 3: RIGID-BODY MOTIONS ***
% Takes T a transformation matrix SE3. 
% Returns the corresponding 6x6 adjoint representation [AdT].
%
% Example Input:
% T = [[1, 0, 0, 0];
%      [0, 0, -1, 0];
%      [0, 1, 0, 3];
%      [0, 0, 0, 1]];
% AdT = ECE569_Adjoint(T)

[R, p] = ECE569_TransToRp(T);

% Skew-symmetric matrix of p
px = [    0   -p(3)   p(2);
        p(3)     0   -p(1);
       -p(2)   p(1)     0];

% Construct adjoint
AdT = [R, zeros(3,3);
       px*R, R];

end