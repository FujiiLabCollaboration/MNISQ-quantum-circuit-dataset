#!/bin/bash

docker build ../ -f ../.devcontainer/Dockerfile -t quantum_mnist_dataset_container
singularity build mnist.sif docker-daemon://quantum_mnist_dataset_container:latest
