import os
from google.cloud import storage
import argparse
from pytube import YouTube
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import pandas as pd
from pytube.exceptions import VideoUnavailable

<<<<<<< HEAD
=======
'''
The following command will upload videos to a gcloud storage bucket from the csv titled "var_data.csv" 
and split the videos with clarity levels "none", "easy", "medium", and "hard"into a folder titled "split". 

EXAMPLE COMMAND: python gcloud_upload.py var_data.csv --split_path split --clarity_level none easy medium hard
'''
>>>>>>> 3e583ac3aea71d068ac170fa6f36b82bc5d005b2

def parse_args():
    parser = argparse.ArgumentParser(
        description='This script will download videos and train val split them from a given csv')
    parser.add_argument('csv_path', help='path to csv you want to download videos from')
<<<<<<< HEAD
    parser.add_argument('--split-path', default='', help='path to place train val split folders')
    parser.add_argument('--clarity-level', default=['none', 'easy', 'medium', 'hard', 'bad'], nargs="*", help='takes a list of clarity levels to prepare. All options ex: ["none","easy","medium","hard","bad_egg"]')
=======
    parser.add_argument('--split_path', default='/', help='path to place train val split folders')
    parser.add_argument('--clarity_level', default=['none', 'easy', 'medium', 'hard', 'bad'], nargs="*", help='takes a list of clarity levels to prepare. All options ex: ["none","easy","medium","hard","bad_egg"]')
>>>>>>> 3e583ac3aea71d068ac170fa6f36b82bc5d005b2
    args = parser.parse_args()
    return args

def download_videos(csv_path, split_path, clarity_level):

    # connect to gcloud bucket
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'survai-data-connect.json'
    storage_client = storage.Client()
<<<<<<< HEAD
    bucket_name = 'survai-dataset'

    # delete old split
    blobs = storage_client.list_blobs(bucket_name, prefix='datasets/var/split/')
=======
    my_bucket = storage_client.get_bucket('survai-dataset')

    # delete old split
    blobs = storage_client.list_blobs('survai-dataset', prefix='datasets/var/split/')
>>>>>>> 3e583ac3aea71d068ac170fa6f36b82bc5d005b2
    for blob in blobs: blob.delete()

    # read csv, clean data
    df = pd.read_csv(csv_path)
    df = df.reset_index()
    df['clarity_level'] = df['clarity_level'].fillna('none') 
    df['split'] = 'train'
<<<<<<< HEAD
=======
    df = df.head(25)
>>>>>>> 3e583ac3aea71d068ac170fa6f36b82bc5d005b2

    # open label_map.txt, create list of labels with their index as key
    txt = open('label_map.txt', 'r')
    lines = [s.strip('\n')for s in txt]
    txt.close()
    label_map = dict((index, label) for label, index in enumerate(lines, start=1))
    broken_videos = []

<<<<<<< HEAD
    videos = storage_client.list_blobs(bucket_name, prefix='datasets/var/master_videos/')
    video_list = [video.name for video in videos]

    has_dash = False

    # function to download videos
    def download(url, file_name): 
        video = YouTube(url, use_oauth=True, allow_oauth_cache=True) 
        yt_video = video.streams.get_highest_resolution()
        yt_video.download(output_path='', filename=f"{file_name}.mp4")

    def subclip(file_name, start, end, fill_start, fill_end):
        '''function to extract subclip'''
        ffmpeg_extract_subclip(filename=f'{file_name}.mp4', t1=start, t2=end, 
                                targetname=f'{file_name}_{fill_start}_{fill_end}.mp4') 
        os.remove(f'{file_name}.mp4') 
=======
    
    # function to download videos
    def download(url, file_name, start, end, fill_start, fill_end):
        attempts = 0
        while attempts < 3: 
            try: 
                video = YouTube(url)
                yt_video = video.streams.get_highest_resolution()
                yt_video.download(output_path='', filename=f"{file_name}.mp4")
                ffmpeg_extract_subclip(filename=f'{file_name}.mp4', t1=start, t2=end, 
                                        targetname=f'{file_name}_{fill_start}_{fill_end}.mp4') 
                os.remove(f'{file_name}.mp4') 
                break
            except:
                print('retrying...', file_name)
                attempts += 1
                continue
        else:  
            print('BROKEN VIDEO: ', file_name)
            broken_videos.append(file_name) # add broken videos to array to be deleted
>>>>>>> 3e583ac3aea71d068ac170fa6f36b82bc5d005b2
        
    # function to upload videos to gcloud bucket
    def upload_to_bucket(blob_name, file_path, bucket_name):
        try:
            bucket = storage_client.get_bucket(bucket_name)
            blob = bucket.blob(blob_name)
            blob.upload_from_filename(file_path)
        except Exception as e:
            print(e)

    
    # iterates all videos in df and downloads them to 'master_videos' folder
    for index, row in df.iterrows():

        file_name = str(row['id'])
        start = int(row['time_start'])
        end = int(row['time_end'])
        label = str(row['label'])
        url = f'https://www.youtube.com/watch?v={file_name[0:11]}'
        fill_start = str(start).zfill(6) # make times the same number of digits
        fill_end = str(end).zfill(6)

<<<<<<< HEAD
        # ignore labels not in label map
=======
        # ignore bad labels and bad videos
>>>>>>> 3e583ac3aea71d068ac170fa6f36b82bc5d005b2
        if label not in label_map.keys(): 
            df.drop(index, inplace=True)
            continue 
        
        # check if file already exists in gcloud storage bucket
