#!/bin/bash

OUTPUT_DIR="~/.output/"

DATASET_NAME='tbird'
LOG_FILE='Thunderbird.log'

SAMPLE_DATASET_NAME="tbird_20m"
SAMPLE_LOG_FILE="Thunderbird_20M.log" #"Thunderbird_20M.log"
SAMPLE_SIZE=20000000000

PARSER_TYPE='drain'
LOG_FORMAT='Label,Id,Date,Admin,Month,Day,Time,AdminAddr,Content'
REGEX1='(0x)[0-9a-fA-F]+'
REGEX2='\d+.\d+.\d+.\d+'
REGEX3='(?<=Warning: we failed to resolve data source name )[\w\s]+'
REGEX4='\d+'
ST=0.3
DEPTH=3

WINDOW_TYPE='sliding'
WINDOW_SIZE=1
STEP_SIZE=0.5
TRAIN_SIZE=0.4

python ../data_process.py \
--output_dir=$OUTPUT_DIR \
--dataset_name=$DATASET_NAME \
--log_file=$LOG_FILE \
--sample_dataset_name=$SAMPLE_DATASET_NAME \
--sample_log_file=$SAMPLE_LOG_FILE \
--sample_size=$SAMPLE_SIZE \
--parser_type=$PARSER_TYPE \
--log_format=$LOG_FORMAT \
--regex="$REGEX1 $REGEX2 $REGEX3 $REGEX4" \
--st=$ST \
--depth=$DEPTH \
--window_type=$WINDOW_TYPE \
--window_size=$WINDOW_SIZE \
--step_size=$STEP_SIZE \
--train_size=$TRAIN_SIZE \
2>&1 | tee -a "${log}${DATASET_NAME}_${PARSER_TYPE}_${WINDOW_TYPE}.log"
