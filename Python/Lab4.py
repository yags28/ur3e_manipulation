# import matplotlib.pyplot as plt
# import numpy as np
# import math

# '''
# *** BASIC HELPER FUNCTIONS ***
# '''

# def ECE569_NearZero(z):
#     """Determines whether a scalar is small enough to be treated as zero"""
#     return abs(z) < 1e-6

# def ECE569_Normalize(V):
#     """Normalizes a vector"""
#     return V / np.linalg.norm(V)

# '''
# *** CHAPTER 3: RIGID-BODY MOTIONS ***
# '''

# def ECE569_RotInv(R):
#     """Inverts a rotation matrix"""
#     return np.array(R).T

# def ECE569_VecToso3(omg):
#     """Converts a 3-vector to an so(3) representation"""
#     return np.array([[0,       -omg[2],  omg[1]],
#                      [omg[2],       0, -omg[0]],
#                      [-omg[1], omg[0],       0]])

# def ECE569_so3ToVec(so3mat):
#     """Converts an so(3) representation to a 3-vector"""
#     return np.array([so3mat[2][1], so3mat[0][2], so3mat[1][0]])

# def ECE569_AxisAng3(expc3):
#     """Converts a 3-vector of exponential coordinates for rotation into axis-angle form"""
#     return (ECE569_Normalize(expc3), np.linalg.norm(expc3))

# def ECE569_MatrixExp3(so3mat):
#     """Computes the matrix exponential of a matrix in so(3)"""
#     omgtheta = ECE569_so3ToVec(so3mat)
#     if ECE569_NearZero(np.linalg.norm(omgtheta)):
#         return np.eye(3)
#     else:
#         theta = ECE569_AxisAng3(omgtheta)[1]
#         omgmat = so3mat / theta
#         return np.eye(3) + np.sin(theta) * omgmat \
#                + (1 - np.cos(theta)) * np.dot(omgmat, omgmat)

# def ECE569_MatrixLog3(R):
#     """Computes the matrix logarithm of a rotation matrix"""
#     acosinput = (np.trace(R) - 1) / 2.0
#     if acosinput >= 1:
#         return np.zeros((3, 3))
#     elif acosinput <= -1:
#         if not ECE569_NearZero(1 + R[2][2]):
#             omg = (1.0 / np.sqrt(2 * (1 + R[2][2]))) \
#                   * np.array([R[0][2], R[1][2], 1 + R[2][2]])
#         elif not ECE569_NearZero(1 + R[1][1]):
#             omg = (1.0 / np.sqrt(2 * (1 + R[1][1]))) \
#                   * np.array([R[0][1], 1 + R[1][1], R[2][1]])
#         else:
#             omg = (1.0 / np.sqrt(2 * (1 + R[0][0]))) \
#                   * np.array([1 + R[0][0], R[1][0], R[2][0]])
#         return ECE569_VecToso3(np.pi * omg)
#     else:
#         theta = np.arccos(acosinput)
#         return theta / 2.0 / np.sin(theta) * (R - np.array(R).T)

# def ECE569_RpToTrans(R, p):
#     """Converts a rotation matrix and a position vector into homogeneous transformation matrix"""
#     return np.r_[np.c_[R, p], [[0, 0, 0, 1]]]

# def ECE569_TransToRp(T):
#     """Converts a homogeneous transformation matrix into a rotation matrix and position vector"""
#     T = np.array(T)
#     return T[0: 3, 0: 3], T[0: 3, 3]

# def ECE569_TransInv(T):
#     """Inverts a homogeneous transformation matrix"""
#     R, p = ECE569_TransToRp(T)
#     Rt = np.array(R).T
#     return np.r_[np.c_[Rt, -np.dot(Rt, p)], [[0, 0, 0, 1]]]

# def ECE569_VecTose3(V):
#     """Converts a spatial velocity vector into a 4x4 matrix in se3"""
#     # V = [omega, v]
#     omega = V[0:3]
#     v = V[3:6]
#     so3 = ECE569_VecToso3(omega)
#     return np.r_[np.c_[so3, v], [[0, 0, 0, 0]]]

# def ECE569_se3ToVec(se3mat):
#     """Converts an se3 matrix into a spatial velocity vector"""
#     return np.r_[ECE569_so3ToVec(se3mat[0: 3, 0: 3]), se3mat[0: 3, 3]]

# def ECE569_Adjoint(T):
#     """Computes the adjoint representation of a homogeneous transformation matrix"""
#     R, p = ECE569_TransToRp(T)
#     p_so3 = ECE569_VecToso3(p)
#     return np.r_[np.c_[R, np.zeros((3, 3))],
#                  np.c_[np.dot(p_so3, R), R]]

# def ECE569_MatrixExp6(se3mat):
#     """Computes the matrix exponential of an se3 representation of exponential coordinates"""
#     se3mat = np.array(se3mat)
#     omgtheta = ECE569_so3ToVec(se3mat[0: 3, 0: 3])
    
#     if ECE569_NearZero(np.linalg.norm(omgtheta)):
#         return np.r_[np.c_[np.eye(3), se3mat[0: 3, 3]], [[0, 0, 0, 1]]]
#     else:
#         theta = ECE569_AxisAng3(omgtheta)[1]
#         omgmat = se3mat[0: 3, 0: 3] / theta
#         R = ECE569_MatrixExp3(se3mat[0: 3, 0: 3])
#         v_vec = se3mat[0: 3, 3] / theta
        
#         # G(theta) * v formula
#         G_theta = np.eye(3) * theta + (1 - np.cos(theta)) * omgmat + \
#                   (theta - np.sin(theta)) * np.dot(omgmat, omgmat)
        
