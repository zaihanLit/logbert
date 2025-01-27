# LogBERT: Log Anomaly Detection via BERT
### [ARXIV](https://arxiv.org/abs/2103.04475) 


This repository provides the implementation of Logbert for log anomaly detection. 
The process includes downloading raw data online, parsing logs into structured data, 
creating log sequences and finally modeling. 

<<<<<<< HEAD
![alt](img/log_preprocess.png)

## Configuration
- Ubuntu 20.04
- NVIDIA driver 460.73.01 
- CUDA 11.2
- Python 3.8
- PyTorch 1.9.0

  

## Installation
This code requires the packages listed in requirements.txt.
=======
## Prerequisites
- Linux or macOS
- Python 3
- NVIDIA GPU + CUDA cuDNN
- PyTorch 1.6
  

## Installation
This code is written in Python 3.8 and requires the packages listed in requirements.txt.
>>>>>>> 3432d4403b1caf05c83f3f9eefa83bb5e41aafef
An virtual environment is recommended to run this code

On macOS and Linux:  
```
python3 -m pip install --user virtualenv
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
<<<<<<< HEAD
deactivate
```
Reference: https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/

## Experiment
Logbert and other baseline models are implemented on [HDFS](https://github.com/logpai/loghub/tree/master/HDFS), [BGL](https://github.com/logpai/loghub/tree/master/BGL), and [thunderbird]() datasets
=======
```

## Experiment
We currently have implemented our model Logbert and other baseline models on [HDFS](https://github.com/logpai/loghub/tree/master/HDFS), [BGL](https://github.com/logpai/loghub/tree/master/BGL), and [thunderbird]() datasets
>>>>>>> 3432d4403b1caf05c83f3f9eefa83bb5e41aafef

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


<<<<<<< HEAD
## Docker Implementation
### How to use docker with NVIDIA GPU

1. Type ```nvidia-smi```  and check NVIDIA driver and  CUDA version. According to [this](https://docs.nvidia.com/deploy/cuda-compatibility/index.html), CUDA 11.2 requires NVIDIA driver version >= 450.80.02

2. Set up NVIDIA Container Toolkit following this [tutorial](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)

3. Refer [this](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/user-guide.html#id2) to set up parameters for docker with NVIDIA GPU

<b>You can choose either of the two docker methods below</b>
### Use image published on docker hub
```shell script
docker pull haixuanguo/logbert:1.0

docker run --gpus all -it haixuanguo/logbert:1.0

```

### Create your own docker image
```shell script
docker build -t logbert:1.1 .

docker run --gpus all -it haixuanguo/logbert:1.1

```





## Citation

If you find this useful for your research, please cite the following paper.
```
@InProceedings{guo_logbert_2021_ijcnn,
author = {Haixuan Guo, Shuhan Yuan and Xintao Wu},
title = {LogBERT: Log Anomaly Detection via BERT},
booktitle = {Proceedings of the International Conference on Neural Networks (IJCNN)},
month = {July 18-22},
year = {2021}
}

```
=======
## Docker Installment
>>>>>>> 3432d4403b1caf05c83f3f9eefa83bb5e41aafef


