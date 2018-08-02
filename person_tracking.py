import csv
from operator import itemgetter, attrgetter

def get_boxes(response_dict):
    boxes = {} # key is person's index, value is list of centers for person
    for person in response_dict["Persons"]:
        box = person["Person"]["BoundingBox"]
        if person["Person"]["Index"] not in boxes:
            boxes[person["Person"]["Index"]] = []
        boxes[person["Person"]["Index"]].append((box["Left"], box["Width"], box["Top"], box["Height"], person["Timestamp"]))
    # sort each box list
    for box_list in boxes.values():
        box_list = sorted(box_list, key=itemgetter(-1))
    return boxes

# writes info_dict to file. info_dict has (key = index, value = list of info to store)
def write_data(info_dict):
    for index, info in info_dict.items():
        with open("logs/{}.csv".format(index), 'a+') as f:
            writer = csv.writer(f)
            writer.writerow(info)