#         p = np.dot(G_theta, v_vec)
#         return np.r_[np.c_[R, p], [[0, 0, 0, 1]]]

# def ECE569_MatrixLog6(T):
#     """Computes the matrix logarithm of a homogeneous transformation matrix"""
#     R, p = ECE569_TransToRp(T)
#     omgmat = ECE569_MatrixLog3(R)
    
#     if np.array_equal(omgmat, np.zeros((3, 3))):
#         return np.r_[np.c_[np.zeros((3, 3)), T[0: 3, 3]], [[0, 0, 0, 0]]]
#     else:
#         theta = np.arccos((np.trace(R) - 1) / 2.0)
#         omgmat_norm = omgmat / theta
        
#         G_inv = np.eye(3) / theta - 0.5 * omgmat_norm + \
#                 (1 / theta - 0.5 / np.tan(theta / 2)) * np.dot(omgmat_norm, omgmat_norm)
                
#         v = np.dot(G_inv, p)
#         se3_mat = np.r_[np.c_[omgmat, np.dot(G_inv, p) * theta], [[0, 0, 0, 0]]]
#         return se3_mat

# '''
# *** CHAPTER 4: FORWARD KINEMATICS ***
# '''

# def ECE569_FKinBody(M, Blist, thetalist):
#     """Computes forward kinematics in the body frame"""
#     T = np.array(M)
#     for i in range(len(thetalist)):
#         # T = M * e^[B1]theta1 * ... * e^[Bn]thetan
#         se3 = ECE569_VecTose3(Blist[:, i] * thetalist[i])
#         T = np.dot(T, ECE569_MatrixExp6(se3))
#     return T

# def ECE569_FKinSpace(M, Slist, thetalist):
#     """Computes forward kinematics in the space frame"""
#     T = np.array(M)
#     for i in range(len(thetalist) - 1, -1, -1):
#         # T = e^[S1]theta1 * ... * e^[Sn]thetan * M
#         se3 = ECE569_VecTose3(Slist[:, i] * thetalist[i])
#         T = np.dot(ECE569_MatrixExp6(se3), T)
#     return T

# '''
# *** CHAPTER 5: VELOCITY KINEMATICS AND STATICS***
# '''

# def ECE569_JacobianBody(Blist, thetalist):
#     """Computes the body Jacobian for an open chain robot"""
#     Jb = np.array(Blist).copy().astype(float)
#     T = np.eye(4)
#     # The last column is just Bn
#     Jb[:, -1] = Blist[:, -1]
    
#     # Iterate backwards from n-1 to 0
#     for i in range(len(thetalist) - 2, -1, -1):
#         # Transformation from frame i+1 to frame i due to joint i+1 rotation
#         # Note: Blist column order is 0 to N-1
#         se3 = ECE569_VecTose3(Blist[:, i+1] * -thetalist[i+1])
#         T = np.dot(T, ECE569_MatrixExp6(se3))
#         # Adjoint of the transformation product transforms the screw axis
#         Jb[:, i] = np.dot(ECE569_Adjoint(T), Blist[:, i])
#     return Jb

# '''
# *** CHAPTER 6: INVERSE KINEMATICS ***
# '''

# def ECE569_IKinBody(Blist, M, T, thetalist0, eomg, ev):
#     """Computes inverse kinematics in the body frame"""
#     thetalist = np.array(thetalist0).copy()
#     i = 0
#     maxiterations = 20
    
#     # Calculate current configuration
#     T_curr = ECE569_FKinBody(M, Blist, thetalist)
#     # Calculate error twist Vb in body frame: [Ad_Tsb] * Vb = Vs -> Vb = log(T_sb^-1 * T_sd)
#     T_diff = np.dot(ECE569_TransInv(T_curr), T)
#     Vb_se3 = ECE569_MatrixLog6(T_diff)
#     Vb = ECE569_se3ToVec(Vb_se3)
    
#     err = np.linalg.norm([Vb[0], Vb[1], Vb[2]]) > eomg \
#           or np.linalg.norm([Vb[3], Vb[4], Vb[5]]) > ev
          
#     while err and i < maxiterations:
#         # Calculate Jacobian
#         Jb = ECE569_JacobianBody(Blist, thetalist)
#         # Update theta: theta = theta + pinv(Jb) * Vb
#         thetalist = thetalist + np.dot(np.linalg.pinv(Jb), Vb)
        
#         i += 1
#         # Recalculate error
#         T_curr = ECE569_FKinBody(M, Blist, thetalist)
#         T_diff = np.dot(ECE569_TransInv(T_curr), T)
#         Vb_se3 = ECE569_MatrixLog6(T_diff)
#         Vb = ECE569_se3ToVec(Vb_se3)
        
#         err = np.linalg.norm([Vb[0], Vb[1], Vb[2]]) > eomg \
#               or np.linalg.norm([Vb[3], Vb[4], Vb[5]]) > ev
              
#     return (thetalist, not err)

# # the ECE569_normalized trapezoid function
# def g(t, T, ta):
#     if t < 0 or t > T:
#         return 0
    
#     if t < ta:
#         return (T/(T-ta))* t/ta
#     elif t > T - ta:
#         return (T/(T-ta))*(T - t)/ta
#     else:
#         return (T/(T-ta))
    
# def trapezoid(t, T, ta):
#     return g(t, T, ta)

# def main():

#     ### Step 1: Trajectory Generation
    
