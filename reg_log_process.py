import os
import re
import pandas as pd
import time


options = dict()

# directory path
options["dataset_name"] = "aiia"
options["data_dir"] = "~/.dataset/"
options["output_dir"] = "~/.output/"

# evalue logs
options["evalue_files"] = ["evalue-"+str(i)+".txt" for i in range(1123,1124)]

# the main process
options["output_dir"] = os.path.expanduser(options["output_dir"])
options["data_dir"] = os.path.expanduser(options["data_dir"])

options["data_dir"] = os.path.join(options["data_dir"], options["dataset_name"] + "/")
options["output_dir"] = os.path.join(options["output_dir"], options["dataset_name"] + "/")



regexString = "^\d+\s\d+.\d+.\d+.\d+.*GET.*404.*$"

pattern = re.compile(regexString)

df_result = pd.DataFrame(columns=['SequenceId','Result','StartLineNum','Detail','TimeCost'])

for evalue_file in options["evalue_files"]:
    print("Now processing "+evalue_file+".")
    evaluefile_path = os.path.join(options["data_dir"], "evalue/" + evalue_file)

    result = "Normal"
    firstlineNum = 0
    outputList = []
    elapsed_time = 0

    with open(evaluefile_path, 'r') as fin:
        start_time = time.time()
        cnt = 0
        for line in fin.readlines():
            cnt += 1
            match = pattern.match(line.strip())
            if match is not None:
                #print(line)
                outputList.append(1)
            else:
                outputList.append(0)

            if len(outputList)>=10:
                if sum(outputList[-10:])>=3:
                    result = "Anomaly"
                    elapsed_time = int((time.time() - start_time) * 100000)
                    if firstlineNum==0:
                        firstlineNum=cnt
            elif sum(outputList)>=3:
                    result = "Anomaly"
                    elapsed_time = int((time.time() - start_time) * 100000)
                    if firstlineNum==0:
                        firstlineNum=cnt
            
        new_row = {'SequenceId':evalue_file.strip(".txt"), "Result":result,"StartLineNum":firstlineNum,"Detail":outputList,"TimeCost":str(elapsed_time)+"ms"}
        df_result = df_result.append(new_row,ignore_index=True)

df_result.to_csv(options["output_dir"]+"result_reg.csv", index=False)

        



            

            

