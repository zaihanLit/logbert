
import os
import pickle
import pandas as pd
import time

from dataset import SimpleParserFactory, split_train_test_aiia, generate_test_set_aiia, sample_raw_data


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




normal_templates_df = pd.read_csv("/root/.output/aiia/normal.txt_templates.csv")
normal_templates_set = set(normal_templates_df['EventId'])

new_templates_set = set()
#for evalue_file in  options["evalue_files"]:
for evalue_file in  ["evalue_all.txt"]:
    evaluefile_path = options["output_dir"]+"evalue/" + evalue_file + "_templates.csv"   
    evalue_templates_df = pd.read_csv(evaluefile_path)
    evalue_templates_set = set(evalue_templates_df['EventId'])
    evalue_templates_set = evalue_templates_set - normal_templates_set

    #if len(evalue_templates_set)>0:
    #    print(evalue_file + ";" +str(evalue_templates_set))
    
    new_templates_set = new_templates_set | evalue_templates_set


templates_seq_df = pd.read_csv("~/.output/aiia/tempaltes_seq_df_2302.csv")

err_seq_df = templates_seq_df.loc[templates_seq_df['cnt']>15,'seq']

err_token_set = set()
for err_seq in err_seq_df:
    err_token_set |= set(eval(err_seq))

#err_seq_df = templates_seq_df['seq']

for evalue_file in options["evalue_files"]:
#for evalue_file in  ["evalue_all.txt"]:
#for evalue_file in  ["evalue-41.txt"]:
    evaluefile_path = options["output_dir"]+"evalue/" + evalue_file + "_structured.csv"   
    evalue_structured_df = pd.read_csv(evaluefile_path)

    start = 0
    end = start + options["window_size"]
    predictResult = 'Normal'
    StartLineNum = 0

    start_time = time.time()

    logDetail = list(evalue_structured_df['EventId'].apply(lambda v:1 if v in err_token_set else 0))

    for idx in range(0,int(len(evalue_structured_df)/options["step_size"])):
    #for idx in range(0,int(700/options["step_size"])):

        #print(idx)
        if end > len(evalue_structured_df):
            end = len(evalue_structured_df)

        eventid_seq_set = set(evalue_structured_df['EventId'].iloc[start:end])

        for err_seq_set in err_seq_df:
            if eval(err_seq_set) == eval(err_seq_set) & eventid_seq_set:
            #if err_seq_set == err_seq_set & eventid_seq_set:
                #print(evalue_file + ";"+str(err_seq_set))
                #print(start)

                if predictResult == 'Normal':
                    for i,token in enumerate(evalue_structured_df['EventId'].iloc[start:end]):
                        if token in err_token_set:
                            #print(token)
                            if i == 0:
                                StartLineNum = start + i
                                while (token in err_token_set) and (StartLineNum >=0):
                                    StartLineNum -= 1
                                    token = evalue_structured_df['EventId'].iloc[StartLineNum]
                                    #print(token)
                                StartLineNum = StartLineNum + 4
                            else:
                                StartLineNum = start + i + 3
                            #print(StartLineNum)
                            break
                predictResult = 'Anomaly'
                #print(start)
                #print(err_seq_set)
                break
        
        #if predictResult == 'Anomaly':
        #    break
        start = start + options["step_size"]
        #print(start)
        
        end = start + options["window_size"]

    elapsed_time = time.time() - start_time
    #print('elapsed_time: {}'.format(elapsed_time))
    #print(evalue_file[:-4] + "," +predictResult + "," +str(StartLineNum) + "," + str(logDetail) + "," + str(int(elapsed_time*1000))+"ms")
    print(evalue_file[:-4] + "," +predictResult + "," +str(StartLineNum) + "," + str(int(elapsed_time*1000))+"ms")

'f58326c9' in new_templates_set

pd.set_option('display.max_rows',None)
templates_seq_df

evalue_structured_df = pd.read_csv("/root/.output/aiia/evalue/evalue_all.txt_structured.csv")
total_eventid_seq = evalue_structured_df['EventId']

start = 0
end = start + options["window_size"]

templates_seq_df = pd.DataFrame(columns=['seq','cnt'])


for idx in range(0,int(len(total_eventid_seq)/options["step_size"])):
#for idx in range(0,int(700/options["step_size"])):

    #print(idx)

    start = start + options["step_size"]
    print(start)
    
    end = start + options["window_size"]

    if end <= len(total_eventid_seq):
        eventid_seq_set = set(total_eventid_seq.iloc[start:end])

        eventid_seq_set = eventid_seq_set & new_templates_set

        if len(eventid_seq_set)>=3:
            isNewSeq = True
            for i,row in templates_seq_df.iterrows():
 
                if len(eventid_seq_set&row['seq']) >= max(len(eventid_seq_set)-1,len(row['seq'])-1,3):
                    templates_seq_df.iloc[i,0] = eventid_seq_set&row['seq']
                    templates_seq_df.iloc[i,1] += 1
                    isNewSeq = False
                    break
            
            if isNewSeq == True:
                new_row = {'seq':eventid_seq_set, 'cnt':1}
                templates_seq_df = templates_seq_df.append(new_row,ignore_index=True)
        

templates_seq_df = templates_seq_df.sort_values('cnt',ascending=False)

templates_seq_df.to_csv("~/.output/aiia/tempaltes_seq_df_1001.csv", index= False)


'''
new_templates_matrix = pd.DataFrame(index=new_templates_list,columns=new_templates_list)

new_templates_matrix[new_templates_list] = 0

evalue_structured_df = pd.read_csv("/root/.output/aiia/evalue/evalue_all.txt_structured.csv")
total_eventid_seq = evalue_structured_df['EventId']

start = 0
end = start + options["window_size"]


for idx in range(0,int(len(total_eventid_seq)/options["step_size"])):
#for idx in range(0,int(700/options["step_size"])):

    #print(idx)

    start = start + options["step_size"]
    print(start)
    
    end = start + options["window_size"]

    if end <= len(total_eventid_seq):
        eventid_seq_set = set(total_eventid_seq.iloc[start:end])

        eventid_seq_set = eventid_seq_set & new_templates_set

        if len(eventid_seq_set) > 0:
            print(eventid_seq_set)
            for eventid in eventid_seq_set:

                #print(new_templates_matrix.loc[eventid_seq_set,eventid])

                new_templates_matrix.loc[eventid_seq_set,eventid] += 1

                #print(new_templates_matrix.loc[eventid_seq_set,eventid])



import matplotlib.pyplot as plt
import seaborn as sns



from sklearn.cluster import MeanShift, estimate_bandwidth
import numpy as np

new_templates_X = [list(row) for i,row in new_templates_matrix.iterrows()]

##带宽，也就是以某个点为核心时的搜索半径
bandwidth = estimate_bandwidth(new_templates_X, quantile=0.1, n_samples=50)

##设置均值偏移函数
#ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
ms = MeanShift()
##训练数据
ms.fit(new_templates_X)

##每个点的标签
labels = ms.labels_

##总共的标签分类
labels_unique = np.unique(labels)

labels_dict = dict()

for label in range(0,len(labels_unique)):
    labels_dict[label] = list(new_templates_matrix.index[labels==label])


pd.set_option('display.max_rows', None)
'''