#     # Infinity shape (Lissajous curve)
#     # x = A * sin(a*t)
#     # y = B * sin(b*t)
#     # For infinity shape (figure 8), ratio a:b is 1:2
    
#     T_period = 2 * np.pi
#     # Amplitude scaling to fit in workspace <= 0.16m
#     A = 0.14 # 15cm
#     B = 0.14 # 7cm
#     a_param = 1
#     b_param = 2
    
#     # Create high-res time vector for accurate arc length calculation
#     t_dummy = np.linspace(0, T_period, 1000)
    
#     xd_dummy = A * np.sin(a_param * t_dummy)
#     yd_dummy = B * np.sin(b_param * t_dummy)

#     # calculate the arc length
#     d = 0
#     for i in range(1, len(t_dummy)):
#         dist = np.sqrt((xd_dummy[i] - xd_dummy[i-1])**2 + (yd_dummy[i] - yd_dummy[i-1])**2)
#         d += dist
    
#     print(f"Total Arc Length: {d} m")
    
#     # Desired total time
#     tfinal = 10.0 # Max allowed is 15s
    
#     # calculate average velocity
#     c = d / tfinal
#     print(f"Average Velocity: {c} m/s")
    
#     if c > 0.25:
#         print("WARNING: Velocity exceeds 0.25 m/s limit! Reduce Amplitudes or increase tfinal.")

#     # forward euler to calculate alpha
#     dt = 0.002
#     t = np.arange(0, tfinal, dt)
#     alpha = np.zeros(len(t))
    
#     # Trapezoid ramp time (e.g., 1/5th of total time)
#     ta = 0.5
    
#     # Forward Euler Integration for alpha
#     # d_alpha/dt = c * g(t) / sqrt(xdot^2 + ydot^2)
#     # xdot = A * a * cos(a * alpha)
#     # ydot = B * b * cos(b * alpha)
    
#     for i in range(1, len(t)):
#         current_alpha = alpha[i-1]
        
#         # Derivatives of the path with respect to the parameter (alpha)
#         # d(sin(u))/du = cos(u)
#         dx_dalpha = A * a_param * np.cos(a_param * current_alpha)
#         dy_dalpha = B * b_param * np.cos(b_param * current_alpha)
        
#         denom = np.sqrt(dx_dalpha**2 + dy_dalpha**2)
        
#         # Avoid division by zero
#         if denom < 1e-6:
#             denom = 1e-6
            
#         alpha_dot = (c * trapezoid(t[i-1], tfinal, ta)) / denom
        
#         alpha[i] = alpha[i-1] + alpha_dot * dt

#     # plot alpha vs t
#     plt.figure()
#     plt.plot(t, alpha,'b-',label='alpha')
#     plt.plot(t, np.ones(len(t))*T_period, 'k--',label='T (period)')
#     plt.xlabel('t')
#     plt.ylabel('alpha')
#     plt.title('alpha vs t')
#     plt.legend()
#     plt.grid()
#     plt.show()

#     # Generate the actual trajectory points using the computed alpha
#     x = A * np.sin(a_param * alpha)
#     y = B * np.sin(b_param * alpha)

#     # calculate velocity for verification
#     xdot = np.diff(x)/dt
#     ydot = np.diff(y)/dt
#     v = np.sqrt(xdot**2 + ydot**2)

#     # plot velocity vs t
#     plt.figure()
#     plt.plot(t[1:], v, 'b-',label='velocity')
#     plt.plot(t[1:], np.ones(len(t[1:]))*c, 'k--',label='average velocity')
#     plt.plot(t[1:], np.ones(len(t[1:]))*0.25, 'r--',label='velocity limit')
#     plt.xlabel('t')
#     plt.ylabel('velocity')
#     plt.title('velocity vs t')
#     plt.legend()
#     plt.grid()
#     plt.show()

#     ### Step 2: Forward Kinematics
#     L1 = 0.2435
#     L2 = 0.2132
#     W1 = 0.1311
#     W2 = 0.0921
#     H1 = 0.1519
#     H2 = 0.0854

#     M = np.array([[-1, 0, 0, L1 + L2],
#                   [0, 0, 1, W1 + W2],
#                   [0, 1, 0, H1 - H2],
#                   [0, 0, 0, 1]])
    
#     S1 = np.array([0, 0, 1, 0, 0, 0])
#     S2 = np.array([0, 1, 0, -H1, 0, 0])
#     S3 = np.array([0, 1, 0, -H1, 0, L1])
#     S4 = np.array([0, 1, 0, -H1, 0, L1 + L2])
#     S5 = np.array([0, 0, -1, -W1, L1+L2, 0])
#     S6 = np.array([0, 1, 0, H2-H1, 0, L1+L2])
#     S = np.array([S1, S2, S3, S4, S5, S6]).T
    
#     B1 = np.dot(np.linalg.inv(ECE569_Adjoint(M)), S1)
#     B2 = np.dot(np.linalg.inv(ECE569_Adjoint(M)), S2)
#     B3 = np.dot(np.linalg.inv(ECE569_Adjoint(M)), S3)
#     B4 = np.dot(np.linalg.inv(ECE569_Adjoint(M)), S4)
#     B5 = np.dot(np.linalg.inv(ECE569_Adjoint(M)), S5)
#     B6 = np.dot(np.linalg.inv(ECE569_Adjoint(M)), S6)
#     B = np.array([B1, B2, B3, B4, B5, B6]).T

#     theta0 = np.array([-1.6800, -1.4018, -1.8127, -2.9937, -0.8857, -0.0696])
    
