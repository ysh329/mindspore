FROM nvidia/cuda:10.1-cudnn7-devel-ubuntu18.04

MAINTAINER leonwanghui <leon.wanghui@huawei.com>

# Set env
ENV PYTHON_ROOT_PATH /usr/local/python-3.7.5
ENV CMAKE_ROOT_PATH /usr/local/cmake-3.14.1
ENV OMPI_ROOT_PATH /usr/local/openmpi-4.0.3
ENV PATH ${OMPI_ROOT_PATH}/bin:${PYTHON_ROOT_PATH}/bin:${CMAKE_ROOT_PATH}/bin:/usr/local/bin:$PATH
ENV LD_LIBRARY_PATH ${OMPI_ROOT_PATH}/lib::${PYTHON_ROOT_PATH}/lib

# Install base tools
RUN apt update \
    && DEBIAN_FRONTEND=noninteractive apt install -y \
    vim \
    wget \
    curl \
    xz-utils \
    net-tools \
    openssh-client \
    git \
    ntpdate \
    tzdata \
    tcl \
    sudo \
    bash-completion

# Install compile tools
RUN DEBIAN_FRONTEND=noninteractive apt install -y \
    gcc \
    g++ \
    zlibc \
    make \
    libgmp-dev \
    patch \
    autoconf \
    libtool \
    automake \
    flex

# Install the rest dependent tools
RUN DEBIAN_FRONTEND=noninteractive apt install -y \
    libnuma-dev

# Configure cuDNN (v7.6.5)
RUN ln -s /usr/lib/x86_64-linux-gnu/libcudnn.so.7.6.5 /usr/local/cuda/lib64/libcudnn.so

# Set bash
RUN echo "dash dash/sh boolean false" | debconf-set-selections
RUN DEBIAN_FRONTEND=noninteractive dpkg-reconfigure dash

# Install python (v3.7.5)
RUN apt install -y libffi-dev libssl-dev zlib1g-dev libbz2-dev libncurses5-dev \
    libgdbm-dev libgdbm-compat-dev liblzma-dev libreadline-dev libsqlite3-dev \
    && cd /tmp \
    && wget https://github.com/python/cpython/archive/v3.7.5.tar.gz \
    && tar -xvf v3.7.5.tar.gz \
    && cd /tmp/cpython-3.7.5 \
    && mkdir -p ${PYTHON_ROOT_PATH} \
    && ./configure --prefix=${PYTHON_ROOT_PATH} --enable-shared \
    && make -j4 \
    && make install -j4 \
    && rm -f /usr/local/bin/python \
    && rm -f /usr/local/bin/pip \
    && ln -s ${PYTHON_ROOT_PATH}/bin/python3.7 /usr/local/bin/python \
    && ln -s ${PYTHON_ROOT_PATH}/bin/pip3.7 /usr/local/bin/pip \
    && rm -rf /tmp/cpython-3.7.5 \
    && rm -f /tmp/v3.7.5.tar.gz

# Set pip source
RUN mkdir -pv /root/.pip \
    && echo "[global]" > /root/.pip/pip.conf \
    && echo "trusted-host=mirrors.aliyun.com" >> /root/.pip/pip.conf \
    && echo "index-url=http://mirrors.aliyun.com/pypi/simple/" >> /root/.pip/pip.conf \
    && pip install --no-cache-dir wheel

# Install cmake (v3.14.1)
RUN cd /tmp \
    && wget https://github.com/Kitware/CMake/releases/download/v3.14.1/cmake-3.14.1-Linux-x86_64.sh \
    && mkdir -p ${CMAKE_ROOT_PATH} \
    && bash ./cmake-3.14.1-Linux-x86_64.sh --prefix=${CMAKE_ROOT_PATH} --exclude-subdir --skip-license \
    && rm -f /tmp/cmake-3.14.1-Linux-x86_64.sh

# Install openmpi (v4.0.3)
RUN cd /tmp \
    && wget https://download.open-mpi.org/release/open-mpi/v4.0/openmpi-4.0.3.tar.gz \
    && tar -xvf openmpi-4.0.3.tar.gz \
    && cd /tmp/openmpi-4.0.3 \
    && mkdir -p ${OMPI_ROOT_PATH} \
    && ./configure --prefix=${OMPI_ROOT_PATH} \
    && make -j4 \
    && make install -j4 \
    && rm -rf /tmp/openmpi-4.0.3 \
    && rm -f /tmp/openmpi-4.0.3.tar.gz