# Introduction

Data tools is a repository containing tools designed to aid in the data collection process as well as prepare the data to be used for training by Survai's machine learning models. The tools are split by Object Detection (survai_od), and Video Action Recognition (survai_var). 

## Object Detection

### edit_jsons

#### coco_to_supervisely.ipynb
Convert json format from our standard coco format, to "supervisely" json format. Supervisely is a machine learning platfrom that provides supplemental annotations for our object detection dataset through a company called "Quantigo". For them to perform this service on our existing data, coco jsons must be converted to their proprietary "supervisely" format. 

The script will take the path to a coco json and convert it to the following format:
```
| - dataset
|   | - annotations
|   |   | - images
|   |   | - annotations
|   | - meta.json
```

#### convert_json_format.ipynb
Converts a json file to the following formats:
- mturk to coco
- coco to via vgg
- mturk csv to via vgg

Train, val splits the following formats:
- VOC
- COCO

#### delete_images.ipynb
References a folder of images to its respective json. Any images in the folder that are not listed in the "images" dictionary inside the json file will be deleted. This prevents the model from training on any images that we deliberately did not label due to the images quality or relevance. 

To use, simply provide a path to the folder containing the images as well as a path to the respective json file. Running all cells will result in a cleaned folder of images to merge with the "MASTER_images" folder in the dataset.

#### edit_jsons.ipynb
Various tools to edit or add to a static json. The following are all the current options for altering the json file:

- Add 'iscrowd' tag
- Add area
- Add height and/or width to images
- Pad edges of mask and bbox
- Change categories

Requires a json input path as well as json output path.

#### split_labels.py
Script that takes a coco json as input, and creates a new json given a list of classes from the original json to include. For example, you have a coco json that has the images with the labels cat, dog, cow and chicken, but you want to train a model using only the cat and dog data.

Requires a coco json as input and outputs a new json with the classes specified in the command line argument.

#### train_val_test_split.py
Splits a coco json file into training, validation, and test sets. The terminal requires the input of the json path you wish to split as well as paths for the train, val, and test files.

### get_color

#### get_color.py 
Incomplete script that will identify the color of a vehicle detection using the most common pixel color within that detections bounding box.

### merge_coco_files

#### merge.py
Merges two coco jsons together. Used to merge new data to the master json. When running in the terminal, the script requires the input of paths to two existing jsons as well as an output path for the merged json.

### review_data

#### fiftyone.ipynb
An open source data visualization tool that allows us to store and visualize our entire object detection dataset in one place. 

To open a dataset in fiftyone, you need to provide a path to the folder containing ALL raw images for the respective dataset as well as the json file containing the coordinates and names for the annotations. This will output the dataset, visualized with all its annotations.  

### web_scrapers

#### flickr_scraper.py
Scrapes images from a given search on [flickr](https://www.flickr.com/) and downloads them into a folder.

Requires the input of a search term as well as the number of images you would like to download.


#### google_scraper.py
Scrapes images from a given search on [google images](https://images.google.com/) and downloads them into a folder.

Requires the input of a search term in the "search_keys" variable as well as the number of images you would like to download in the "number_of_images" variable.


## Video Action Recognition

### annotation_tool

#### var_app.ipynb
Annotates clips from youtube videos and stores them in a database created in Supabase titled, "var_data". Additionally, this script will upload each annotated clip to the "survai_dataset" google cloud storage bucket in its appropriate folder. This is to prevent data loss from users and youtube admins deleting videos.

The script takes the following inputs:
- youtube url
- label
- clarity level tag (easy, medium or hard. based off of the quality of the video.)
- time start and time end (i.e. 0:30, 1:20)

#### var_app_LEGACY.ipynb
Original version of var_app. No longer works with the var data collection pipeline.

### prepare_data_for_train
For all scripts in this directory, the following files are required:
- label_map/class_list
- google cloud access key
- csv containing the most recent video action training data

#### gcloud_upload.py
Uploads all videos in the var_data database to the survai_dataset google cloud storage bucket that do not already exist. The script will also create a train/val split of the entire dataset along with the respective txt files containing the paths to each video clip. Currently, the amount of clips that are split from each class into the val dataset is determined by taking 35% of the SMALLEST class in terms of clip count. It is important to note that the clips are taken randomly from each class every time the script is ran. 

The script requires the following terminal inputs:
- path to csv containing ALL var_data (usually generated directly from Supabase)
- path to save the split dataset (default is prepare_data_for_train)
- specification of the clarity levels to include in the split dataset (default is all possible clarity levels)

#### local_download.py
Downloads the videos in the video action dataset into a 'master_videos' folder in your local directory and generates a train val split. The script works the same as gcloud_upload.py.

#### train_val_split.py 
Generates a train val split of the video action data that is in [survai-dataset/datasets/var/master_videos](https://console.cloud.google.com/storage/browser/survai-dataset/datasets/var/master_videos) at the time of running the script.

### quality_control

#### quality_control.ipynb
Will display each video clip and allow user to modify the label, start and end time, and clarity level. There is also an option to mark a video as "bad" to be discarded or ignored when creating a train/test split. An input of a label name will start the user at the last video clip of that label that has not been reviewed.

#### quality_control_LEGACY.ipynb
Original version of quality_control.ipynb. No longer works with the var data collection pipeline.

----------------------------------------------------------------------------------------------------
For more information on collecting training data and putting it into the Glimpse system refer to page 5 here: https://docs.google.com/document/d/1suZmiOkJ7AjUf3kXyYZgi1mBKoY6DloNnoSKQ_LIumg/edit?usp=sharing
