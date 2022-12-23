import argparse
import json


def parse_args():
    parser = argparse.ArgumentParser(
        description='This script will create a new json with only the labels that you specify')
    parser.add_argument('--json-path', default="", help='path to coco json')
    parser.add_argument('--labels', default=[], nargs="*", help='REQUIRED: list of labels to include in json')
    args = parser.parse_args()
    return args


def create_json(json_path, labels):
    '''
    This script will take a given COCO json and create a new json given a list of category_id's to include. 
    '''
    int_labels = []
    for label in labels:
        label = int(label)
        int_labels.append(label)

    with open(json_path) as file:
        data = json.load(file)

    categories = [
        {
            "id": 0,
            "name": "uniformed"
        },
        {
            "id": 1,
            "name": "non_uniformed"
        },
        {
            "id": 2,
            "name": "riot_shield"
        },
        {
            "id": 3,
            "name": "gun"
        },
        {
            "id": 4,
            "name": "pepper_spray"
        },
        {
            "id": 5,
            "name": "baton"
        },
        {
            "id": 6,
            "name": "chemical_smoke"
        },
        {
            "id": 7,
            "name": "civilian_vehicle"
        },
        {
            "id": 8,
            "name": "emergency_vehicle"
        },
        {
            "id": 9,
            "name": "armored_vehicle"
        },
        {
            "id": 10,
            "name": "blade"
        }
    ]

    info = {"description": labels}

    # get all annotations for one class
    annotations = []
    count = 0
    for annot in data['annotations']:
        if annot['category_id'] in int_labels:
            annot['id'] = count
            annotations.append(annot)
            count += 1

    # get images
    images = []
    used_ids = []
    for annot in annotations:
        image_id = annot['image_id']

        if image_id in used_ids:
            continue
        else:
            used_ids.append(image_id)
            images.append(data['images'][image_id-1])
           
    output = {
        'info': info,
        'images': images,
        'annotations': annotations,
        'categories': categories
    }   

    with open("test.json", "w+") as file:
        json.dump(output, file)


if __name__ == '__main__':
    args = parse_args()
    create_json(args.json_path, args.labels)  