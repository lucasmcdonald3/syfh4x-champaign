def get_bounding_boxes(response_dict):
    boxes = {} # key is person's index, value is bounding box for person
    for person in response_dict["Persons"]:
        box = person["BoundingBox"]
        boxes[person["Index"]] = (box["Left"], box["Width"], box["Top"], box["Height"])

def get_emotions(response_dict):
    emotions = {} # key is person's index, value is list of emotions (emotion = {Confidence, Type})
    for person in response_dict["Persons"]:
        emotions[person["Index"]] = person["Emotions"]