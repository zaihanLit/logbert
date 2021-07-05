#!/bin/bash

OUTPUT_DIR="~/.output/"
DATASET_NAME='bgl_2k' #bgl_2k, bgl
LOG_FILE='BGL_2k.log' #BGL_2k.log, BGL.log
PARSER_TYPE='drain'
LOG_FORMAT='Label,Id,Date,Code1,Time,Code2,Component1,Component2,Level,Content'
REGEX1='(0x)[0-9a-fA-F]+'
REGEX2='\d+.\d+.\d+.\d+'
REGEX3='(/[-\w]+)+'
REGEX4='\d+'
ST=0.3
DEPTH=3
WINDOW_TYPE='sliding'
WINDOW_SIZE=5
STEP_SIZE=1
TRAIN_SIZE=0.4

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
--regex="$REGEX1 $REGEX2 $REGEX3 $REGEX4" \
--st=$ST \
--depth=$DEPTH \
--window_type=$WINDOW_TYPE \
--window_size=$WINDOW_SIZE \
--step_size=$STEP_SIZE \
--train_size=$TRAIN_SIZE \
2>&1 | tee -a "${log}${DATASET_NAME}_${PARSER_TYPE}_${WINDOW_TYPE}.log"
