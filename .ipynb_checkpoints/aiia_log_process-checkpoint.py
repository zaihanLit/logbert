"""
Pipelines for processing raw logs to structured data
including sampling (optional), log parsing, log sequence generation by windowing, and train test splitting
"""


import os
import pickle

from dataset import SimpleParserFactory, split_train_test_aiia, generate_test_set_aiia, sample_raw_data


# define options
options=dict()

# directory path
options["dataset_name"] = "aiia"
options["data_dir"] = "~/.dataset/"
options["output_dir"] = "~/.output/"

# log file name
options["log_file"] = "normal.txt"

options["parser_type"] = "drain"
options["log_format"] = "Id,Content"

REGEX1='(0x)[0-9a-fA-F]+'
REGEX2='\d+.\d+.\d+.\d+'
REGEX3='(/[-\w]+)+'
REGEX4='\d+'
options["regex"] = [REGEX1,REGEX2,REGEX3,REGEX4]
options["keep_para"] = False

options["st"] = 0.3
options["depth"] = 3
options["max_child"] = 100
options["tau"] = 0.5

options["window_type"] = "sliding_aiia"
options["window_size"] = 50
options["step_size"] = 5
options["train_size"] = 0.7

# evalue logs
options["evalue_files"] = ["evalue-"+str(i)+".txt" for i in range(0,20)]

# parser path
options["parserPickle_path"] = "/root/.output/aiia/parser.pkl"



# the main process
options["output_dir"] = os.path.expanduser(options["output_dir"])
options["data_dir"] = os.path.expanduser(options["data_dir"])

options["data_dir"] = os.path.join(options["data_dir"], options["dataset_name"] + "/")
options["output_dir"] = os.path.join(options["output_dir"], options["dataset_name"] + "/")


if not os.path.exists(options["output_dir"]):
    os.makedirs(options["output_dir"], exist_ok=True)

'''
# parse normal logs
if options["parser_type"] is not None:
    options["log_format"] = " ".join([f"<{field}>" for field in options["log_format"].split(",")])
    parser = SimpleParserFactory.create_parser(options["data_dir"], options["output_dir"], options["parser_type"], options["log_format"],
                                                options["regex"], options["keep_para"],
                                                options["st"], options["depth"], options["max_child"], options["tau"])
    parser.parse(options["log_file"])

    with open(options["parserPickle_path"], "wb") as f:
        pickle.dump(parser, f)
''' 


# split normal to train and valid set

split_train_test_aiia(data_dir=options["data_dir"],
                    output_dir=options["output_dir"],
                    log_file=options["log_file"],
                    dataset_name=options["dataset_name"],
                    window_type=options["window_type"],
                    window_size=options["window_size"],
                    step_size=options["step_size"],
                    train_size=options["train_size"])


'''
# parse evalue logs
with open(options["parserPickle_path"], "rb") as f:
    parser = pickle.load(f)

for evalue_file in options["evalue_files"]:
    print("Now processing "+evalue_file+".")
    evaluefile_path = "evalue/" + evalue_file

    options["log_format"] = " ".join([f"<{field}>" for field in options["log_format"].split(",")])
    parser.parse(evaluefile_path)
'''


# generate test set for each evalue files

for evalue_file in options["evalue_files"]:
    print("Now processing "+evalue_file+".")
    evaluefile_path = "evalue/" + evalue_file

    generate_test_set_aiia(output_dir=options["output_dir"],
                        log_file=evaluefile_path,
                        window_type=options["window_type"],
                        window_size=options["window_size"],
                        step_size=options["step_size"])


