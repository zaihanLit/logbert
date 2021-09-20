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

# evalue的日志版本和normal的日志版本不一致，以下的正则表达式是为了消除两个日志之间版本的问题
REGEX101=['\[instance\:\s[\'\"]?([0-9a-fA-F]+-)+([0-9a-fA-F]+)[\'\"]?\]',''] # 对于每行开头的[instance: 6cf33854-4177-4998-89bd-d30cead6f9c3]要删除
REGEX102=['^Hypervisor: assignable PCI devices.*$','Hypervisor: assignable PCI devices'] # 对于Hypervisor: assignable PCI devices后面的参数要删除
REGEX103=['^Hypervisor/Node resource view.*$','Hypervisor/Node resource view'] # 对于Hypervisor/Node resource view后面的参数要删除
REGEX104=['^Lock "?.*"?','Lock <LockObject>'] # 对Lock 后面的对象"compute_resources"等，统一适配为<LockObject>
REGEX105=['^Loaded extensions:.*$','Loaded extensions'] # 对Loaded extensions后面的参数要删除
REGEX106=['^Update host state with instances:.*','Update host state with instances'] # 对Update host state with instances后面的参数要删除
REGEX107=['^.*log_opt_values','log_opt_values'] # 删除所有log_opt_values之前的参数

REGEX108=['^\"?\d+\.\d+\.\d+\.\d+.*(?!\s)\"*GET.*\"*\sstatus: 1\d{2}.*$','<GET_1XX> <GET_1XX> <GET_1XX>'] # 简化所有GET和POST的模版
REGEX109=['^\"?\d+\.\d+\.\d+\.\d+.*(?!\s)\"*POST.*\"*\sstatus: 1\d{2}.*$','<POST_1XX> <POST_1XX> <POST_1XX>'] # 简化所有GET和POST的模版
REGEX110=['^\"?\d+\.\d+\.\d+\.\d+.*(?!\s)\"*GET.*\"*\sstatus: 2\d{2}.*$','<GET_2XX> <GET_2XX> <GET_2XX>'] # 简化所有GET和POST的模版
REGEX111=['^\"?\d+\.\d+\.\d+\.\d+.*(?!\s)\"*POST.*\"*\sstatus: 2\d{2}.*$','<POST_2XX> <POST_2XX> <POST_2XX>'] # 简化所有GET和POST的模版
REGEX112=['^\"?\d+\.\d+\.\d+\.\d+.*(?!\s)\"*GET.*\"*\sstatus: 3\d{2}.*$','<GET_3XX> <GET_3XX> <GET_3XX>'] # 简化所有GET和POST的模版
REGEX113=['^\"?\d+\.\d+\.\d+\.\d+.*(?!\s)\"*POST.*\"*\sstatus: 3\d{2}.*$','<POST_3XX> <POST_3XX> <POST_3XX>'] # 简化所有GET和POST的模版
REGEX114=['^\"?\d+\.\d+\.\d+\.\d+.*(?!\s)\"*GET.*\"*\sstatus: 4\d{2}.*$','<GET_4XX> <GET_4XX> <GET_4XX>'] # 简化所有GET和POST的模版
REGEX115=['^\"?\d+\.\d+\.\d+\.\d+.*(?!\s)\"*POST.*\"*\sstatus: 4\d{2}.*$','<POST_4XX> <POST_4XX> <POST_4XX>'] # 简化所有GET和POST的模版
REGEX116=['^\"?\d+\.\d+\.\d+\.\d+.*(?!\s)\"*GET.*\"*\sstatus: 5\d{2}.*$','<GET_5XX> <GET_5XX> <GET_5XX>'] # 简化所有GET和POST的模版
REGEX117=['^\"?\d+\.\d+\.\d+\.\d+.*(?!\s)\"*POST.*\"*\sstatus: 5\d{2}.*$','<POST_5XX> <POST_5XX> <POST_5XX>'] # 简化所有GET和POST的模版
REGEX118=['^\"?\d+\.\d+\.\d+\.\d+.*(?!\s)\"*DELETE.*\"*\sstatus: 1\d{2}.*$','<DELETE_1XX> <DELETE_1XX> <DELETE_1XX>'] # 简化所有GET和POST的模版
REGEX119=['^\"?\d+\.\d+\.\d+\.\d+.*(?!\s)\"*DELETE.*\"*\sstatus: 2\d{2}.*$','<DELETE_2XX> <DELETE_2XX> <DELETE_2XX>'] # 简化所有GET和POST的模版
REGEX120=['^\"?\d+\.\d+\.\d+\.\d+.*(?!\s)\"*DELETE.*\"*\sstatus: 3\d{2}.*$','<DELETE_3XX> <DELETE_3XX> <DELETE_3XX>'] # 简化所有GET和POST的模版
REGEX121=['^\"?\d+\.\d+\.\d+\.\d+.*(?!\s)\"*DELETE.*\"*\sstatus: 4\d{2}.*$','<DELETE_4XX> <DELETE_4XX> <DELETE_4XX>'] # 简化所有GET和POST的模版
REGEX122=['^\"?\d+\.\d+\.\d+\.\d+.*(?!\s)\"*DELETE.*\"*\sstatus: 5\d{2}.*$','<DELETE_5XX> <DELETE_5XX> <DELETE_5XX>'] # 简化所有GET和POST的模版

