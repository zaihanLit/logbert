#!/bin/bash

# hyperparameters
OUTPUT_DIR="~/.output/"
DATASET_NAME='bgl'
MODEL_NAME='logbert'

MIN_LEN=10
TRAIN_RATIO=1
VALID_RATIO=0.1
TEST_RATIO=1

MAX_EPOCH=200
N_EPOCHS_STOP=5
N_WARM_UP_EPOCH=0
BATCH_SIZE=32
MASK_RATIO=0.5
NUM_CANDIDATES=15


EXP_MODEL="${MODEL_NAME}_mask_ratio_${MASK_RATIO}_num_candidate_${NUM_CANDIDATES}"

MODEL_DIR="${EXP_MODEL}/"

log="${HOME}/.logs/"



python ../main_logbert.py \
--output_dir=$OUTPUT_DIR \
--dataset_name=$DATASET_NAME \
--model_name=$MODEL_NAME \
--model_dir=$MODEL_DIR \
--is_logkey \
--min_len=$MIN_LEN \
--train_ratio=$TRAIN_RATIO \
--valid_ratio=$VALID_RATIO \
--test_ratio=$TEST_RATIO \
--max_epoch=$MAX_EPOCH \
--n_warm_up_epoch=$N_WARM_UP_EPOCH \
--n_epochs_stop=$N_EPOCHS_STOP \
--batch_size=$BATCH_SIZE \
--mask_ratio=$MASK_RATIO \
--adaptive_window \
--deepsvdd_loss \
--num_candidates=$NUM_CANDIDATES \
2>&1 | tee -a "${log}${DATASET_NAME}_${EXP_MODEL}.log"

