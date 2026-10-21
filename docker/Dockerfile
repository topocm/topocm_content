# A separate public-CA stage protects even legacy bases without a CA bundle.
# Package indexes/packages are authenticated by Debian's archive signatures.
FROM debian:bookworm-slim AS emudhra-trust
COPY sanitize-ca-bundle.sh /usr/local/bin/sanitize-ca-bundle
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates \
    && mkdir -p /usr/local/share/emudhra /etc/ssl/empty \
    && cp /etc/ssl/certs/ca-certificates.crt /usr/local/share/emudhra/ca-certificates.crt \
    && sh /usr/local/bin/sanitize-ca-bundle /usr/local/share/emudhra/ca-certificates.crt

# Adopted from jupyter/docker-stacks Dockerfile's
# Copyright (c) 2016 Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

FROM debian@sha256:32a225e412babcd54c0ea777846183c61003d125278882873fb2bc97f9057c51
COPY --from=emudhra-trust /usr/local/share/emudhra /usr/local/share/emudhra
COPY --from=emudhra-trust /etc/ssl/empty /etc/ssl/empty
COPY --from=emudhra-trust /usr/local/bin/sanitize-ca-bundle /usr/local/bin/sanitize-ca-bundle
ENV SSL_CERT_FILE=/usr/local/share/emudhra/ca-certificates.crt \
    SSL_CERT_DIR=/etc/ssl/empty \
    REQUESTS_CA_BUNDLE=/usr/local/share/emudhra/ca-certificates.crt \
    CURL_CA_BUNDLE=/usr/local/share/emudhra/ca-certificates.crt \
    PIP_CERT=/usr/local/share/emudhra/ca-certificates.crt \
    CONDA_SSL_VERIFY=/usr/local/share/emudhra/ca-certificates.crt \
    MAMBA_SSL_VERIFY=/usr/local/share/emudhra/ca-certificates.crt \
    GIT_SSL_CAINFO=/usr/local/share/emudhra/ca-certificates.crt \
    NODE_OPTIONS=--use-openssl-ca \
    UV_NATIVE_TLS=true UV_SYSTEM_CERTS=true DENO_TLS_CA_STORE=system


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
    wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-py39_4.10.3-Linux-x86_64.sh && \
    /bin/bash Miniconda3-py39_4.10.3-Linux-x86_64.sh -f -b -p $CONDA_DIR && \
    rm Miniconda3-py39_4.10.3-Linux-x86_64.sh && \
    conda install mamba -n base -c conda-forge

# Add environment file
COPY environment.yml .

RUN mamba env update -n base -f environment.yml && mamba clean --all -y

# setting openblas and mkl variables
ENV OPENBLAS_NUM_THREADS=1\
    OMP_NUM_THREADS=1\
    MKL_DYNAMIC=FALSE\
    MKL_NUM_THREADS=1

USER root
RUN find /opt /usr/local/lib /etc/ssl -type f \( -name cacert.pem -o -name ca-certificates.crt \) \
    -exec sh /usr/local/bin/sanitize-ca-bundle {} \;
USER root
