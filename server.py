import socket
import serverconfig as config
import select
import struct
import json
import cv2
import numpy as np

from boto import kinesis
from boto import kinesis 
from __future__ import division
import time

def read_kinesis(kinesis, shard_it):
    out = kinesis.get_records(shard_it, limit=2)
    for o in out["Records"]:
        jdat = json.loads(o["Data"])
        


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
    kinesis = kinesis.connect_to_region("us-west-2")
    shard_id = 'shardId-000000000000' #we only have one shard!
    shard_it = kinesis.get_shard_iterator("BotoDemo", shard_id, "LATEST")["ShardIterator"]

    while True:
        read_kinesis(kinesis, shard_it)
