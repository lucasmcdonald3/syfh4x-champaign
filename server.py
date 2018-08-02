import socket
import serverconfig as config
import select
import struct
import json
import cv2
import numpy as np

def recv_msg(source_socket):
    buf = source_socket.recv(4096)
    cursor = 0
    buf_len = len(buf)
    while cursor < buf_len:
        message_length = struct.unpack('>I', buf[cursor:cursor+4])[0]
        cursor += 4 # 4 bytes
        if cursor + message_length == buf_len:
            return buf[cursor:]
        elif cursor + buf_len > buf_len:
            # receive next buffer
            buf = source_socket.recv(4096)
            cursor = 0
            buf_len = len(buf)

def get_camera_info(picamera):
    camera_mtx = np.array(picamera.get("camera_mtx")).reshape(3,3)
    camera_dist = np.array(picamera.get("camera_dist"))
    tran_vec = np.array(picamera.get("trans_vec"))
    rot_vec = np.array(picamera.get("rot_vec"))
    return (camera_mtx, camera_dist, tran_vec, rot_vec)

def get_point(picamera_info, source_data):
    cam_pos = get_camera_pos(picamera_info)
    normal = (0,0,1)
    t = -np.dot(cam_pos,normal)/np.dot(ray,normal)
    ground_pos = cam_pos + t*ray
    return ground_pos


def get_camera_pos(picamera_info):
    cam_mtx, cam_dist, trans_vec, rot_vec = get_camera_info(picamera_info)
    rot_mtx, _ = cv2.Rodrigues(rot_vec)
    trans_vec = trans_vec.reshape(3,1)
    return np.dot(-rot_mtx.T,trans_vec.reshape(3,1))

def main():
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('', config.PORT))
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
                    source_address = fd.getpeername()[0]
                    source_data = json.loads(data.decode())
                    if type(source_data) is not list:
                        print("source_data:", str(source_data))
                        picameras_info[source_address] = source_data
                    point = get_point(picameras_info[source_address], source_data)
                    print(point)
                    
                except:
                    continue
