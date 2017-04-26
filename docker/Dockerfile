# Adopted from jupyter/docker-stacks Dockerfile's
# Copyright (c) 2016 Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

FROM debian@sha256:32a225e412babcd54c0ea777846183c61003d125278882873fb2bc97f9057c51

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
    parallel \
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
    wget --quiet https://repo.continuum.io/miniconda/Miniconda3-4.3.11-Linux-x86_64.sh && \
    /bin/bash Miniconda3-4.3.11-Linux-x86_64.sh -f -b -p $CONDA_DIR && \
    rm Miniconda3-4.3.11-Linux-x86_64.sh

# Add environment file
COPY python3.yaml .

RUN conda env update -n root -f python3.yaml && conda clean -tipsy
