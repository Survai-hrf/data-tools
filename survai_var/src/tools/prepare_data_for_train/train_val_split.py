from distutils.log import error
import os
from google.cloud import storage
import argparse
import pandas as pd
from decord import VideoReader



def parse_args():
    parser = argparse.ArgumentParser(
        description='This script will create a new train, val split using the existing videos in the survai-dataset bucket in google cloud storage.')
    parser.add_argument('--split-path', default='split', help='specifies which folder to put the train, val split')


def train_val_split(split_path):

    # connect to gcloud bucket
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'survai-data-connect.json'
    storage_client = storage.Client()
    bucket_name = 'survai-dataset'
    master_bucket = storage_client.bucket(bucket_name)


    data = []
    val_txt = []
    train_txt = []


    # generate label map
    txt = open('label_map.txt', 'r')
    lines = [s.strip('\n')for s in txt]
    label_map = dict((index, label) for label, index in enumerate(lines, start=0))


    # get list of videos from gcloud
    videos = storage_client.list_blobs(bucket_name, prefix='datasets/var/master_videos/')
    video_list = [video.name for video in videos]


    # put labels and respective files into a dataframe
    for video in video_list:
        label = str(video.split('/')[3])
        file = str(video.split('/')[4])

        data.append({
            'label': label,
            'file': file
        })

    df = pd.DataFrame(data)
    df['split'] = 'train'


    # get 35% of smallest class
    split_size = int(df['label'].value_counts().min()*0.35)


    # get random 7 files from each class and change split from 'train' to 'val'
    df_val = df.groupby('label').apply(lambda x: x.sample(n=split_size, replace=False))
    df_val['split'] = 'val'
    cond = df['file'].isin(df_val['file'])
    df.drop(df[cond].index, inplace = True)
    df = pd.concat([df, df_val], ignore_index=True)



    # function to upload videos to gcloud bucket
    def upload_to_bucket(blob_name, file_path, bucket_name):
        try:
            bucket = storage_client.get_bucket(bucket_name)
            blob = bucket.blob(blob_name)
            blob.upload_from_filename(file_path)
        except Exception as e:
            print(e)


    # split files into train and val folders
    def split_files(x):

        class_num = label_map.get(x.label)
        master_blob = master_bucket.blob(f"datasets/var/master_videos/{x.label}/{x.file}")

        if x.split == 'val':
            master_bucket.copy_blob(master_blob, master_bucket, 
                                    f"datasets/var/{split_path}/val/{x.label}/{x.file}")
            val_txt.append(f"{x.label}/{x.file} {class_num}")

        if x.split == 'train':
            master_bucket.copy_blob(master_blob, master_bucket, 
                                    f"datasets/var/{split_path}/train/{x.label}/{x.file}")
            train_txt.append(f"{x.label}/{x.file} {class_num}")


    # create split
    df.apply(split_files, axis=1)


    # create val and train txt's  
    with open('val_list.txt', 'w') as val_file, open('train_list.txt', 'w') as train_file:
        for file_name in val_txt:
            val_file.write(f"{file_name}\n")
        for file_name in train_txt:
            train_file.write(f"{file_name}\n")

    upload_to_bucket(f'datasets/var/{split_path}/val_list.txt', 'val_list.txt', bucket_name)
    upload_to_bucket(f'datasets/var/{split_path}/train_list.txt', 'train_list.txt', bucket_name)


if __name__ == '__main__':
    args = parse_args()
    train_val_split(args.split_path)