import pickle

def get_bounding_boxes(response_dict):
    boxes = {} # key is person's index, value is bounding box for person
    for person in response_dict["Persons"]:
        box = person["BoundingBox"]
        boxes[person["Index"]] = (box["Left"], box["Width"], box["Top"], box["Height"])

def write_data(info_dict):
    for index, info in info_dict.items():
        with open("logs/{}.txt".format(index), 'a') as f:
            pickle.dump(info, f)