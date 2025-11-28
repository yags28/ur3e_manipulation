function [omghat, theta] = ECE569_AxisAng3(expc3)
% *** CHAPTER 3: RIGID-BODY MOTIONS ***
% Takes A 3-vector of exponential coordinates for rotation.
% Returns the unit rotation axis omghat and the corresponding rotation 
% angle theta.

theta = norm(expc3);

if theta < 1e-12
    % Zero rotation → axis is arbitrary, choose [1;0;0]
    omghat = [1; 0; 0];
else
    omghat = expc3 / theta;
end

end