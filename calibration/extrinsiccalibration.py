import numpy as np
import cv2
import cv2.aruco as aruco

marker_length = .20955 #in meters
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)

#load intrinsic
camera_mtx = np.asmatrix(np.loadtxt("cameramatrix.txt"))
camera_dist = np.loadtxt("cameradistortion.txt")

img = cv2.imread("aruco.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

parameters =  aruco.DetectorParameters_create()

#find markers
corners, idx, rejected = aruco.detectMarkers(gray, aruco_dict, parameters = parameters)
print(corners)

img = aruco.drawDetectedMarkers(img, corners)
for rect in rejected:
    print("Rect:" + str(rect))
    for point in rect[0]:
        cv2.circle(img, (point[0],point[1]), 2, (0,255,0),-1)

#get pose
rvecs, tvecs, obj_points = aruco.estimatePoseSingleMarkers(corners, marker_length, camera_mtx, camera_dist)

#save rotation and translation
np.savetxt("rotationvector.txt",rvecs[0])
np.savetxt("translationvector.txt",tvecs[0])
img = aruco.drawAxis(img, camera_mtx, camera_dist, rvecs, tvecs, .1) 

cv2.destroyAllWindows()
