import csv
from operator import itemgetter, attrgetter
import server
import cv2
import numpy as np

width = 864
height = 648

def get_boxes(response_dict):
    boxes = {} # key is person's index, value is list of centers for person
    for person in response_dict["Persons"]:
        try:
            box = person["Person"]["BoundingBox"]
            if person["Person"]["Index"] not in boxes:
                boxes[person["Person"]["Index"]] = []
            boxes[person["Person"]["Index"]].append((box["Left"], box["Left"] + box["Width"], 1 - box["Top"], 1 - (box["Top"] + box["Height"]), person["Timestamp"]))
        except:
            continue
    # sort each box list
    for box_list in boxes.values():
        box_list = sorted(box_list, key=itemgetter(-1))
    # boxes = dict(key = person_index, value = (Left, Width, Top, Height, Timestamp))
    return boxes

def compute_proj_mtx(cam_mtx, rot_vec, trans_vec):
    #rotation vector to rotation vector
    rot_mtx, _ = cv2.Rodrigues(rot_vec)
    extrinsic = cv2.hconcat([rot_mtx, trans_vec])
    return np.matrix(cam_mtx) * np.matrix(extrinsic)

def undistort(point, camera_mtx, camera_dist):
    point = np.array([[[point[0], float(point[1])]]])	   
    #TODO look into use getOptimalNewCameraMatrix
    return cv2.undistortPoints(point, camera_mtx, camera_dist, P=camera_mtx)

def get_vector(point):
    cam_mtx, cam_dist, tran_vec, rot_vec = get_camera_info()
    proj = compute_proj_mtx(cam_mtx, rot_vec, tran_vec)
    undist = undistort(point, cam_mtx, cam_dist)
    proj_inv = np.linalg.pinv(cam_mtx)
    #backproject using pseudo inverse
    ray = proj_inv*np.matrix([[undist[0][0][0]],[undist[0][0][1]],[1]])
    #print(ray)
    #convert from homegenous to cartesian
    return np.array([ray.item(0),ray.item(1),ray.item(2)])

def get_camera_info():
    scale_mtx = np.matrix([
        [.5, 0, 0],
        [0, .5, 0],
        [0, 0, 1]
    ])
    camera_mtx = np.asmatrix(np.loadtxt("calibration/cameramatrix.txt"))
    camera_mtx = scale_mtx * camera_mtx
    camera_dist = np.loadtxt("calibration/cameradistortion.txt")
    rot_vec = np.loadtxt("calibration/rotationvector.txt")
    tran_vec = np.loadtxt("calibration/translationvector.txt")
    return (camera_mtx, camera_dist, tran_vec, rot_vec)

def get_point(point2d):
    cam_pos = get_camera_pos()
    ray = get_vector(point2d)
    ray = (ray.item(0)+cam_pos.item(0),ray.item(1)+cam_pos.item(1),ray.item(2)+cam_pos.item(2))
    normal = (0,0,1)
    t = -np.dot(cam_pos,normal)/np.dot(ray,normal)
    ground_pos = cam_pos + t*ray
    return ground_pos

def boxes_to_points(tracking_info):
    position_dict = {}
    for index, boxes in tracking_info.items():
        position_dict[index] = []
        for box in boxes:
            cam_point = ((box[0] * width + box[1]*width)/2,box[3]*height)
            point = get_point(cam_point).reshape(1,3)
            position_dict[index].append((point[0][0], point[0][1]))
    return position_dict

def get_camera_pos():
    cam_mtx, cam_dist, trans_vec, rot_vec = get_camera_info()
    rot_mtx, _ = cv2.Rodrigues(rot_vec)
    trans_vec = trans_vec.reshape(3,1)
    return np.dot(-rot_mtx.T,trans_vec.reshape(3,1)).reshape(1,3)

# writes info_dict to file. info_dict has (key = index, value = list of info to store)
def write_data(info_dict):
    for index, info in info_dict.items():
        with open("logs/{}.csv".format(index), 'a+') as f:
            writer = csv.writer(f)
            writer.writerow(info)