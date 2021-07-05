#!/bin/bash

OUTPUT_DIR='~/.output/'
DATASET_NAME='tbird_20m'
BASELINES='pca_iforest_svm_logcluster'

log="${HOME}/.logs/"


python ../main_loglizer.py \
--output_dir=$OUTPUT_DIR \
--dataset_name=$DATASET_NAME \
--baselines=$BASELINES \
2>&1 | tee -a "${log}${DATASET_NAME}_${BASELINES}.log"