#     T0_space = ECE569_FKinSpace(M, S, theta0)
#     print(f'T0_space:\n{T0_space}')
#     T0_body = ECE569_FKinBody(M, B, theta0)
#     print(f'T0_body:\n{T0_body}')
#     T0_diff = T0_space - T0_body
#     print(f'T0_diff:\n{T0_diff}')
#     T0 = T0_body

#     # calculate Tsd for each time step
#     # We want to draw on the z=0 plane of the S frame? 
#     # Usually lab instructions imply drawing on a plane defined relative to T0.
#     # The snippet implies Tsd = T0 * Td(t)
    
#     Tsd = np.zeros((4, 4, len(t)))
#     for i in range(len(t)):
#         # Define Td(t) as displacement from home
#         # p_d = [x[i], y[i], 0]
#         # T_d = [[I, p_d], [0, 1]]
#         Td = np.eye(4)
#         Td[0, 3] = x[i]
#         Td[1, 3] = y[i]
#         Td[2, 3] = 0 # Drawing plane z=0 relative to end effector start
        
#         # Tsd = T0 * Td
#         Tsd[:, :, i] = np.dot(T0, Td)
        
#     # plot p(t) vs t in the {s} frame
#     xs = Tsd[0, 3, :]
#     ys = Tsd[1, 3, :]
#     zs = Tsd[2, 3, :]
    
#     fig = plt.figure()
#     ax = fig.add_subplot(projection='3d')
#     ax.plot(xs, ys, zs, 'b-',label='p(t)')
#     ax.plot(xs[0], ys[0], zs[0], 'go',label='start')
#     ax.plot(xs[-1], ys[-1], zs[-1], 'rx',label='end')
#     ax.set_title('Trajectory in s frame')
#     ax.set_xlabel('x (m)')
#     ax.set_ylabel('y (m)')
#     ax.set_zlabel('z (m)')
#     ax.legend()
#     plt.show()

#     ### Step 3: Inverse Kinematics

#     # when i=0
#     thetaAll = np.zeros((6, len(t)))

#     initialguess = theta0
#     eomg = 1e-4 # Slightly relaxed tolerance for stability
#     ev = 1e-4

#     thetaSol, success = ECE569_IKinBody(B, M, Tsd[:,:,0], initialguess, eomg, ev)
#     if not success:
#         print(f"Warning: Failed to converge at start (index 0). Using guess.")
#         # raise Exception(f'Failed to find a solution at index {0}')
    
#     thetaAll[:, 0] = thetaSol

#     # when i=1...,N-1
#     for i in range(1, len(t)):
#         # Use previous solution as current guess
#         initialguess = thetaAll[:, i-1]

#         thetaSol, success = ECE569_IKinBody(B, M, Tsd[:,:,i], initialguess, eomg, ev)
        
#         if not success:
#              print(f'Failed to find a solution at index {i}')
#              # Fallback: keep previous theta
#              thetaSol = initialguess
             
#         thetaAll[:, i] = thetaSol

#     # verify that the joint angles don't change much
#     dj = np.diff(thetaAll, axis=1)
    
#     plt.figure()
#     plt.plot(t[1:], dj[0], 'b-',label='joint 1')
#     plt.plot(t[1:], dj[1], 'g-',label='joint 2')
#     plt.plot(t[1:], dj[2], 'r-',label='joint 3')
#     plt.plot(t[1:], dj[3], 'c-',label='joint 4')
#     plt.plot(t[1:], dj[4], 'm-',label='joint 5')
#     plt.plot(t[1:], dj[5], 'y-',label='joint 6')
#     plt.xlabel('t (seconds)')
#     plt.ylabel('first order difference')
#     plt.title('Joint angles first order difference')
#     plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
#     plt.grid()
#     plt.tight_layout()
#     plt.show()

#     # verify that the joint angles will trace out our trajectory
#     actual_Tsd = np.zeros((4, 4, len(t)))
#     for i in range(len(t)):
#         actual_Tsd[:,:,i] = ECE569_FKinSpace(M, S, thetaAll[:, i])
    
#     xs = actual_Tsd[0, 3, :]
#     ys = actual_Tsd[1, 3, :]
#     zs = actual_Tsd[2, 3, :]
    
#     fig = plt.figure()
#     ax = fig.add_subplot(projection='3d')
#     ax.plot(xs, ys, zs, 'b-',label='p(t)')
#     ax.plot(xs[0], ys[0], zs[0], 'go',label='start')
#     ax.plot(xs[-1], ys[-1], zs[-1], 'rx',label='end')
#     ax.set_xlabel('x (m)')
#     ax.set_ylabel('y (m)')
#     ax.set_zlabel('z (m)')
#     ax.set_title('Verified Trajectory in s frame')
#     ax.legend()
#     plt.show()
    
#     # (3e) verify the robot does not enter kinematic singularity
#     # by plotting the determinant of the body jacobian
#     body_dets = np.zeros(len(t))
#     for i in range(len(t)):
#         Jb = ECE569_JacobianBody(B, thetaAll[:, i])
#         body_dets[i] = np.linalg.det(Jb)
        
#     plt.figure()
#     plt.plot(t, body_dets, '-')
#     plt.xlabel('t (seconds)')
#     plt.ylabel('det of J_B')
#     plt.title('Manipulability')
#     plt.grid()
#     plt.tight_layout()
#     plt.show()

#     # save to csv file
#     # led = 1 means the led is on, led = 0 means the led is off
#     led = np.ones_like(t)
#     # Turn off LED during ramp up/down (first 1/5th and last 1/5th) if desired
#     # led[t < ta] = 0
#     # led[t > tfinal - ta] = 0
    
