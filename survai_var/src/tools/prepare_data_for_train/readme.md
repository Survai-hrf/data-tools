
EXPLANATION:
-----------------------------------------------------------------------------------------------
Given a var csv, download all the videos from youtube, put them in proper hiearchy, tran and val split, and create the 3 relevant txts. 
Final output should be a folder containing all these things, fully ready for model training.

HIGH LEVEL STEPS:
-----------------------------------------------------------------------------------------------
1.) see if the videos are already downloaded

2.) download the new videos from youtube with proper naming conventions on download, and retry the broken ones

3.) generate the label_map, train and val txts by train val splitting the videos that survived.

4.) at this point a single folder should contain subfolders of each class, and have all videos in it associated with that class. With 3 txts outside these folders.
	move associated videos into NEW train and val video folders in correspondence with the train and val txts. 
	THERE SHOULD ONLY BE TWO FOLDERS: videos_train and videos_val, with subfolders for each class. no folder with all videos.

5.) peace out

These steps may be wrong or omitting something, i just kinda threw it together

CONDITIONS:
-----------------------------------------------------------------------------------------------
- All videos must be WORKING videos. When downloaded, some will be broken. These videos must be deleted AFTER being reattempted. VERIFY ALL VIDEOS ARE WORKING or its not final

- Final code result must be in one .py file already prepared called prepare_data_for_train.py, that takes as least command line arguements as possible.

- train and val splits MUST BE RANDOM 

- Final folder hierarchy output should be:

	[ ] *dataset name*
		[ ] videos_train
			[ ] restraining
					1KtJwup_tK421_000200_000209.mp4
					2a2Z6j3Ur_I2_000016_000022.mp4
					...
			[ ] brawling
					...
			[ ] ...
					...
		[ ] videos_val
			[ ] restraining
					4UJf_STaRUU1_000032_000040.mp4
					4GXivYtOLvQ2_000005_000019.mp4
					...
			[ ] brawling
					...
			[ ] ...
					...
		train_list.txt
		val_list.txt
		label_map.txt

- label_map.txt contains simply a class name on each new line and looks like this:
	brawling
	crowd
	person_on_ground
	restraining
	running
	spray
	striking
	throwing
DO NOT LEAVE ANY WHITESPACE AT ALL


- train_list.txt and val_list.txt should be rows of data looking like this:

	spray/MbRuBTMWTZw1_000002_000005.mp4 5
	^         ^              ^           ^
  class    youtube_id     timestamp   class id

	timestamp must always have 6 digits!
	DO NOT LEAVE ANY WHITESPACE AT ALL

