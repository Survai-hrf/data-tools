# feed us an object detection and an action recognition model path, config
#run models on ground truth dataset
# extract statistics from results
# Print stats about performance on each grounfd truth attribute, on each detected class, and on entire dataset
#print those results out, visualize with graphs
# save all this in jsons in logs

# https://docs.google.com/document/d/1hzRCPs7wvhZ0B663hCZAO1Z6hN7rLpCgJfKYlmiEocI/edit?usp=sharing

import argparse

def parse_args():

    parser = argparse.ArgumentParser(
        description='Test models on the ground truth dataset')
    parser.add_argument('config', help='path to a model config')
    parser.add_argument('model', help='path to a model pth')
    args = parser.parse_args()
    return args

def create_folders():
    pass



if __name__ == '__main__':
    p = parse_args()
    print(p.config)
    print(p.model)
    # HERE create a new folder in logs in the format of 10-17-2022-114501 using the function create_folders



    #HERE 