REGEX123=['^\"?\d+\.\d+\.\d+\.\d+.*(?!\s)\"*GET.*HTTP/\d\.\d\"*\s1\d{2}.*$','<GET_1XX> <GET_1XX> <GET_1XX>'] # 简化所有GET和POST的模版
REGEX124=['^\"?\d+\.\d+\.\d+\.\d+.*(?!\s)\"*GET.*HTTP/\d\.\d\"*\s2\d{2}.*$','<GET_2XX> <GET_2XX> <GET_2XX>'] # 简化所有GET和POST的模版
REGEX125=['^\"?\d+\.\d+\.\d+\.\d+.*(?!\s)\"*GET.*HTTP/\d\.\d\"*\s3\d{2}.*$','<GET_3XX> <GET_3XX> <GET_3XX>'] # 简化所有GET和POST的模版
REGEX126=['^\"?\d+\.\d+\.\d+\.\d+.*(?!\s)\"*GET.*HTTP/\d\.\d\"*\s4\d{2}.*$','<GET_4XX> <GET_4XX> <GET_4XX>'] # 简化所有GET和POST的模版
REGEX127=['^\"?\d+\.\d+\.\d+\.\d+.*(?!\s)\"*GET.*HTTP/\d\.\d\"*\s5\d{2}.*$','<GET_5XX> <GET_5XX> <GET_5XX>'] # 简化所有GET和POST的模版
REGEX128=['^\"?\d+\.\d+\.\d+\.\d+.*(?!\s)\"*POST.*HTTP/\d\.\d\"*\s1\d{2}.*$','<POST_1XX> <POST_1XX> <POST_1XX>'] # 简化所有GET和POST的模版
REGEX129=['^\"?\d+\.\d+\.\d+\.\d+.*(?!\s)\"*POST.*HTTP/\d\.\d\"*\s2\d{2}.*$','<POST_2XX> <POST_2XX> <POST_2XX>'] # 简化所有GET和POST的模版
REGEX130=['^\"?\d+\.\d+\.\d+\.\d+.*(?!\s)\"*POST.*HTTP/\d\.\d\"*\s3\d{2}.*$','<POST_3XX> <POST_3XX> <POST_3XX>'] # 简化所有GET和POST的模版
REGEX131=['^\"?\d+\.\d+\.\d+\.\d+.*(?!\s)\"*POST.*HTTP/\d\.\d\"*\s4\d{2}.*$','<POST_4XX> <POST_4XX> <POST_4XX>'] # 简化所有GET和POST的模版
REGEX132=['^\"?\d+\.\d+\.\d+\.\d+.*(?!\s)\"*POST.*HTTP/\d\.\d\"*\s5\d{2}.*$','<POST_5XX> <POST_5XX> <POST_5XX>'] # 简化所有GET和POST的模版
REGEX133=['^\"?\d+\.\d+\.\d+\.\d+.*(?!\s)\"*DELETE.*HTTP/\d\.\d\"*\s1\d{2}.*$','<DELETE_1XX> <DELETE_1XX> <DELETE_1XX>'] # 简化所有GET和POST的模版
REGEX134=['^\"?\d+\.\d+\.\d+\.\d+.*(?!\s)\"*DELETE.*HTTP/\d\.\d\"*\s2\d{2}.*$','<DELETE_2XX> <DELETE_2XX> <DELETE_2XX>'] # 简化所有GET和POST的模版
REGEX135=['^\"?\d+\.\d+\.\d+\.\d+.*(?!\s)\"*DELETE.*HTTP/\d\.\d\"*\s3\d{2}.*$','<DELETE_3XX> <DELETE_3XX> <DELETE_3XX>'] # 简化所有GET和POST的模版
REGEX136=['^\"?\d+\.\d+\.\d+\.\d+.*(?!\s)\"*DELETE.*HTTP/\d\.\d\"*\s4\d{2}.*$','<DELETE_4XX> <DELETE_4XX> <DELETE_4XX>'] # 简化所有GET和POST的模版
REGEX137=['^\"?\d+\.\d+\.\d+\.\d+.*(?!\s)\"*DELETE.*HTTP/\d\.\d\"*\s5\d{2}.*$','<DELETE_5XX> <DELETE_5XX> <DELETE_5XX>'] # 简化所有GET和POST的模版