<<<<<<< HEAD
        if f"datasets/var/master_videos/{label}/{file_name}_{fill_start}_{fill_end}.mp4" in video_list:
            print('file already exists', file_name)
            continue
        
        attempts = 0
        while attempts < 1: 
            try: 
                download(url, file_name)

                if file_name[0] == '-':
                    has_dash = True
                    os.rename(f'{file_name}.mp4', f'{file_name[1:]}.mp4')
                    file_name = file_name[1:]

                subclip(file_name, start, end, fill_start, fill_end)
                if has_dash == True:
                    os.rename(f'{file_name}_{fill_start}_{fill_end}.mp4', 
                                f'-{file_name}_{fill_start}_{fill_end}.mp4')
                    file_name = '-' + file_name
                    has_dash = False
                break
            except:
                print('retrying...', file_name)
                attempts += 1
                continue
        else:  
            print('BROKEN VIDEO: ', file_name)
            broken_videos.append(file_name) # add broken videos to array to be deleted
            continue

        upload_to_bucket(f'datasets/var/master_videos/{label}/{file_name}_{fill_start}_{fill_end}.mp4', 
                            f"{file_name}_{fill_start}_{fill_end}.mp4", bucket_name)
=======
        videos = storage_client.list_blobs('survai-dataset', prefix='datasets/var/master_videos/')
        video_list = [video.name for video in videos]
        if f"datasets/var/master_videos/{label}/{file_name}_{fill_start}_{fill_end}.mp4" in video_list:
            print('file already exists')
            continue
        
        download(url, file_name, start, end, fill_start, fill_end)
        upload_to_bucket(f'datasets/var/master_videos/{label}/{file_name}_{fill_start}_{fill_end}.mp4', 
                            f"{file_name}_{fill_start}_{fill_end}.mp4", 'survai-dataset')
>>>>>>> 3e583ac3aea71d068ac170fa6f36b82bc5d005b2
        os.remove(f"{file_name}_{fill_start}_{fill_end}.mp4")


    # filter df and create train and val split
<<<<<<< HEAD
    print(len(broken_videos))
=======
>>>>>>> 3e583ac3aea71d068ac170fa6f36b82bc5d005b2
    for video in broken_videos: 
        df = df.drop(df.loc[df['id'] == video].index) # drop videos from df that did not download

    # drop rows with clarity levels not included in list of clarity levels
    for index, row in df.iterrows(): 
<<<<<<< HEAD
        if row['clarity_level'] not in clarity_level: 
            df.drop(index, inplace=True) 

    # set val split for each class equal to 35% of the class with the least amount of rows
    least_label = int(df['label'].value_counts().min()*0.35) 
    df_val = df.groupby('label').apply(lambda x: x.sample(n=least_label, replace=False)) 
=======
        if row['clarity_level'] not in clarity_level: df.drop(index, inplace=True) 

    # set val split for each class equal to 35% of the class with the least amount of rows
    least_label = int(df['label'].value_counts().min()*0.35) 
    df_val = df.groupby('label').apply(lambda x: x.sample(n=1, replace=False)) 
>>>>>>> 3e583ac3aea71d068ac170fa6f36b82bc5d005b2
    df_val['split'] = 'val'
    cond = df['id'].isin(df_val['id'])
    df.drop(df[cond].index, inplace = True)
    df = pd.concat([df, df_val], ignore_index=True)
<<<<<<< HEAD
    print(df.tail(50))
=======
>>>>>>> 3e583ac3aea71d068ac170fa6f36b82bc5d005b2


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

<<<<<<< HEAD
        source_bucket = storage_client.bucket(bucket_name)
=======
        source_bucket = storage_client.bucket('survai-dataset')
>>>>>>> 3e583ac3aea71d068ac170fa6f36b82bc5d005b2
        source_blob = source_bucket.blob(f"datasets/var/master_videos/{label}/{file_name}_{fill_start}_{fill_end}.mp4")

        if split == 'val':
            source_bucket.copy_blob(source_blob, source_bucket, 
                                    f"datasets/var/{split_path}/val/{label}/{file_name}_{fill_start}_{fill_end}.mp4")
            val_list.append(f"{label}/{file_name}_{fill_start}_{fill_end}.mp4 {class_num}")
            
        if split == 'train':
            source_bucket.copy_blob(source_blob, source_bucket, 
                                    f"datasets/var/{split_path}/train/{label}/{file_name}_{fill_start}_{fill_end}.mp4")
            train_list.append(f"{label}/{file_name}_{fill_start}_{fill_end}.mp4 {class_num}")


    # create val_list and train_list txt's  
    with open('val_list.txt', 'w') as val_file, open('train_list.txt', 'w') as train_file:
        for file_name in val_list:
            val_file.write(f"{file_name}\n")
        for file_name in train_list:
            train_file.write(f"{file_name}\n")

<<<<<<< HEAD
    upload_to_bucket('datasets/var/split/val_list.txt', 'val_list.txt', bucket_name)
    upload_to_bucket('datasets/var/split/train_list.txt', 'train_list.txt', bucket_name)
=======
    upload_to_bucket('datasets/var/split/val_list.txt', 'val_list.txt', 'survai-dataset')
    upload_to_bucket('datasets/var/split/train_list.txt', 'train_list.txt', 'survai-dataset')
>>>>>>> 3e583ac3aea71d068ac170fa6f36b82bc5d005b2
    os.remove('val_list.txt')
    os.remove('train_list.txt')  

if __name__ == '__main__':
    args = parse_args()
    download_videos(args.csv_path, args.split_path, args.clarity_level)  

    