#     data = np.column_stack((t, thetaAll.T, led))
    
#     # Replace filename with your Purdue ID
#     filename = 'ydawanka.csv' 
#     print(f"Saving to {filename}...")
#     np.savetxt(filename, data, delimiter=',')
#     print("Done.")

# if __name__ == "__main__":
#     main()



import matplotlib.pyplot as plt
import numpy as np
import math

'''
*** BASIC HELPER FUNCTIONS ***
'''

def ECE569_NearZero(z):
    """Determines whether a scalar is small enough to be treated as zero"""
    return abs(z) < 1e-6

def ECE569_Normalize(V):
    """Normalizes a vector"""
    return V / np.linalg.norm(V)

'''
*** CHAPTER 3: RIGID-BODY MOTIONS ***
'''

def ECE569_RotInv(R):
    """Inverts a rotation matrix"""
    return np.array(R).T

def ECE569_VecToso3(omg):
    """Converts a 3-vector to an so(3) representation"""
    return np.array([[0,       -omg[2],  omg[1]],
                     [omg[2],       0, -omg[0]],
                     [-omg[1], omg[0],       0]])

def ECE569_so3ToVec(so3mat):
    """Converts an so(3) representation to a 3-vector"""
    return np.array([so3mat[2][1], so3mat[0][2], so3mat[1][0]])

def ECE569_AxisAng3(expc3):
    """Converts a 3-vector of exponential coordinates for rotation into axis-angle form"""
    return (ECE569_Normalize(expc3), np.linalg.norm(expc3))

def ECE569_MatrixExp3(so3mat):
    """Computes the matrix exponential of a matrix in so(3)"""
    omgtheta = ECE569_so3ToVec(so3mat)
    if ECE569_NearZero(np.linalg.norm(omgtheta)):
        return np.eye(3)
    else:
        theta = ECE569_AxisAng3(omgtheta)[1]
        omgmat = so3mat / theta
        return np.eye(3) + np.sin(theta) * omgmat \
               + (1 - np.cos(theta)) * np.dot(omgmat, omgmat)

def ECE569_MatrixLog3(R):
    """Computes the matrix logarithm of a rotation matrix"""
    acosinput = (np.trace(R) - 1) / 2.0
    if acosinput >= 1:
        return np.zeros((3, 3))
    elif acosinput <= -1:
        if not ECE569_NearZero(1 + R[2][2]):
            omg = (1.0 / np.sqrt(2 * (1 + R[2][2]))) \
                  * np.array([R[0][2], R[1][2], 1 + R[2][2]])
        elif not ECE569_NearZero(1 + R[1][1]):
            omg = (1.0 / np.sqrt(2 * (1 + R[1][1]))) \
                  * np.array([R[0][1], 1 + R[1][1], R[2][1]])
        else:
            omg = (1.0 / np.sqrt(2 * (1 + R[0][0]))) \
                  * np.array([1 + R[0][0], R[1][0], R[2][0]])
        return ECE569_VecToso3(np.pi * omg)
    else:
        theta = np.arccos(acosinput)
        return theta / 2.0 / np.sin(theta) * (R - np.array(R).T)

def ECE569_RpToTrans(R, p):
    """Converts a rotation matrix and a position vector into homogeneous transformation matrix"""
    return np.r_[np.c_[R, p], [[0, 0, 0, 1]]]

def ECE569_TransToRp(T):
    """Converts a homogeneous transformation matrix into a rotation matrix and position vector"""
    T = np.array(T)
    return T[0: 3, 0: 3], T[0: 3, 3]

def ECE569_TransInv(T):
    """Inverts a homogeneous transformation matrix"""
    R, p = ECE569_TransToRp(T)
    Rt = np.array(R).T
    return np.r_[np.c_[Rt, -np.dot(Rt, p)], [[0, 0, 0, 1]]]

def ECE569_VecTose3(V):
    """Converts a spatial velocity vector into a 4x4 matrix in se3"""
    # V = [omega, v]
    omega = V[0:3]
    v = V[3:6]
    so3 = ECE569_VecToso3(omega)
    return np.r_[np.c_[so3, v], [[0, 0, 0, 0]]]

def ECE569_se3ToVec(se3mat):
    """Converts an se3 matrix into a spatial velocity vector"""
    return np.r_[ECE569_so3ToVec(se3mat[0: 3, 0: 3]), se3mat[0: 3, 3]]

def ECE569_Adjoint(T):
    """Computes the adjoint representation of a homogeneous transformation matrix"""
    R, p = ECE569_TransToRp(T)
    p_so3 = ECE569_VecToso3(p)
    return np.r_[np.c_[R, np.zeros((3, 3))],
                 np.c_[np.dot(p_so3, R), R]]

def ECE569_MatrixExp6(se3mat):
    """Computes the matrix exponential of an se3 representation of exponential coordinates"""
    se3mat = np.array(se3mat)
    omgtheta = ECE569_so3ToVec(se3mat[0: 3, 0: 3])
    
    if ECE569_NearZero(np.linalg.norm(omgtheta)):
        return np.r_[np.c_[np.eye(3), se3mat[0: 3, 3]], [[0, 0, 0, 1]]]
    else:
        theta = ECE569_AxisAng3(omgtheta)[1]
        omgmat = se3mat[0: 3, 0: 3] / theta
        R = ECE569_MatrixExp3(se3mat[0: 3, 0: 3])
        v_vec = se3mat[0: 3, 3] / theta
        
        # G(theta) * v formula
        G_theta = np.eye(3) * theta + (1 - np.cos(theta)) * omgmat + \
                  (theta - np.sin(theta)) * np.dot(omgmat, omgmat)
        
        p = np.dot(G_theta, v_vec)
        return np.r_[np.c_[R, p], [[0, 0, 0, 1]]]

