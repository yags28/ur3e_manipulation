function T = ECE569_FKinSpace(M, Slist, thetalist)
T = eye(4);
n = length(thetalist);
for i = 1:n
    se3mat = ECE569_VecTose3(Slist(:,i) * thetalist(i));
    T = T * ECE569_MatrixExp6(se3mat);
end
T = T * M;
end
