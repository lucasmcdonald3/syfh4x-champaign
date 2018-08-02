from socket import socket
import clientconfig as config
import numpy as np
import json
import cv2
import imutils
from imutils.video import VideoStream
import struct
import time

def send_msg(target_socket, msg):
    msg = msg.encode()
    msg = struct.pack('>I', len(msg)) + msg
    target_socket.sendall(msg)

def setup():
    #set up socket
    client_socket = socket()
    client_socket.connect((config.IP, config.PORT))

    # load saved camera information
    camera_mtx = np.asmatrix(np.loadtxt("calibration/cameramatrix.txt"))
    camera_dist = np.loadtxt("calibration/cameradistortion.txt")
    rot_vec = np.loadtxt("calibration/rotationvector.txt")
    trans_vec = np.loadtxt("calibration/translationvector.txt")
    # send camera info
    camera_data = json.dumps({
        "camera_mtx": camera_mtx.tolist(),
        "camera_dist": camera_dist.tolist(),
        "rot_vec": rot_vec.tolist(),
        "trans_vec": trans_vec.tolist()
    })
    send_msg(client_socket, camera_data)
    # set up video stream
    print("[INFO] starting video stream...")
    vs = cv2.VideoCapture(0)
    time.sleep(1.0)

    return (client_socket, vs)

def detection(client_socket, vs):
    while True:
            # Send this to the server
        data = json.dumps([{"x":836,"y":1788}])
        try:
            send_msg(client_socket, data)
        except:
            pass 


def main():
    (client_socket, vs) = setup()
    detection(client_socket, vs)

if __name__ == '__main__':
    main()
