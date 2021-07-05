OUTPUT_DIR="~/.output/"
DATASET_NAME='bgl'
MODEL_NAME='loganomaly' #deeplog, loganomaly
QUANTITATIVES='true' # false if deeplog, true if loganomaly

WINDOW_SIZE=20
MIN_LEN=10

INPUT_SIZE=1
HIDDEN_SIZE=64
EMBEDDING_DIM=50
NUM_LAYERS=2

MAX_EPOCH=200 #200
N_EPOCHS_STOP=10
N_WARM_UP_EPOCH=5
BATCH_SIZE=32 #32
LR=0.01
LR_DECAY_RATIO=0.1
DEVICE='cuda:1'
SEQUENTIALS='true'
SAMPLE='sliding_window'

TRAIN_RATIO=1
VALID_RATIO=0.1
TEST_RATIO=1

NUM_CANDIDATES=9


EXP_MODEL="${MODEL_NAME}_window_size_${WINDOW_SIZE}_num_candidate_${NUM_CANDIDATES}"

MODEL_DIR="${EXP_MODEL}/"

log="${HOME}/.logs/"


python ../main_logdeep.py \
--output_dir=$OUTPUT_DIR \
--dataset_name=$DATASET_NAME \
--model_name=$MODEL_NAME \
--model_dir=$MODEL_DIR \
--window_size=$WINDOW_SIZE \
--min_len=$MIN_LEN \
--input_size=$INPUT_SIZE \
--hidden_size=$HIDDEN_SIZE \
--embedding_dim=$EMBEDDING_DIM \
--num_layers=$NUM_LAYERS \
--max_epoch=$MAX_EPOCH \
--n_epochs_stop=$N_EPOCHS_STOP \
--n_warm_up_epoch=$N_WARM_UP_EPOCH \
--batch_size=$BATCH_SIZE \
--lr=$LR \
--lr_decay_ratio=$LR_DECAY_RATIO \
--device=$DEVICE \
--sequentials=$SEQUENTIALS \
--quantitatives=$QUANTITATIVES \
--sample=$SAMPLE \
--train_ratio=$TRAIN_RATIO \
--valid_ratio=$VALID_RATIO \
--test_ratio=$TEST_RATIO \
--is_logkey \
--num_candidates=$NUM_CANDIDATES \
2>&1 | tee -a "${log}${DATASET_NAME}_${EXP_MODEL}.log"

