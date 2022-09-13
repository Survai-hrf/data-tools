# Introduction

Data tools is a repository containing tools designed to aid in the data collection process as well as prepare the data to be used for training by Survai's machine learning models. The tools are split by Object Detection (survai_od), and Video Action Recognition (survai_var). 

## Object Detection

Hierarchy:
```
| - src
|   | - apps
|   |   | - fiftyone.ipynb
|   | - tools
|   |   | - coco_to_supervisely
|   |   |   | - coco_to_supervisely.ipynb
|   |   | - delete_images_not_in_json
```


### Code Descriptions

### fiftyone.ipynb

An open source data visualization tool that allows us to store and visualize our entire object detection dataset in one place. 

To open a dataset in fiftyone, you need to provide a path to the folder containing ALL raw images for the respective dataset as well as the json file containing the coordinates and names for the annotations. This will output the dataset, visualized with all its annotations.  


### coco_to_supervisely.ipynb

Convert json format from our standard coco format, to "supervisely" json format. Supervisely is a machine learning platfrom that provides supplemental annotations for our object detection dataset through a company called "Quantigo". For them to perform this service on our existing data, coco jsons must be converted to their proprietary "supervisely" format. 

The script will take the path to a coco json and convert it to the following format:
```
| - dataset
|   | - annotations
|   |   | - images
|   |   | - annotations
|   | - meta.json
```

### delete_images.ipynb

Reference a folder of images to its respective json. Any images in the folder that are not listed in the "images" dictionary inside the folders respective json file will get deleted. This prevents the model from training on any images that we deliberately did not label due to the images quality or relevance. 

To use, simply provide a path to the folder containing the images as well as a path to the respective json file. Running all cells will result in a cleaned folder of images to merge with the "MASTER_images" folder in the dataset.


### edit_json_labels.ipynb

Changes the labels in the "categories" dictionary in a coco json to the updated class names. Requires input of the path to the json you wish to update labels for.


### edit_jsons.ipynb

Various tools to edit or add to a static json. The following are all the current options for altering the json file:

- Add 'iscrowd' tag
- Add area
- Add height and/or width to images
- Pad edges of mask and bbox
- Change categories

Requires a json input path as well as json output path.


### merge.py

Merges two coco jsons together. Used to merge new data to the master json. When running in the terminal, the script requires the input of paths to two existing jsons as well as an output path for the merged json.


### flickr_scraper.py

Scrapes images from a given search on [flickr](https://www.flickr.com/) and downloads them into a folder.

Requires the input of a search term as well as the number of images you would like to download.


### google_scraper.py

Scrapes images from a given search on [google images](https://images.google.com/) and downloads them into a folder.

Requires the input of a search term in the "search_keys" variable as well as the number of images you would like to download in the "number_of_images" variable.


### class_to_txt.ipynb

Takes class names from a dictionary and writes the names into a txt file. Requires the input of a path to a json.


### convert_annot_format.ipynb

Converts a json file to the following formats:
- mturk to coco
- coco to via vgg
- mturk csv to via vgg

Train, val splits the following formats:
- VOC
- COCO


### train_val_test_split.py

Splits a coco json file into training, validation, and test sets. The terminal requires the input of the json path you wish to split as well as paths for the train, val, and test files.



## Video Action Recognition

### var_app.ipynb

Annotates clips from youtube videos and stores them in a database created in Supabase titled, "var_data". Additionally, this script will upload each annotated clip to the "survai_dataset" google cloud storage bucket in its appropriate folder. This is to prevent data loss from users and youtube admins deleting videos.

The script takes the following inputs:
- youtube url
- label
- clarity level tag (easy, medium or hard. based off of the quality of the video.)
- time start and time end (i.e. 0:30, 1:20)


### quality_control.ipynb

Will display each video clip and allow user to modify the label, start and end time, and clarity level. There is also an option to mark a video as "bad" to be discarded or ignored when creating a train/test split. An input of a label name will start the user at the last video clip of that label that has not been reviewed.


### gcloud_delete.ipynb

Deletes video clips from the "survai_dataset" google cloud storage bucket given a certain condition.


### gcloud_upload.py

Uploads all videos in the var_data database to the survai_dataset google cloud storage bucket that do not already exist. The script will also create a train/val split of the entire dataset along with the respective txt files containing the paths to each video clip. Currently, the amount of clips that are split from each class into the val dataset is determined by taking 35% of the SMALLEST class in terms of clip count. It is important to note that the clips are taken randomly from each class every time the script is ran. 

The script requires the following terminal inputs:
- path to csv containing ALL var_data (usually generated directly from Supabase)
- path to save the split dataset (default is prepare_data_for_train)
- specification of the clarity levels to include in the split dataset (default is all possible clarity levels)
