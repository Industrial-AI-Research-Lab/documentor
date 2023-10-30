FROM nvidia/cuda:12.1.0-cudnn8-devel-ubuntu22.04

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /opt/conda/bin:$PATH

RUN apt-get update && apt-get install -y git apt-utils wget supervisor nano


RUN wget --quiet https://repo.anaconda.com/archive/Anaconda3-2023.07-2-Linux-x86_64.sh -O ~/anaconda.sh && \
    /bin/bash ~/anaconda.sh -b -p /opt/conda && \
    rm ~/anaconda.sh && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc

RUN /opt/conda/bin/pip install --upgrade pip
RUN /opt/conda/bin/conda update -n base -c defaults conda
RUN /opt/conda/bin/conda install -c conda-forge jupyterlab>=3.4.5
RUN /opt/conda/bin/pip install setuptools wheel
RUN /opt/conda/bin/conda install ipykernel

RUN /opt/conda/bin/conda install -c plotly plotly=5.6.0
RUN /opt/conda/bin/conda install -c conda-forge jupyterlab_widgets

RUN /opt/conda/bin/pip install openpyxl


RUN /opt/conda/bin/pip install scipy ftfy
RUN /opt/conda/bin/pip install "ipywidgets>=7,<8"

# для корректной работы plotly
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get -y install nodejs
RUN /opt/conda/bin/jupyter labextension install jupyterlab-plotly@5.6.0

RUN apt-get install -y sudo
RUN mkdir -p /mnt/ess_storage/DN_1/
RUN mkdir /home/jovyan && chmod 777 /home/jovyan 
RUN mkdir /home/jovyan/notebooks && chmod 777 /home/jovyan/notebooks