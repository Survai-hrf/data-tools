#!/usr/bin/env bash


#ANNOT TYPE = master or train_val
ANNOT_NAME=$1

DATA_DIR="/home/bean/code/hrf/datasets/VAR/survai_var_mk1"

ANNO_DIR="/home/bean/code/hrf/datasets/VAR/survai_var_mk1/annotations"

python tools/data/survai_var_mk1/download.py ${ANNO_DIR}/${ANNOT_NAME}_master.csv test/videos

#python tools/data/survai_var_mk1/train_val_split.py ${ANNO_DIR}/${ANNOT_NAME}_master.csv

#DATASET="survai_var_mk1"


#cd ../../../
#PYTHONPATH=. python tools/data/build_file_list.py ${DATASET} ${DATA_DIR}videos/ --level 2 --format videos --num-split 1 --subset train --shuffle --custom_annot_name $ANNOT_NAME
echo "Train filelist for video generated."

#PYTHONPATH=. python tools/data/build_file_list.py ${DATASET} ${DATA_DIR}/videos/ --level 2 --format videos --num-split 1 --subset val --shuffle --custom_annot_name $ANNOT_NAME
echo "Val filelist for video generated."
cd tools/data/$DATASET/
#python download.py ${ANNO_DIR}/${ANNOT_NAME}_train.csv ${DATA_DIR}/videos_train
#echo "dfgwefg"
#python download.py ${ANNO_DIR}/${ANNOT_NAME}_val.csv ${DATA_DIR}/videos_val

#source deactivate kinetics
#conda remove -n kinetics --all