def ECE569_MatrixLog6(T):
    """Computes the matrix logarithm of a homogeneous transformation matrix"""
    R, p = ECE569_TransToRp(T)
    omgmat = ECE569_MatrixLog3(R)
    
    if np.array_equal(omgmat, np.zeros((3, 3))):
        return np.r_[np.c_[np.zeros((3, 3)), T[0: 3, 3]], [[0, 0, 0, 0]]]
    else:
        theta = np.arccos((np.trace(R) - 1) / 2.0)
        omgmat_norm = omgmat / theta
        
        G_inv = np.eye(3) / theta - 0.5 * omgmat_norm + \
                (1 / theta - 0.5 / np.tan(theta / 2)) * np.dot(omgmat_norm, omgmat_norm)
                
        v = np.dot(G_inv, p)
        se3_mat = np.r_[np.c_[omgmat, np.dot(G_inv, p) * theta], [[0, 0, 0, 0]]]
        return se3_mat

'''
*** CHAPTER 4: FORWARD KINEMATICS ***
'''

def ECE569_FKinBody(M, Blist, thetalist):
    """Computes forward kinematics in the body frame"""
    T = np.array(M)
    for i in range(len(thetalist)):
        # T = M * e^[B1]theta1 * ... * e^[Bn]thetan
        se3 = ECE569_VecTose3(Blist[:, i] * thetalist[i])
        T = np.dot(T, ECE569_MatrixExp6(se3))
    return T

def ECE569_FKinSpace(M, Slist, thetalist):
    """Computes forward kinematics in the space frame"""
    T = np.array(M)
    for i in range(len(thetalist) - 1, -1, -1):
        # T = e^[S1]theta1 * ... * e^[Sn]thetan * M
        se3 = ECE569_VecTose3(Slist[:, i] * thetalist[i])
        T = np.dot(ECE569_MatrixExp6(se3), T)
    return T

'''
*** CHAPTER 5: VELOCITY KINEMATICS AND STATICS***
'''

def ECE569_JacobianBody(Blist, thetalist):
    """Computes the body Jacobian for an open chain robot"""
    Jb = np.array(Blist).copy().astype(float)
    T = np.eye(4)
    # The last column is just Bn
    Jb[:, -1] = Blist[:, -1]
    
    # Iterate backwards from n-1 to 0
    for i in range(len(thetalist) - 2, -1, -1):
        # Transformation from frame i+1 to frame i due to joint i+1 rotation
        # Note: Blist column order is 0 to N-1
        se3 = ECE569_VecTose3(Blist[:, i+1] * -thetalist[i+1])
        T = np.dot(T, ECE569_MatrixExp6(se3))
        # Adjoint of the transformation product transforms the screw axis
        Jb[:, i] = np.dot(ECE569_Adjoint(T), Blist[:, i])
    return Jb

'''
*** CHAPTER 6: INVERSE KINEMATICS ***
'''

def ECE569_IKinBody(Blist, M, T, thetalist0, eomg, ev):
    """Computes inverse kinematics in the body frame"""
    thetalist = np.array(thetalist0).copy()
    i = 0
    maxiterations = 20
    
    # Calculate current configuration
    T_curr = ECE569_FKinBody(M, Blist, thetalist)
    # Calculate error twist Vb in body frame: [Ad_Tsb] * Vb = Vs -> Vb = log(T_sb^-1 * T_sd)
    T_diff = np.dot(ECE569_TransInv(T_curr), T)
    Vb_se3 = ECE569_MatrixLog6(T_diff)
    Vb = ECE569_se3ToVec(Vb_se3)
    
    err = np.linalg.norm([Vb[0], Vb[1], Vb[2]]) > eomg \
          or np.linalg.norm([Vb[3], Vb[4], Vb[5]]) > ev
          
    while err and i < maxiterations:
        # Calculate Jacobian
        Jb = ECE569_JacobianBody(Blist, thetalist)
        # Update theta: theta = theta + pinv(Jb) * Vb
        thetalist = thetalist + np.dot(np.linalg.pinv(Jb), Vb)
        
        i += 1
        # Recalculate error
        T_curr = ECE569_FKinBody(M, Blist, thetalist)
        T_diff = np.dot(ECE569_TransInv(T_curr), T)
        Vb_se3 = ECE569_MatrixLog6(T_diff)
        Vb = ECE569_se3ToVec(Vb_se3)
        
        err = np.linalg.norm([Vb[0], Vb[1], Vb[2]]) > eomg \
              or np.linalg.norm([Vb[3], Vb[4], Vb[5]]) > ev
              
    return (thetalist, not err)

def generate_segment_trajectory(start_pt, end_pt, velocity, dt, led_state):
    """Generates a linear trajectory between two points with constant velocity"""
    dist = np.linalg.norm(end_pt - start_pt)
    
    # Avoid division by zero for zero-length segments
    if dist < 1e-6:
        return np.array([start_pt]), np.array([led_state])
        
    duration = dist / velocity
    num_steps = int(np.ceil(duration / dt))
    
    # Linear interpolation
    t = np.linspace(0, 1, num_steps)
    traj_points = np.zeros((num_steps, 2))
    
    traj_points[:, 0] = start_pt[0] + t * (end_pt[0] - start_pt[0])
    traj_points[:, 1] = start_pt[1] + t * (end_pt[1] - start_pt[1])
    
    led_status = np.ones(num_steps) * led_state
    
    return traj_points, led_status

