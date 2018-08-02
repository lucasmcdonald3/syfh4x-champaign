import numpy as np
import cv2 

def get_cam_pos(trans_vec, rot_vec):
    rot_mtx, _ = cv2.Rodrigues(rot_vec)
    trans_vec = trans_vec.reshape(3,1)
    return np.dot(-rot_mtx.T,trans_vec.reshape(3,1))

def get_trans_vec(pos, rot_vec):
    rot_mtx, _ = cv2.Rodrigues(rot_vec)
    return -np.dot(rot_mtx, pos)

camera_mtx = np.asmatrix(np.loadtxt("../calibration/cameramatrix.txt"))
camera_dist = np.loadtxt("../calibration/cameradistortion.txt")
rot_vec = np.loadtxt("../calibration/rotationvector.txt")
trans_vec = np.loadtxt("../calibration/translationvector.txt")

pos = get_cam_pos(trans_vec, rot_vec)
print(pos)

x_offset = float(input("X offset: "))
y_offset = float(input("Y offset: "))
z_offset = float(input("Z offset: "))

pos[0][0] += x_offset
pos[1][0] += y_offset
pos[2][0] += z_offset

print(pos)
new_trans_vec = get_trans_vec(pos, rot_vec)
print("New translation vector")
print(new_trans_vec)
save_input = input("Save? press y: ")
if save_input.lower() == "y":
    np.savetxt("translationvector.txt", new_trans_vec)

'''
.885825
.796925
0
'''
