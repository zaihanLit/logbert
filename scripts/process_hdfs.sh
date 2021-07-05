#!/bin/bash

OUTPUT_DIR="~/.output/"
DATASET_NAME='hdfs_2k' #hdfs_2k, hdfs
LOG_FILE='HDFS_2k.log' #HDFS_2k.log, HDFS.log
PARSER_TYPE='spell'
LOG_FORMAT='Date,Time,Pid,Level,Component,Content'
REGEX1='(?<=blk_)[-\d]+'
REGEX2='\d+.\d+.\d+.\d+'
REGEX3='(/[-\w]+)+'
TAU=0.35
WINDOW_TYPE='session'

log="${HOME}/.logs/"
if [ -e $log ]
then
  echo "$log exists"
else
  mkdir -p $log
fi


python ../data_process.py \
--output_dir=$OUTPUT_DIR \
--dataset_name=$DATASET_NAME \
--log_file=$LOG_FILE \
--parser_type=$PARSER_TYPE \
--log_format=$LOG_FORMAT \
--regex="$REGEX1 $REGEX2 $REGEX3" \
--tau=$TAU \
--window_type=$WINDOW_TYPE \
2>&1 | tee -a "${log}${DATASET_NAME}_${PARSER_TYPE}_${WINDOW_TYPE}.log"
