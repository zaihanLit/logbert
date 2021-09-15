import os
from argparse import ArgumentParser

from logbert.bert_pytorch import Predictor, Trainer
from logbert.bert_pytorch.dataset import WordVocab
from common import Utils


def arg_parser():
    """
    add parser parameters
    :return:
    """
    parser = ArgumentParser()
    parser.add_argument("--model_name", help="which model to train", default="logbert")
    parser.add_argument("--dataset_name", help="which dataset to use")
    parser.add_argument("--device", help="hardware device", default="cpu")
    parser.add_argument("--output_dir", metavar="DIR", help="output directory")
    parser.add_argument("--model_dir", metavar="DIR", help="model directory")

    parser.add_argument("--train_ratio", default=1, type=float)
    parser.add_argument("--valid_ratio", default=0.1, type=float)
    parser.add_argument("--test_ratio", default=1, type=float)

    parser.add_argument("--max_epoch", default=200, type=int, help="epochs")
    parser.add_argument("--n_epochs_stop", default=10, type=int, help="stops after n epochs without improvement")
    parser.add_argument("--n_warm_up_epoch", default=10, type=int, help="save parameters after n warm-up epoch")
    parser.add_argument("--batch_size", default=32, type=int)
    parser.add_argument("--lr", default=0.001, type=float, help="learning rate")

    # features
    parser.add_argument("--is_logkey", action='store_true', help="is logkey included in features")
    parser.add_argument("--is_time", action='store_true', help="is time duration included in features")

    parser.add_argument("--min_freq", default=1, type=int, help="min frequency of logkey")

    # logbert
    parser.add_argument("--seq_len", default=512, type=int, help="max length of sequence")
    parser.add_argument("--min_len", default=10, type=int, help="min length of sequence")
    parser.add_argument("--max_len", default=512, type=int, help="for position embedding in bert")
    parser.add_argument("--mask_ratio", default=0.5, type=float, help="mask ratio in bert")

    # in deeplog, each log sequence creates a subsequences by windowing for predicting the next logkey
    # window size is discarded in logbert
    parser.add_argument("--window_size", default=20, type=int, help="window size is used to create subsequences")
    parser.add_argument("--adaptive_window", action='store_true', help="if true, window size is the length of sequences")

    parser.add_argument("--deepsvdd_loss", action='store_true', help="if calculate deepsvdd loss")
    parser.add_argument("--deepsvdd_loss_test", action='store_true', help="if use deepsvdd for prediction")

    # scale is used to standardize time duration which is discarded
    parser.add_argument("--scale", default=None, help="sklearn normalization methods")
    parser.add_argument("--scale_path", default=None, help="store the scale parameters")

    parser.add_argument("--hidden", type=int, default=256, help="hidden size in logbert")
    parser.add_argument("--layers", default=4, type=int, help="number of layers in bert")
    parser.add_argument("--attn_heads", default=4, type=int, help="number of attention heads")

    parser.add_argument("--num_workers", default=5, type=int)
    parser.add_argument("--adam_beta1", default=0.9, type=float)
    parser.add_argument("--adam_beta2", default=0.999, type=float)
    parser.add_argument("--adam_weight_decay", default=0.00, type=float)
    parser.add_argument("--log_freq", default=100, type=int, help="logging frequency of the batch iteration")
    parser.add_argument("--num_candidates", default=9, type=int, help="top g candidates are normal")

    return parser

def main():
    parser = arg_parser()
    args = parser.parse_args()
    args.output_dir = os.path.expanduser(args.output_dir + args.dataset_name + "/")
    args.model_dir = args.output_dir + args.model_dir

    options = vars(args)
    options["train_vocab"] = options["output_dir"] + "train"
    options["vocab_path"] = options["output_dir"] + "vocab.pkl"  # pickle file
    options["model_path"] = options["model_dir"] + "best_model.pth"
    options["scale_path"] = options["model_dir"] + "scale.pkl"

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

    #Trainer(options).train()
    Predictor(options).predict()


if __name__ == "__main__":
    main()





