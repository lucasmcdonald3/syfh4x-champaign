import cv2

def background_subtraction(client_socket, vs):
    # open video
    cap = cv2.VideoCapture(0)
    # load stored background image for subtraction
    bg = cv2.imread("background.jpg")
    bg = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
    bg = cv2.GaussianBlur(bg, (5, 5), 0)
    while True:
        _, frame = cap.read()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)
    
        difference = cv2.absdiff(gray_frame, gray_frame)
        _, difference = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)

    return difference

def get_boxes(difference_frame):
    boxes = []
    ret, thresh = cv2.threshold(difference_frame, 127, 255, 0)
    (contours, hierarchy) = cv2.findContours(thresh, 1, 2)
    for contour, hier in zip(contours, hierarchy):
        (x,y,w,h) = cv2.boundingRect(contour)
        if w > 40 and h > 40:
            boxes.append(x, w+x, y, y+h)
    return boxes