REGEX138=['^\"?\d+\.\d+\.\d+\.\d+.*(?!\s)\"*HEAD.*HTTP/\d\.\d\"*\s1\d{2}.*$','<HEAD_1XX> <HEAD_1XX> <HEAD_1XX>'] # 简化所有GET和POST的模版
REGEX139=['^\"?\d+\.\d+\.\d+\.\d+.*(?!\s)\"*HEAD.*HTTP/\d\.\d\"*\s2\d{2}.*$','<HEAD_2XX> <HEAD_2XX> <HEAD_2XX>'] # 简化所有GET和POST的模版
REGEX140=['^\"?\d+\.\d+\.\d+\.\d+.*(?!\s)\"*HEAD.*HTTP/\d\.\d\"*\s3\d{2}.*$','<HEAD_3XX> <HEAD_3XX> <HEAD_3XX>'] # 简化所有GET和POST的模版
REGEX141=['^\"?\d+\.\d+\.\d+\.\d+.*(?!\s)\"*HEAD.*HTTP/\d\.\d\"*\s4\d{2}.*$','<HEAD_4XX> <HEAD_4XX> <HEAD_4XX>'] # 简化所有GET和POST的模版
REGEX142=['^\"?\d+\.\d+\.\d+\.\d+.*(?!\s)\"*HEAD.*HTTP/\d\.\d\"*\s5\d{2}.*$','<HEAD_5XX> <HEAD_5XX> <HEAD_5XX>'] # 简化所有GET和POST的模版

REGEX143=['^\"?\d+\.\d+\.\d+\.\d+.*(?!\s)\"*PUT.*HTTP/\d\.\d\"*\s1\d{2}.*$','<PUT_1XX> <PUT_1XX> <PUT_1XX>'] # 简化所有GET和POST的模版
REGEX144=['^\"?\d+\.\d+\.\d+\.\d+.*(?!\s)\"*PUT.*HTTP/\d\.\d\"*\s2\d{2}.*$','<PUT_2XX> <PUT_2XX> <PUT_2XX>'] # 简化所有GET和POST的模版
REGEX145=['^\"?\d+\.\d+\.\d+\.\d+.*(?!\s)\"*PUT.*HTTP/\d\.\d\"*\s3\d{2}.*$','<PUT_3XX> <PUT_3XX> <PUT_3XX>'] # 简化所有GET和POST的模版
REGEX146=['^\"?\d+\.\d+\.\d+\.\d+.*(?!\s)\"*PUT.*HTTP/\d\.\d\"*\s4\d{2}.*$','<PUT_4XX> <PUT_4XX> <PUT_4XX>'] # 简化所有GET和POST的模版
REGEX147=['^\"?\d+\.\d+\.\d+\.\d+.*(?!\s)\"*PUT.*HTTP/\d\.\d\"*\s5\d{2}.*$','<PUT_5XX> <PUT_5XX> <PUT_5XX>'] # 简化所有GET和POST的模版


REGEX148=['^REQ: curl -g -i -X POST.* _http_log_request','<REQ_POST> <REQ_POST> <REQ_POST>'] # 简化所有REQ的模版
REGEX149=['^REQ: curl -g -i -X GET.* _http_log_request','<REQ_GET> <REQ_GET> <REQ_GET>'] # 简化所有REQ的模版
REGEX150=['^REQ: curl -g -i -X DELETE.* _http_log_request','<REQ_DELETE> <REQ_DELETE> <REQ_DELETE>'] # 简化所有REQ的模版
REGEX151=['^RESP: \[1\d{2}\].*$','<RESP_1XX> <RESP_1XX> <RESP_1XX>'] # 简化所有RESP的模版
REGEX152=['^RESP: \[2\d{2}\].*$','<RESP_2XX> <RESP_2XX> <RESP_2XX>'] # 简化所有RESP的模版
REGEX153=['^RESP: \[3\d{2}\].*$','<RESP_3XX> <RESP_3XX> <RESP_3XX>'] # 简化所有RESP的模版
REGEX154=['^RESP: \[4\d{2}\].*$','<RESP_4XX> <RESP_4XX> <RESP_4XX>'] # 简化所有RESP的模版
REGEX155=['^RESP: \[5\d{2}\].*$','<RESP_5XX> <RESP_5XX> <RESP_5XX>'] # 简化所有RESP的模版



