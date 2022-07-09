import os
from pytube import YouTube
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import pandas as pd
from pytube.exceptions import VideoUnavailable
import shutil

csv_path = 'csvs/11-11-21_03-17-22_LEGACY_test.csv'
df = pd.read_csv(csv_path)
df = df.reset_index()  # make sure indexes pair with number of rows


label_list = ['br', 'cr', 'st', 'pg', 'ru', 'ar', 'th', 'ps']
class_dict = {'br': 0, 'cr': 1, 'pg': 2, 'ar': 3, 'ru': 4, 'ps': 5, 'st': 6}


# create array to store broken videos
broken_videos = set()

# function that retries download after first fails, (tries) times
def retry_download(tries, url, file_name, label):
    for i in range(tries):
        try:
            video = YouTube(url)
            yt_video = video.streams.get_highest_resolution()
            yt_video.download(output_path=f'videos/{label}/', filename=f"{file_name}.mp4")

            # download videos into correct folder
            ffmpeg_extract_subclip(filename=f'videos/{label}/{file_name}.mp4', t1=start, t2=end, 
                                    targetname=f'videos/{label}/{file_name}_{fill_start}_{fill_end}.mp4') 
            os.remove(f'videos/{label}/{file_name}.mp4')
            
        except VideoUnavailable:
            if i < tries:
                broken_videos.add(file_name) # add broken videos to array to be deleted
                continue  
            

# Iterates all videos in csv
for index, row in df.iterrows():

    file_name = str(row['youtube_id'])
    start = int(row['time_start'])
    end = int(row['time_end'])
    label = str(row['label'])
    bad_egg = row['bad_egg']
    url = f'https://www.youtube.com/watch?v={file_name[0:11]}'
    fill_start = str(start).zfill(6) # make times the same number of digits
    fill_end = str(end).zfill(6)

    # ignore bad labels and bad videos
    if label not in label_list or bad_egg == True:
        continue

    # makes sure videos that were previously downloaded don't get downloaded again
    if os.path.exists(f"master_videos/{label}/{file_name}_{fill_start}_{fill_end}.mp4"):
        print('file already exists')
        continue
    
    try:
        video = YouTube(url)
        yt_video = video.streams.get_highest_resolution()
        # download video to master_videos directory
        yt_video.download(output_path=f'master_videos/{label}', filename=f"{file_name}.mp4")
        

        # download videos into correct folder
        ffmpeg_extract_subclip(filename=f'master_videos/{label}/{file_name}.mp4', t1=start, t2=end, 
                                targetname=f'master_videos/{label}/{file_name}_{fill_start}_{fill_end}.mp4') 
        os.remove(f'master_videos/{label}/{file_name}.mp4')

    except:
        print('retrying...', file_name)
        retry_download(1, url, file_name, label)  


# drop broken videos from dataframe
for video in broken_videos:
    df = df.drop(df.loc[df['youtube_id'] == video].index)


# create dataframe of random val videos, amount for each class based off of 35% of the smallest class
least_label_35 = int(df['label'].value_counts().min()*.35)
df_val = df.groupby('label')['youtube_id', 'time_start', 'time_end'].apply(lambda s: s.sample(least_label_35))
df_val = pd.DataFrame(df_val)
df_val = df_val.reset_index()


# remove df_val from df to get list of id's for df_train
cond = df['youtube_id'].isin(df_val['youtube_id'])
df.drop(df[cond].index, inplace = True)


# move val videos to new directory
val_list = []

for ind, row in df_val.iterrows():
    
    id = str(row['youtube_id'])
    label = str(row['label'])
    start = row['time_start']
    end = row['time_end']
    fill_start = str(start).zfill(6) # make times the same number of digits
    fill_end = str(end).zfill(6)
    class_num = class_dict.get(label)
    
    # ignore bad labels and bad videos
    if label not in label_list or bad_egg == True:
        continue   
       
    # create directory to move val videos
    val_path = f'val/{label}'
    if not os.path.exists(val_path):
        os.makedirs(val_path)

    # move videos to val videos
    shutil.copyfile(f"master_videos/{label}/{id}_{fill_start}_{fill_end}.mp4", 
                    f"val/{label}/{id}_{fill_start}_{fill_end}.mp4")   
    val_list.append(f"{label}/{id}_{fill_start}_{fill_end}.mp4 {class_num}")


# move train videos to new directory
train_list = []

for ind, row in df.iterrows():
    
    id = str(row['youtube_id'])
    label = str(row['label'])
    start = row['time_start']
    end = row['time_end']
    fill_start = str(start).zfill(6) # make times the same number of digits
    fill_end = str(end).zfill(6)
    class_num = class_dict.get(label)

    # ignore bad labels and bad videos
    if label not in label_list or bad_egg == True:
        continue
        
    # create directory to for train videos
    train_path = f'train/{label}'
    if not os.path.exists(train_path):
        os.makedirs(train_path)

    # move videos to train videos
    shutil.copyfile(f"master_videos/{label}/{id}_{fill_start}_{fill_end}.mp4", 
                    f"train/{label}/{id}_{fill_start}_{fill_end}.mp4")
    train_list.append(f"{label}/{id}_{fill_start}_{fill_end}.mp4 {class_num}")


# create val_list and train_list txt's  
with open('files_txts/val_list.txt', 'w') as val_file, open('files_txts/train_list.txt', 'w') as train_file:
    for video in val_list:
        val_file.write("%s\n" % f'{video}')
    for video in train_list:
        train_file.write("%s\n" % f'{video}')