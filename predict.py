
import os
import pandas as pd
import time

# define options
options=dict()

# directory path
options["dataset_name"] = "aiia"
options["data_dir"] = "~/.dataset/"
options["output_dir"] = "~/.output/"

# log file name
options["log_file"] = "normal.txt"


options["window_size"] = 25
options["step_size"] = 10


# evalue logs
options["evalue_files"] = ["evalue-"+str(i)+".txt" for i in range(0,1124)]

# parser path
options["parserPickle_path"] = "/root/.output/aiia/parser.pkl"


# the main process
options["output_dir"] = os.path.expanduser(options["output_dir"])
options["data_dir"] = os.path.expanduser(options["data_dir"])

options["data_dir"] = os.path.join(options["data_dir"], options["dataset_name"] + "/")
options["output_dir"] = os.path.join(options["output_dir"], options["dataset_name"] + "/")

print("Now predicting...")

templates_seq_df = pd.read_csv("~/.output/aiia/tempaltes_seq_df.csv")
err_seq_df = templates_seq_df.loc[templates_seq_df['cnt']>15,'seq']

err_token_set = set()
for err_seq in err_seq_df:
    err_token_set |= set(eval(err_seq))

result_df = pd.DataFrame(columns=['SequenceId','Result','StartLineNum','Detail','TimeCost'])


for evalue_file in options["evalue_files"]:
    evaluefile_path = options["output_dir"]+"evalue/" + evalue_file + "_structured.csv"   
    evalue_structured_df = pd.read_csv(evaluefile_path)

    start = 0
    end = start + options["window_size"]
    predictResult = 'Normal'
    StartLineNum = 0

    start_time = time.time()

    logDetail = list(evalue_structured_df['EventId'].apply(lambda v:1 if v in err_token_set else 0))

    for idx in range(0,int(len(evalue_structured_df)/options["step_size"])):

        if end > len(evalue_structured_df):
            end = len(evalue_structured_df)

        eventid_seq_set = set(evalue_structured_df['EventId'].iloc[start:end])

        for err_seq_set in err_seq_df:
            if eval(err_seq_set) == eval(err_seq_set) & eventid_seq_set:

                if predictResult == 'Normal':
                    for i,token in enumerate(evalue_structured_df['EventId'].iloc[start:end]):
                        if token in err_token_set:

                            if i == 0:
                                StartLineNum = start + i
                                while (token in err_token_set) and (StartLineNum >=0):
                                    StartLineNum -= 1
                                    token = evalue_structured_df['EventId'].iloc[StartLineNum]

                                StartLineNum = StartLineNum + 4
                            else:
                                StartLineNum = start + i + 3

                            break
                predictResult = 'Anomaly'

                break
        
        start = start + options["step_size"]
        end = start + options["window_size"]

    elapsed_time = time.time() - start_time
    print(evalue_file[:-4] + "," +predictResult + "," +str(StartLineNum) + "," + str(logDetail) + "," + str(int(elapsed_time*1000))+"ms")
    new_row = {"SequenceId":evalue_file[:-4],"Result":predictResult,"StartLineNum":str(StartLineNum),"Detail":str(logDetail),"TimeCost":str(int(elapsed_time*1000))+"ms"}
    result_df = result_df.append(new_row,ignore_index=True)

result_df.to_csv(options["output_dir"]+"result.csv", index = False)
print("Done.")
print("Results saved to "+options["output_dir"]+"result.csv")