# 对一些常见的参数进行匹配
REGEX201= ['(0x)[0-9a-fA-F]+','<MemAddr>'] # 0xa829ce83
REGEX202= ['\d+\.\d+\.\d+\.\d+','<IPAddr>'] # 10.10.10.10
REGEX203=['\s\[\d+\/[a-zA-Z]+/\d+\s\d+:\d+:\d+\]',' <DateTime>'] # [18/Jun/2021 14:16:02]
REGEX204=['^\(\d+\)',' <ProcessId>'] # (30102)
REGEX205= ['\shttps?://([\w\.\:\d]+)(/[-_\w\.]+)*((\?).*)?(?=\s)',' <HTTPUri>'] # http://siels:1080/asdljw.json?aljsd=733&sldk=372
REGEX206= ['\s(/[-_\w\.]+)+\:\d+$',' <LogOccurAddr>'] # /sdlj.dksd/cljs/a/ew.py:383
REGEX207= ['\s(/[-_\w\.]+)+(\?).*(?=\s)',' <UriPath>'] # /v2.0/subnets.json?id=c197d80a-6716-46d7-b6a8-3fbf52d7bfc9
REGEX208= ['((?![\s\(\'\"])(/?[-_\w\.]+)(/[-_\w\.]+){2,}(?=[\s\)\'\"]))|((?![\s])(/?[-_\w\.]+)(/[-_\w\.]+){2,}$)','<Path>'] # /sdlj.dksd/cljs/a/ew.py
REGEX209=['[\'\"]?([0-9a-fA-F]+-)+([0-9a-fA-F]+)[\'\"]?','<InstanceId>'] # '16d1f7bc-11f1-4d23-95af-f0dce3f61667'
REGEX210=['[\'\"]?([0-9a-fA-F]{30,})[\'\"]?','<ID>'] # '16d1f7bc11f14d2395aff0dce3f61667'
REGEX211=['(?!\s)ComputeNode\(.*\)(?=\s)','<ComputNode>'] #  ComputeNode(cpu_allocation_ratio=16.0) 




options["regex"] = [REGEX101,REGEX102,REGEX103,REGEX104,REGEX105,REGEX106,REGEX107,REGEX108,REGEX109,REGEX110,\
                    REGEX111,REGEX112,REGEX113,REGEX114,REGEX115,REGEX116,REGEX117,REGEX118,REGEX119,REGEX120,\
                    REGEX121,REGEX122,REGEX123,REGEX124,REGEX125,REGEX126,REGEX127,REGEX128,REGEX129,REGEX130,\
                    REGEX131,REGEX132,REGEX133,REGEX134,REGEX135,REGEX136,REGEX137,REGEX138,REGEX139,REGEX140,\
                    REGEX141,REGEX142,REGEX143,REGEX144,REGEX145,REGEX146,REGEX147,REGEX148,REGEX149,REGEX150,\
                    REGEX151,REGEX152,REGEX153,REGEX154,REGEX155,\
                    REGEX201,REGEX202,REGEX203,REGEX204,REGEX205,REGEX206,REGEX207,REGEX208,REGEX209,REGEX210,\
                    REGEX211]

options["keep_para"] = False

options["st"] = 0.6
options["depth"] = 4
options["max_child"] = 100
options["tau"] = 0.5

options["window_type"] = "sliding_aiia"
options["window_size"] = 25
options["step_size"] = 1
options["train_size"] = 0.7

# evalue logs
options["evalue_files"] = ["evalue-"+str(i)+".txt" for i in range(0,10)]

# parser path
options["parserPickle_path"] = "/root/.output/aiia/parser.pkl"



# the main process
options["output_dir"] = os.path.expanduser(options["output_dir"])
options["data_dir"] = os.path.expanduser(options["data_dir"])

options["data_dir"] = os.path.join(options["data_dir"], options["dataset_name"] + "/")
options["output_dir"] = os.path.join(options["output_dir"], options["dataset_name"] + "/")


if not os.path.exists(options["output_dir"]):
    os.makedirs(options["output_dir"], exist_ok=True)


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

#for evalue_file in options["evalue_files"]:
for evalue_file in ["evalue_all.txt"]:
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
'''

