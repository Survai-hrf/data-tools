from google.cloud import storage
from pytube import YouTube
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os


def download(newvid_url, new_vid_key):
    '''downloads youtube video from url'''
    video = YouTube(newvid_url, use_oauth=True, allow_oauth_cache=True) 
    yt_video = video.streams.get_highest_resolution()
    yt_video.download(output_path='', filename=f"{new_vid_key}.mp4")


def subclip(new_vid_key, time_start, time_end, fill_start, fill_end):
    '''extrats subclip from video file'''
    ffmpeg_extract_subclip(filename=f'{new_vid_key}.mp4', t1=time_start, t2=time_end, 
                                targetname=f'{new_vid_key}_{fill_start}_{fill_end}.mp4') 
    os.remove(f'{new_vid_key}.mp4')


def upload_to_bucket(blob_name, file_path, bucket_name):
    '''uploads video clip to appropriate folder in gcloud'''
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(file_path)
    except Exception as e:
        print(e)