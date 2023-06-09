ARG VARIANT

FROM mcr.microsoft.com/vscode/devcontainers/python:0-3.9-bullseye

# Requires $POETRY_HOME to install the location; poetry is installed under /root by default.
ENV POETRY_HOME=/home/vscode/.local/share/pypoetry
ENV PATH="${POETRY_HOME}/bin:${PATH}"

RUN curl -sSL https://install.python-poetry.org | python3 -


ENV DEBIAN_FRONTEND=noninteractive

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
  libboost-dev \
  && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

RUN pip install -U pip \
  && pip install black flake8 mypy openfermion pybind11-stubgen

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
RUN git clone -b json-dev https://github.com/qulacs/qulacs.git --depth 1 /tmp/qulacs \
  && cd /tmp/qulacs \
  && ./script/build_gcc.sh \
  && cp -r include/* /usr/local/include \
  && cp -r lib/* /usr/local/lib
