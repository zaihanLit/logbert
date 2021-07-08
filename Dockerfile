FROM nvidia/cuda:11.2.0-cudnn8-runtime-ubuntu20.04
ARG PYTHON_VERSION=3.8
ARG DEBIAN_FRONTEND="noninteractive"

RUN apt-get update && apt-get -y upgrade && apt-get install -y --no-install-recommends \
         build-essential \
         cmake \
	     wget sudo git vim curl \
	     tzdata \
         ca-certificates \
         libgtk2.0-dev \
         libjpeg-dev \
         libpng-dev && \
     rm -rf /var/lib/apt/lists/*

RUN curl -o ~/miniconda.sh -L -O  https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh  && \
     chmod +x ~/miniconda.sh && \
     ~/miniconda.sh -b -p /opt/conda && \
     rm ~/miniconda.sh && \
     /opt/conda/bin/conda install -y python=$PYTHON_VERSION

ENV PATH /opt/conda/bin:$PATH

WORKDIR /workspace

COPY requirements.txt .
COPY . logbert/
RUN python -m pip install -r requirements.txt

CMD python -c "import torch; device = torch.device('cuda' if torch.cuda.is_available() else 'cpu'); print('Using device:', device); torch.rand(10).to(device)"
