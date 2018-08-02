import socket
import select
import struct
import json
import cv2
import numpy as np

def recv_msg(sock):
    #Read msg length which is 4 bytes long
    raw_msglen = recv_all(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    return recv_all(sock, msglen)

def recv_all(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def compute_proj_mtx(cam_mtx, rot_vec, trans_vec):
    #rotation vector to rotation vector
    rot_mtx, _ = cv2.Rodrigues(rot_vec)
    extrinsic = cv2.hconcat([rot_mtx, trans_vec])
    return np.matrix(cam_mtx) * np.matrix(extrinsic)

def undistort(point, camera_mtx, camera_dist):
    point = np.array([[[point[0], float(point[1])]]])	   
    #TODO look into use getOptimalNewCameraMatrix
    return cv2.undistortPoints(point, camera_mtx, camera_dist, P=camera_mtx)

def get_vector(point, picamera_info):
    cam_mtx, cam_dist, tran_vec, rot_vec = get_camera_info(picamera_info)
    proj = compute_proj_mtx(cam_mtx, rot_vec, tran_vec)
    undist = undistort(point, cam_mtx, cam_dist)
    proj_inv = np.linalg.pinv(proj)
    #backproject using pseudo inverse
    ray = proj_inv*np.matrix([[undist[0][0][0]],[undist[0][0][1]],[1]])
    #convert from homegenous to cartesian
    return np.array([ray.item(0)/ray.item(3),ray.item(1)/ray.item(3),ray.item(2)/ray.item(3)])

def get_camera_info(picamera):
    camera_mtx = np.array(picamera.get("camera_mtx")).reshape(3,3)
    camera_dist = np.array(picamera.get("camera_dist"))
    tran_vec = np.array(picamera.get("trans_vec"))
    rot_vec = np.array(picamera.get("rot_vec"))
    return (camera_mtx, camera_dist, tran_vec, rot_vec)

def get_point(picamera_info, point2d):
    cam_pos = get_camera_pos(picamera_info)
    ray = get_vector(point2d, picamera_info)
    normal = (0,0,1)
    t = -np.dot(cam_pos,normal)/np.dot(ray,normal)
    ground_pos = cam_pos + t*ray
    return ground_pos


def get_camera_pos(picamera_info):
    cam_mtx, cam_dist, trans_vec, rot_vec = get_camera_info(picamera_info)
    rot_mtx, _ = cv2.Rodrigues(rot_vec)
    trans_vec = trans_vec.reshape(3,1)
    return np.dot(-rot_mtx.T,trans_vec.reshape(3,1)).reshape(1,3)

def main():
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('', 2018))
    server_socket.listen(2)
    input_sockets = [server_socket]

    picameras_info = {}

    while True:
        input_fds = select.select(input_sockets, input_sockets, [], 2)[0]

        for fd in input_fds:
            if fd is server_socket:
                client_socket, client_address = fd.accept()
                input_sockets.append(client_socket)
                print("Connected to ", client_address)
            else:
                try:
                    data = recv_msg(fd)
                    if not data:
                        input_sockets.remove(fds)
                    source_address = fd.getpeername()[0]
                    source_data = json.loads(data.decode())
                    if type(source_data) is not list:
                        picameras_info[source_address] = source_data
                    else:
                        for point2d in source_data:
                            point3d = get_point(picameras_info[source_address], point2d)
                            print("Final Point", str(point3d))
                except:
                    continue

if __name__ == "__main__":
    main()
