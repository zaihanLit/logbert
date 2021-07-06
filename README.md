# LogBERT: Log Anomaly Detection via BERT
### [ARXIV](https://arxiv.org/abs/2103.04475) 


This repository provides the implementation of Logbert for log anomaly detection. 
The process includes downloading raw data online, parsing logs into structured data, 
creating log sequences and finally modeling. 

## Prerequisites
- Linux or macOS
- Python 3
- NVIDIA GPU + CUDA cuDNN
- PyTorch
  

## Installation
This code is written in Python 3 and requires the packages listed in requirements.txt.
An virtual environment is recommended to run this code

On macOS and Linux:  
```
python3 -m pip install --user virtualenv
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
deactivate
```
Reference: https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/

## Experiment
We currently have implemented our model Logbert and other baseline models on [HDFS](https://github.com/logpai/loghub/tree/master/HDFS), [BGL](https://github.com/logpai/loghub/tree/master/BGL), and [thunderbird]() datasets

 ### HDFS example
 ```shell script
cd scripts

#download 2000 hdfs samples for testing and debugging
sh download_hdfs_2k.sh

#download hdfs dataset
sh download_hdfs.sh


#run logbert on HDFS
sh run_logbert_hdfs.sh


#run deeplog on HDFS
sh run_logdeep_hdfs.sh

#run loganomaly on HDFS by setting the corresponding parameters
sh run_logdeep_hdfs.sh

#run baselines

sh run_loglizer_hdfs.sh
```


## Docker Implementation

### 1. Use image published on docker hub
```shell script

```

### 2. Create your own docker image
1. Edit Dockerfile
```shell script

```
2. Build docker image









