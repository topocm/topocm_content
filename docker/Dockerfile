# Adopted from jupyter/docker-stacks Dockerfile's
# Copyright (c) 2016 Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

FROM debian@sha256:32a225e412babcd54c0ea777846183c61003d125278882873fb2bc97f9057c51

MAINTAINER Anton Akhmerov <anton.akhmerov@gmail.com>

USER root

RUN apt-get update && apt-get install -yq --no-install-recommends \
    dvipng \
    openssh-client \
    git \
    build-essential \
    python-dev \
    unzip \
    libsm6 \
    pandoc \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-extra \
    texlive-fonts-recommended \
    texlive-generic-recommended \
    libxrender1 \    
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -yq --no-install-recommends \
    wget \
    rsync \
    bzip2 \
    ca-certificates \
    sudo \
    locales \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

# Configure environment
ENV CONDA_DIR /opt/conda
ENV PATH $CONDA_DIR/bin:$PATH
ENV SHELL /bin/bash
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

RUN cd /tmp && \
    mkdir -p $CONDA_DIR && \
    wget --quiet https://repo.continuum.io/miniconda/Miniconda3-4.2.12-Linux-x86_64.sh && \
    echo "c59b3dd3cad550ac7596e0d599b91e75d88826db132e4146030ef471bb434e9a *Miniconda3-4.2.12-Linux-x86_64.sh" | sha256sum -c - && \
    /bin/bash Miniconda3-4.2.12-Linux-x86_64.sh -f -b -p $CONDA_DIR && \
    rm Miniconda3-4.2.12-Linux-x86_64.sh && \
    $CONDA_DIR/bin/conda install --quiet --yes conda==4.2.13 && \
    $CONDA_DIR/bin/conda config --system --add channels conda-forge && \
    conda install --quiet --yes \
    'ipywidgets=5.2.*' \
    'matplotlib=2.0.*' \
    'scipy=0.18*' \
    'sympy=1.0*' \
    'pelican=3.7.0' \
    'markdown=2.6.7' \
    'beautifulsoup4=4.5*' \
    'feedparser=5.2*' \
    'kwant=1.2.2' &&\
    conda clean -tipsy

RUN pip install https://github.com/ioam/holoviews/archive/master.zip
