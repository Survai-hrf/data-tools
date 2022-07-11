


#HOW TO RUN: specifiying optional path: python args_example.py sadg/sdg/ --video_id sdg//sdg/sdg/
            #without specifiying optional path: python args_example.py sadg/sdg/

import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description='MMAction2 predict different labels in a long video demo')
    parser.add_argument('mux_url', help='mux url, writes out detections.json to processed/(VIDEO_ID)/')
    parser.add_argument('--video_id', default='/', help='id to video to update table to', )

    args = parser.parse_args()
    return args







def processvideo(mux_url, video_id):

    print(mux_url)
    print(video_id)
    #all coding logic here
    return


if __name__ == '__main__':
    args = parse_args()
    processvideo(args.mux_url, args.video_id)