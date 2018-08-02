import csv

def get_bounding_boxes(response_dict):
    boxes = {} # key is person's index, value is bounding box for person
    for person in response_dict["Persons"]:
        box = person["BoundingBox"]
        boxes[person["Index"]] = (box["Left"], box["Width"], box["Top"], box["Height"])

# writes info_dict to file. info_dict has (key = index, value = list of info to store)
def write_data(info_dict):
    for index, info in info_dict.items():
        with open("logs/{}.csv".format(index), 'a+') as f:
            writer = csv.writer(f)
            writer.writerow(info)