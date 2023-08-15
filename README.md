# MNISQ: A Large-Scale Quantum Circuit Dataset for Machine Learning on/for Quantum Computers in the NISQ era
We are in the review process so there will soon be some additions!

===> datasets are fully accessible!


- 1  we made the dataset executable from qiskit! See [doc/source/notebooks/qiskit_quickstart.ipynb](doc/source/notebooks/qiskit_quickstart.ipynb)

- 2 we made the dataset executable from pennylane! See [doc/source/notebooks/Tutorial_Pennylane.ipynb](doc/source/notebooks/Tutorial_Pennylane.ipynb)

- 3 if you want to donwload locally the datasets with the normals QASM formalism, use [doc/source/notebooks/download_datasets.py](doc/source/notebooks/download_datasets.py)


There is already the dataset and qml experiments, some guide can be found in doc/sources


This library provides machine learning datasets as a Qulacs's QuantumCircuit instance.

## How To Install

### pypi
```
pip install mnisq
```

### source install
```
pip install git+https://github.com/FujiiLabCollaboration/MNISQ-quantum-circuit-dataset.git
```

## Directory structure
- `doc/source/notebooks` provides sample usage of this library.
- `mnisq` and `tests` contains python code.
- `generator_scripts` contains scripts used to generate datasets.


## Dataset accessibility
### Data Construction
The datasets we created are easily accessible through the MNISQ library (currently in preparation). To install the library from PyPI, use the command: `pip install mnisq`.

The library automatically downloads predefined quantum circuits for Qulacs (Quantum Circuit Simulator), which are ready for use. When executing a circuit starting from the initial zero state, one of the images from the dataset is embedded in the quantum state.

**Note**: The QASM files come in two different forms:

- *QASM with Dense() formalism*: These files can be used in qulacs, but not on qiskit or other platforms due to the proprietary Dense() operator.
- *Base QASM formalism*: **These files are compatible with any platform, including qiskit**. You can find a tutorial on how to run them on our GitHub page at the following link: [tutorial link](https://github.com/FujiiLabCollaboration/MNISQ-quantum-circuit-dataset/blob/main/doc/source/notebooks/qiskit_quickstart.ipynb). Please note that to access these files, they begin with the prefix *"base\_"*.

The datasets can be found at the following URL:

`https://qulacs-quantum-datasets.s3.us-west-1.amazonaws.com/[data]_[type]_[fidelity].zip`

Here are the parameters for the URL:

- **data**:
  1. **"train_orig"** (60,000 original encoded training data, QASM files with *Dense()* formalism).
  2. **"base_train_orig"** (same as above but the QASM files do not include *Dense()* operator, but a gate conversion. Can be run on qiskit and other platforms).
  3. **"train"**: "train_orig" but augmented to 480,000 training data for each subdataset. *Dense()* formalism.
  4. **"test"**: 10,000 test element from original encoding. QASM files with *Dense()* formalism.
  5. **"base_test"**: same as above but the QASM files do not include *Dense()* operator, but a gate conversion. Can be run on qiskit and other platforms.

- **type**:
  1. **"mnist_784"**: MNIST dataset.
  2. **"Fashion-MNIST"**
  3. **"Kuzushiji-MNIST"**

- **fidelity**:
  1. **"f80"**: fidelity greater than or equal to 80%.
  2. **"f90"**: fidelity greater than or equal to 90%.
  3. **"f95"**: fidelity greater than or equal to 95%.

Example: [https://qulacs-quantum-datasets.s3.us-west-1.amazonaws.com/test_mnist_784_f90.zip](https://qulacs-quantum-datasets.s3.us-west-1.amazonaws.com/test_mnist_784_f90.zip)

# Contributor
This project was developed by:
- Koki Aoyama(@kotamanegi)
- Hayata Morisaki
- Kouki Kawamura(@KowerKoint)
- Toshio Mori(@forest1040)
- Leonardo Placidi(@Gruntrexpewrus)
- Ryuichiro Hataya
- Kosuke Mitarai
- Keisuke Fujii
