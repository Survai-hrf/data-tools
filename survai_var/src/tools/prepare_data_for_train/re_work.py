import argparse
import os
from pytube import YouTube
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import pandas as pd
from pytube.exceptions import VideoUnavailable
import distutils.dir_util
import shutil


def parse_args():
    parser = argparse.ArgumentParser(
        description='This script will download videos and train val split them from a given csv')
    parser.add_argument('csv_path', help='path to csv you want to download videos from')
    parser.add_argument('--split_path', default='/', help='path to place train val split folders')
    parser.add_argument('--clarity_level', default=['none', 'easy', 'medium', 'hard', 'bad'], nargs="*", help='takes a list of clarity levels to prepare. All options ex: ["none","easy","medium","hard","bad_egg"]')
    args = parser.parse_args()
    return args

def download_videos(csv_path, split_path, clarity_level):

    if os.path.exists(split_path): shutil.rmtree(split_path) # delete split_path

    # Read csv, clean data
    df = pd.read_csv(csv_path)
    df = df.reset_index()
    df['clarity_level'] = df['clarity_level'].fillna('none') 
    df['split'] = 'train'
    df = df.head(300)

    # open label_map.txt, create list of labels with their index as key
    txt = open('label_map.txt', 'r')
    lines = [s.strip('\n')for s in txt]
    txt.close()
    label_map = dict((index, label) for label, index in enumerate(lines, start=1))
    broken_videos = list()


    # define function for both initial and retry of download
    def download(url, file_name, label, start, end, fill_start, fill_end):

        video = YouTube(url)
        yt_video = video.streams.get_highest_resolution()
        yt_video.download(output_path=f'master_videos/{label}/', filename=f"{file_name}.mp4")
        # download videos into correct folder
        ffmpeg_extract_subclip(filename=f'master_videos/{label}/{file_name}.mp4', t1=start, t2=end, 
                                targetname=f'master_videos/{label}/{file_name}_{fill_start}_{fill_end}.mp4') 
        os.remove(f'master_videos/{label}/{file_name}.mp4') 


    # iterates all videos in df and downloads them to 'master_videos' folder
    for index, row in df.iterrows():

        file_name = str(row['id'])
        start = int(row['time_start'])
        end = int(row['time_end'])
        label = str(row['label'])
        url = f'https://www.youtube.com/watch?v={file_name[0:11]}'
        fill_start = str(start).zfill(6) # make times the same number of digits
        fill_end = str(end).zfill(6)

        # ignore bad labels and bad videos
        if label not in label_map.keys(): 
            df.drop(index, inplace=True)
            continue 

        # makes sure videos that were previously downloaded don't get downloaded again
        if os.path.exists(f"master_videos/{label}/{file_name}_{fill_start}_{fill_end}.mp4"):
            print('file already exists')
            continue

        attempts = 0
        while attempts < 3: 
            try: 
                download(url, file_name, label, start, end, fill_start, fill_end)
                break
            except:
                print('retrying...', file_name)
                attempts = attempts+1
                continue
        else:  
            print('BROKEN VIDEO: ', file_name)
            broken_videos.append(file_name) # add broken videos to array to be deleted


    # drop videos from df that did not download
    for video in broken_videos: df = df.drop(df.loc[df['id'] == video].index)

    # drop rows with clarity levels not included in list of clarity levels, and labels not in label map
    for index, row in df.iterrows(): 
        if row['clarity_level'] not in clarity_level: df.drop(index, inplace=True)

    # set val split for each class equal to 35% of the class with the least amount of rows
    least_label = int(df['label'].value_counts().min()*0.50) # CHANGE BACK TO 35% AFTER TESTING
    df_val = df.groupby('label').apply(lambda x: x.sample(n=1, replace=False)) 
    df_val['split'] = 'val'
    cond = df['id'].isin(df_val['id'])
    df.drop(df[cond].index, inplace = True)
    df = pd.concat([df, df_val], ignore_index=True)


    val_list = []
    train_list = []

    for index, row in df.iterrows():
        
        file_name = str(row['id'])
        start = int(row['time_start'])
        end = int(row['time_end'])
        label = str(row['label'])
        url = f'https://www.youtube.com/watch?v={file_name[0:11]}'
        fill_start = str(start).zfill(6) # make times the same number of digits
        fill_end = str(end).zfill(6)
        class_num = label_map.get(label)
        split = row['split']

        # create directories to split videos into val and train
        val_path = f'{split_path}/val/{label}'
        train_path = f'{split_path}/train/{label}'

        if not os.path.exists(val_path): os.makedirs(val_path)
        if not os.path.exists(train_path): os.makedirs(train_path)

        if split == 'val':
            shutil.copyfile(f"master_videos/{label}/{file_name}_{fill_start}_{fill_end}.mp4", 
                                f"{val_path}/{file_name}_{fill_start}_{fill_end}.mp4")
            val_list.append(f"{label}/{file_name}_{fill_start}_{fill_end}.mp4 {class_num}")
            
        if split == 'train':
            shutil.copyfile(f"master_videos/{label}/{file_name}_{fill_start}_{fill_end}.mp4", 
                                f"{train_path}/{file_name}_{fill_start}_{fill_end}.mp4")
            train_list.append(f"{label}/{file_name}_{fill_start}_{fill_end}.mp4 {class_num}")

    # create val_list and train_list txt's  
    with open(f'{split_path}/val_list.txt', 'w') as val_file, open(f'{split_path}/train_list.txt', 'w') as train_file:
        for file_name in val_list:
            val_file.write(f"{file_name}\n")
        for file_name in train_list:
            train_file.write(f"{file_name}\n")


if __name__ == '__main__':
    args = parse_args()
    download_videos(args.csv_path, args.split_path, args.clarity_level)