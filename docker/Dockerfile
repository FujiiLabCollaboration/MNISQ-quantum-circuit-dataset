#FROM mcr.microsoft.com/vscode/devcontainers/python:0-3.9-bullseye
FROM ubuntu:20.04


ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Tokyo

ENV USE_TEST="Yes"
# Add build artifact to PYTHONPATH and python can find qulacs.
# Egg file name might vary depending on qulacs and python version.
ENV PYTHONPATH="/qulacs/dist:${PYTHONPATH}"
ENV PYTHONPATH="/qulacs/build:${PYTHONPATH}"

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  clang-format \
  gdb \
  cmake \
  curl \
  libboost-dev \
  git \
  wget \
  make \
  build-essential \
  gcc \
  g++ \
  software-properties-common \
  && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# python
RUN add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends \
    python3.9 \
    python3.9-dev \
    python3.9-tk \
    python3-distutils

RUN rm /usr/bin/python3 && \
    wget https://bootstrap.pypa.io/get-pip.py && \
    python3.9 get-pip.py && \
    ln -s /usr/bin/python3.9 /usr/bin/python3 && \
    ln -s /usr/bin/python3.9 /usr/bin/python && \
    ln -s /usr/bin/pip3.9 /usr/bin/pip

RUN pip install -U pip \
  && pip install black flake8 mypy openfermion pybind11-stubgen poetry

# Install cereal
RUN git clone https://github.com/USCiLab/cereal.git -b v1.3.0 --depth 1 /tmp/cereal \
  && cp -r /tmp/cereal/include/cereal /usr/local/include \
  && rm -rf /tmp/cereal

# Install Eigen
RUN git clone https://gitlab.com/libeigen/eigen.git -b 3.3.7 --depth 1 /tmp/eigen \
  && cp -r /tmp/eigen/Eigen /usr/local/include \
  && rm -rf /tmp/eigen

# Install Google Test
RUN git clone https://github.com/google/googletest.git -b release-1.8.1 --depth 1 /tmp/gtest \
  && cp -r /tmp/gtest/googletest/include/gtest /usr/local/include \
  && rm -rf /tmp/gtest

# Install pybind11
RUN git clone https://github.com/pybind/pybind11.git -b v2.10.0 --depth 1 /tmp/pybind11 \
  && cp -r /tmp/pybind11/include/pybind11 /usr/local/include \
  && rm -rf /tmp/pybind11

# Install lcov
RUN git clone https://github.com/linux-test-project/lcov.git -b v1.15 --depth 1 /tmp/lcov \
  && cd /tmp/lcov \
  && make install \
  && cd - \
  && rm -rf /tmp/lcov

# Install qulacs
RUN git clone https://github.com/qulacs/qulacs.git --depth 1 /tmp/qulacs \
  && cd /tmp/qulacs \
  && ./script/build_gcc.sh \
  && pip install . \
  && cp -r include/* /usr/local/include \
  && cp -r lib/* /usr/local/lib

# AQCE build
COPY AQCE.cpp .
RUN g++ ./AQCE.cpp -o ./AQCE.out -lcppsim_static -lcsim_static -lvqcsim_static -fopenmp \
  && cp ./AQCE.out /usr/local/bin

# poetry
COPY pyproject.toml .
RUN poetry install
