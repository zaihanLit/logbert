import os
import pandas as pd
from argparse import ArgumentParser

from logbert.bert_pytorch import Predictor, Trainer
from logbert.bert_pytorch.dataset import WordVocab
from common import Utils


# define options
options=dict()


options["model_name"] = "logbert"
options["dataset_name"] = "aiia"
options["device"] = "cpu"
options["output_dir"] = "~/.output/"
options["model_dir"] = "logbert_aiia/"

options["train_ratio"] = 1
options["valid_ratio"] = 0.1
options["test_ratio"] = 1

options["max_epoch"] = 200
options["n_epochs_stop"] = 5
options["n_warm_up_epoch"] = 0
options["batch_size"] = 32
options["lr"] = 0.001

options["is_logkey"] = True
options["is_time"] = False
options["min_freq"] = 1

options["seq_len"] = 512
options["min_len"] = 10
options["max_len"] = 512
options["mask_ratio"] = 0.5

options["window_size"] = 20
options["adaptive_window"] = True
options["deepsvdd_loss"] = True
options["deepsvdd_loss_test"] = False

options["scale"] = None
options["scale_path"] = None
options["hidden"] = 256
options["layers"] = 4

options["attn_heads"] = 4
options["num_workers"] = 5
options["adam_beta1"] = 0.9
options["adam_beta2"] = 0.999
options["adam_weight_decay"] = 0.00
options["log_freq"] = 100
options["num_candidates"] = 15


options["output_dir"] = os.path.expanduser(options["output_dir"] + options["dataset_name"] + "/")
options["model_dir"] = options["output_dir"] + options["model_dir"]

options["train_vocab"] = options["output_dir"] + "train"
options["vocab_path"] = options["output_dir"] + "vocab.pkl"  # pickle file
options["model_path"] = options["model_dir"] + "best_model.pth"
options["scale_path"] = options["model_dir"] + "scale.pkl"

options["testset_files"] = ["evalue-"+str(i)+".txt.test" for i in range(0,10)]

if not os.path.exists(options["model_dir"]):
    os.makedirs(options["model_dir"], exist_ok=True)

Utils.seed_everything(seed=1234)

print("Save options parameters")
Utils.save_parameters(options, options["model_dir"] + "parameters.txt")

if not os.path.exists(options["vocab_path"]):
    with open(options["train_vocab"], "r") as f:
        texts = f.readlines()
    vocab = WordVocab(texts, min_freq=options["min_freq"])
    print("VOCAB SIZE:", len(vocab))
    print("save vocab in", options["vocab_path"])
    print("\n")
    vocab.save_vocab(options["vocab_path"])

Trainer(options).train()
#Predictor(options).predict_aiia()

'''
result_df = pd.DataFrame(columns=['SequenceId','Result','StartLineNum','Detail','TimeCost'])

for i, testset_file in enumerate(options["testset_files"]):
    print("Now predicting "+testset_file+".")
    evaluefile_path = "evalue/" + testset_file

    retResult,firstlineNum, outputList, elapsed_time = Predictor(options).predict_testset_aiia(evaluefile_path,seq_threshold=0.1)
    new_row = {"SequenceId":testset_file.strip(".txt"),"Result":retResult,"StartLineNum":firstlineNum,"Detail":outputList,"TimeCost":str(int(elapsed_time*1000))+"ms"}
    result_df = result_df.append(new_row,ignore_index=True)

result_df.to_csv(options["output_dir"]+"result.csv", index = False)
'''




