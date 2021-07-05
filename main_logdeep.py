import os
from argparse import ArgumentParser

from logdeep.tools.predict import Predicter
from logdeep.tools.train import Trainer

from common import Vocab, Utils


def arg_parser():
    """
    add parser parameters
    :return:
    """
    parser = ArgumentParser()
    parser.add_argument("--model_name", help="which model to train", default="deeplog")
    parser.add_argument("--dataset_name", help="which dataset to use")
    parser.add_argument("--output_dir", metavar="DIR", help="output directory")
    parser.add_argument("--model_dir", metavar="DIR", help="model directory")

    parser.add_argument("--train_ratio", default=1, type=float)
    parser.add_argument("--valid_ratio", default=0.1, type=float)
    parser.add_argument("--test_ratio", default=1, type=float)

    # features
    parser.add_argument("--is_logkey", action='store_true', help="is logkey included in features")
    parser.add_argument("--is_time", action='store_true', help="is time duration included in features")
    parser.add_argument("--scale", default=None, help="scale time duration")

    parser.add_argument("--min_freq", default=1, type=int, help="min frequency of logkey in vocab")

    parser.add_argument("--sample", default="sliding_window", help="split sequences by sliding window")

    parser.add_argument("--min_len", default=0, type=int, help="min length of sequence")

    # in deeplog, each log sequence creates a subsequences by windowing for predicting the next logkey
    parser.add_argument("--window_size", default=20, type=int, help="window size is used to create subsequences")

    # Features
    parser.add_argument("--sequentials", default=True, help="sequences of logkeys")
    parser.add_argument("--quantitatives", default=False, help="logkey count vector")
    parser.add_argument("--semantics", default=False, help="logkey embedding with semantics vectors")
    parser.add_argument("--parameters", default=False, help="include parameters in logs after parsing such time")

    parser.add_argument("--input_size", default=1, type=int, help="input size in lstm")
    parser.add_argument("--hidden_size", default=64, type=int, help="hidden size in lstm")
    parser.add_argument("--num_layers", default=2, type=int, help="num of lstm layers")
    parser.add_argument("--embedding_dim", default=50, type=int, help="embedding dimension of logkeys")

    parser.add_argument("--max_epoch", default=20, type=int, help="epochs")
    parser.add_argument("--n_epochs_stop", default=10, type=int, help="training stops after n epochs without improvement")
    parser.add_argument("--n_warm_up_epoch", default=6, type=int, help="save model parameters after n warm-up epoch")
    parser.add_argument("--batch_size", default=32, type=int)
    parser.add_argument("--lr", default=0.001, type=float, help="learning rate")
    parser.add_argument("--lr_decay_ratio", default=0.1, type=float, help="learning rate decays")

    parser.add_argument("--device", help="hardware device", default="cuda")
    parser.add_argument("--accumulation_step", default=1, type=int, help="let optimizer steps after several batches")
    parser.add_argument("--optimizer", default="adam")

    parser.add_argument("--num_candidates", default=9, type=int, help="top g candidates are normal")
    parser.add_argument("--log_freq", default=100, type=int, help="logging frequency of the batch iteration")
    parser.add_argument("--resume_path", action='store_true')
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
        vocab = Vocab(texts, min_freq=options["min_freq"])
        print("VOCAB SIZE:", len(vocab))
        print("save vocab in", options["vocab_path"])
        print("\n")
        vocab.save_vocab(options["vocab_path"])

    Trainer(options).start_train()
    Predicter(options).predict_unsupervised()


if __name__ == "__main__":
    main()
