# Dataset creation

In this document, `computer cluster` is a cluster that makes the real dataset, and `build machine` is a machine (possibly laptop computer) that do some preparation.

## Prerequirements
- Singularity installed in **BOTH** computer cluster and build machine
- Docker installed in build machine
- PBSPro installed in computer cluster

## How to run

1. Clone this repository to your build machine.

2. In build machine, run `cd generator_scripts; ./create_container.sh` to create singularity image.
This will create a `mnist.sif` file.

3. Upload folders to computer cluster.
Following commands will upload folders to computer cluster:
```[bash]
$ zip -r quantum_MNIST.zip quantum_MNIST
$ sftp <computer cluster name>
sftp> put quantum_MNIST.zip
$ ssh <computer cluster name>
ssh> $ unzip qulacs_MNIST.zip
```

4. In computer cluster, run `cd generator_scripts; python initialize.py`.
This will create zip files in `outcome` folder.

5. Upload all zip files in `outcome` folder to aws s3 or some file hosting service.
The default configuration uses url `https://qulacs-quantum-datasets.s3.us-west-1.amazonaws.com` as a download server.
