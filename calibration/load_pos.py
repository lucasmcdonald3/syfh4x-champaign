import numpy as np
import cv2

def get_cam_pos(camera_mtx, camera_dist, trans_vec, rot_vec):
    rot_mtx, _ = cv2.Rodrigues(rot_vec)
    trans_vec = trans_vec.reshape(3,1)
    return np.dot(-rot_mtx.T,trans_vec.reshape(3,1))

#create matrix to scale intrinsic matrix down 1/6
#scale_mtx = np.matrix([[.5, 0, 0], [0, .5, 0], [0, 0, 1]])
camera_mtx = np.asmatrix(np.loadtxt("../calibration/cameramatrix.txt"))
camera_dist = np.loadtxt("../calibration/cameradistortion.txt")
rot_vec = np.loadtxt("../calibration/rotationvector.txt")
trans_vec = np.loadtxt("../calibration/translationvector.txt")

#scale intrinsic matrix because we are detecting on image 1/6 the original resolution
#camera_mtx = scale_mtx * camera_mtx

print(get_cam_pos(camera_mtx, camera_dist, trans_vec, rot_vec))