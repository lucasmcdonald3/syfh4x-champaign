from socket import socket
import serverconfig as config
import numpy as np
import json

def setup():
    #set up socket
    client_socket = socket.socket()
    client_socket.connect((config.IP, config.PORT))

    scale_mtx = np.matrix([
        [.5, 0, 0],
        [0, .5, 0],
        [0, 0,  1]
    ])
    # load saved camera information
    camera_mtx = np.asmatrix(np.loadtxt("calibration/cameramatrix.txt"))
    camera_dist = np.loadtxt("calibration/cameradistortion.txt")
    rot_vec = np.loadtxt("calibration/rotationvector.txt")
    trans_vec = np.loadtxt("calibration/translationvector.txt")
    # scale camera matrix by resolution decrease
    camera_mtx = scale_mtx * camera_mtx
    # send camera info
    camera_data = json.dumps({
        "camera_mtx": camera_mtx.tolist(),
        "camera_dist": camera_dist.tolist(),
        "rot_vec": rot_vec.tolist(),
        "trans_vec": trans_vec.tolist()
    })
    send_msg(sock, camera_data)
    # set up video stream
    print("[INFO] starting video stream...")
    vs = cv2.VideoCapture(0)
    time.sleep(1.0)

    return (sock, vs)

def detection(client_socket, vs):
    print("[INFO] loading model...")
    net = cv2.dnn.readNetFromCaffe(config.PROTOTXT, config.MODEL)
    while True:
        centers = []
        # get frame from video feed
        ret, frame = vs.read()
        if ret == False:
            continue
        frame = imutils.resize(frame, width=config.PICTURE_WIDTH)
        # convert frame to neural net input format
        blob = cv2.dnn.blobFromImage(
                    frame,
                    config.MOBILENET_SCALE_FACTOR,
                    (config.MOBILENET_IMAGE_WIDTH, config.MOBILENET_IMAGE_HEIGHT),
                    config.MOBILENET_IMAGE_MEDIAN
                )
        net.setInput(blob)
        detections = net.forward()

        # loop over the detections
        for result_index in np.arange(0, detections.shape[2]):
            class_index = int(detections[0, 0, result_index, 1])
            if class_index == 15: # person class index # for mobilenet
                box = detections[0, 0, result_index,
                                            3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                # append center of bbox as tuple (x, y)
                centers.append(((startX + endX) / 2, (startY + endY) / 2))

        # Send this to the server
        data = json.dumps(centers)
        try:
            send_msg(client_socket, data)
        except:
            pass 


def main():
    (client_socket, vs) = setup_device()
    object_tracking(client_socket, vs)

if __name__ == '__main__':
    main()