def transform_to_upright(points_2d):
    """
    Transforms 2D letter points (x,y) to 3D upright orientation.
    Plane: Vertical YZ plane in front of the robot.
    X_world = Fixed offset (reach)
    Y_world = x_local (Width)
    Z_world = y_local (Height)
    """
    x_local = points_2d[:, 0]
    y_local = points_2d[:, 1]
    
    num_pts = len(x_local)
    
    # Fixed forward distance (X)
    # Reduced to 0.20m to be safer and within reach
    x_world = np.ones(num_pts) * 0.20  # 20cm forward from base
    
    # Map width to Y (Side to Side)
    # Center the width at Y=0
    width_center = np.mean(x_local)
    y_world = x_local - width_center
    
    # Map height to Z (Up)
    # Lowered lift off. Min height at 0.05m
    z_offset = 0.05
    z_world = y_local + z_offset
    
    return x_world, y_world, z_world

def main():

    ### Step 1: Trajectory Generation (Purdue Block P - Refined)
    dt = 0.002
    target_velocity = 0.10 # Reduced to 0.10 m/s for smoother motion
    
    # Define Shape Parameters (Normalized Size 1.0)
    
    # Unskewed Block P Coordinates (x,y)
    # Normalized Height = 1.0
    stem_width = 0.35
    bowl_start_y = 0.40
    # Chamfer size for corners
    chamfer = 0.05
    
    # Outer Perimeter (CCW)
    # Start bottom left. Added precise geometry.
    raw_outer = np.array([
        [0.0, 0.0],          # Bottom Left
        [0.55, 0.0],         # Bottom-Right Serif Corner (Base)
        [0.55, 0.15],        # Up serif side
        [0.40, 0.15],        # In to Stem Right
        [0.40, 0.45],        # Up Stem to Bowl
        [0.85, 0.45],        # Out Bowl Bottom
        [1.0, 0.60],         # Bowl Bottom Chamfer
        [1.0, 0.85],         # Bowl Right Vertical
        [0.85, 1.0],         # Bowl Top Chamfer
        [0.0, 1.0],          # Top Left
        [0.0, 0.85],         # Down Top Serif Side
        [0.15, 0.85],        # In to Stem Left
        [0.15, 0.15],        # Down Stem Left
        [0.0, 0.15],         # Out to Bottom Serif Top
        [0.0, 0.0]           # Close
    ])
    
    # Inner Hole (CCW)
    # Uniform thickness approximations
    
    raw_inner = np.array([
        [0.45, 0.55],       # Bottom Left
        [0.70, 0.55],       # Bottom Right
        [0.75, 0.60],       # Chamfer
        [0.75, 0.80],       # Top Right
        [0.70, 0.85],       # Chamfer
        [0.45, 0.85],       # Top Left
        [0.45, 0.55]        # Close
    ])
    
    # Transformations
    # INCREASED SIZE to 22cm (0.22m)
    h_scale = 0.22 
    skew_factor = 0.4 # Horizontal shift per unit height (Italicize)
    
    # Apply Skew and Scale
    def transform_poly(poly):
        new_poly = np.zeros_like(poly)
        for i, pt in enumerate(poly):
            x, y = pt
            # Skew: x' = x + ky
            x_skew = x + skew_factor * y
            # Scale
            new_poly[i] = [x_skew * h_scale, y * h_scale]
        return new_poly

    outer_poly = transform_poly(raw_outer)
    inner_poly = transform_poly(raw_inner)
    
    # Generate full trajectory arrays
    x_full = []
    y_full = []
    led_full = []
    
    # 1. Trace Outer Loop (Twice)
    for _ in range(2):
        for i in range(len(outer_poly) - 1):
            pts, leds = generate_segment_trajectory(outer_poly[i], outer_poly[i+1], target_velocity, dt, 1)
            x_full.extend(pts[:,0])
            y_full.extend(pts[:,1])
            led_full.extend(leds)
        
    # 2. Transition to Inner Loop (LED OFF)
    # Move from end of outer loop to start of inner loop
    pts, leds = generate_segment_trajectory(outer_poly[-1], inner_poly[0], target_velocity, dt, 0)
    x_full.extend(pts[:,0])
    y_full.extend(pts[:,1])
    led_full.extend(leds)
    
    # 3. Trace Inner Loop (Twice)
    for _ in range(2):
        for i in range(len(inner_poly) - 1):
            pts, leds = generate_segment_trajectory(inner_poly[i], inner_poly[i+1], target_velocity, dt, 1)
            x_full.extend(pts[:,0])
            y_full.extend(pts[:,1])
            led_full.extend(leds)
        
    # Convert to arrays
    points_2d = np.column_stack((x_full, y_full))
    led = np.array(led_full)
    t = np.arange(0, len(points_2d) * dt, dt)
    
    # Ensure lengths match
    min_len = min(len(t), len(points_2d))
    t = t[:min_len]
    points_2d = points_2d[:min_len]
    led = led[:min_len]

    # Map to 3D "Upright" Space
    x_world, y_world, z_world = transform_to_upright(points_2d)

    # Plot 3D path for verification
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.plot(x_world[led==1], y_world[led==1], z_world[led==1], 'b-', label='Paint (LED ON)')
    ax.plot(x_world[led==0], y_world[led==0], z_world[led==0], 'r:', label='Move (LED OFF)')
    ax.set_title('3D Trajectory (Upright P)')
    ax.set_xlabel('X (Forward)')
    ax.set_ylabel('Y (Side)')
    ax.set_zlabel('Z (Up)')
    ax.legend()
    plt.show()

    ### Step 2: Forward Kinematics Setup
    L1 = 0.2435
    L2 = 0.2132
    W1 = 0.1311
    W2 = 0.0921
    H1 = 0.1519
    H2 = 0.0854

    M = np.array([[-1, 0, 0, L1 + L2],
                  [0, 0, 1, W1 + W2],
                  [0, 1, 0, H1 - H2],
                  [0, 0, 0, 1]])

    S1 = np.array([0, 0, 1, 0, 0, 0])
    S2 = np.array([0, 1, 0, -H1, 0, 0])
    S3 = np.array([0, 1, 0, -H1, 0, L1])
    S4 = np.array([0, 1, 0, -H1, 0, L1 + L2])
    S5 = np.array([0, 0, -1, -W1, L1+L2, 0])
    S6 = np.array([0, 1, 0, H2-H1, 0, L1+L2])
    S = np.array([S1, S2, S3, S4, S5, S6]).T
    
    B1 = np.dot(np.linalg.inv(ECE569_Adjoint(M)), S1)
    B2 = np.dot(np.linalg.inv(ECE569_Adjoint(M)), S2)
    B3 = np.dot(np.linalg.inv(ECE569_Adjoint(M)), S3)
    B4 = np.dot(np.linalg.inv(ECE569_Adjoint(M)), S4)
    B5 = np.dot(np.linalg.inv(ECE569_Adjoint(M)), S5)
    B6 = np.dot(np.linalg.inv(ECE569_Adjoint(M)), S6)
    B = np.array([B1, B2, B3, B4, B5, B6]).T

    theta0 = np.array([-1.6800, -1.4018, -1.8127, -2.9937, -0.8857, -0.0696])
    
    T0 = ECE569_FKinBody(M, B, theta0)

    # Calculate Tsd for each time step
    Tsd = np.zeros((4, 4, len(t)))
    
    # Base Orientation (Vertical Plane)
    # We want the end effector to point FORWARD (X) or DOWN (Z)?
    # Standard home orientation usually points X forward. 
    # Let's keep the rotation fixed to T0's rotation for simplicity, just moving position.
    R0 = T0[0:3, 0:3]

    for i in range(len(t)):
        Td = np.eye(4)
        Td[0:3, 0:3] = R0 # Keep orientation constant
        Td[0, 3] = x_world[i]
        Td[1, 3] = y_world[i]
        Td[2, 3] = z_world[i]
        
        # NOTE: Tsd is T_sb (Space to Body). 
        # If we just set position in space frame:
        Tsd[:, :, i] = Td

    ### Step 3: Inverse Kinematics
    thetaAll = np.zeros((6, len(t)))
    initialguess = theta0
    eomg = 1e-4
    ev = 1e-4

    # Initial Point
    thetaSol, success = ECE569_IKinBody(B, M, Tsd[:,:,0], initialguess, eomg, ev)
    if not success:
        print(f"Warning: Failed to converge at start (index 0). Using guess.")
    thetaAll[:, 0] = thetaSol

    # Path loop
    for i in range(1, len(t)):
        initialguess = thetaAll[:, i-1]
        thetaSol, success = ECE569_IKinBody(B, M, Tsd[:,:,i], initialguess, eomg, ev)
        
        if not success:
             print(f'Failed to find a solution at index {i}')
             thetaSol = initialguess # Fallback
             
        thetaAll[:, i] = thetaSol

    # Verify Joint Velocities (Safety Check)
    joint_velocities = np.diff(thetaAll, axis=1) / dt
    max_joint_vel = np.max(np.abs(joint_velocities))
    print(f"Max Joint Velocity: {max_joint_vel:.4f} rad/s")
    if max_joint_vel > 1.74: # ~100 deg/s
        print("WARNING: Joint velocity exceeds 100 deg/s limit!")

    # Plot Joint Angles First Order Difference
    dj = np.diff(thetaAll, axis=1)

    plt.figure()
    plt.plot(t[1:], dj[0], label='J1')
    plt.plot(t[1:], dj[1], label='J2')
    plt.plot(t[1:], dj[2], label='J3')
    plt.plot(t[1:], dj[3], label='J4')
    plt.plot(t[1:], dj[4], label='J5')
    plt.plot(t[1:], dj[5], label='J6')
    plt.xlabel('t (seconds)')
    plt.ylabel('First Order Difference (rad)')
    plt.title('Joint Angles First Order Difference')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()
    
    # Manipulability Check
    body_dets = np.zeros(len(t))
    for i in range(len(t)):
        Jb = ECE569_JacobianBody(B, thetaAll[:, i])
        body_dets[i] = np.linalg.det(Jb)
        
    plt.figure()
    plt.plot(t, body_dets, '-')
    plt.xlabel('t (seconds)')
    plt.ylabel('det of J_B')
    plt.title('Manipulability (Singularity Check)')
    plt.grid()
    plt.tight_layout()
    plt.show()

    # Save CSV
    if np.any(np.isinf(thetaAll)) or np.any(np.isnan(thetaAll)):
        print("ERROR: Computed joint angles contain Inf or NaN. CSV will not be saved.")
    else:
        data = np.column_stack((t, thetaAll.T, led))
        filename = 'ydawanka.csv' 
        print(f"Saving to {filename}...")
        np.savetxt(filename, data, delimiter=',')
        print("Done.")

if __name__ == "__main__":
    main()