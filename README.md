# MNISQ: A Large-Scale Quantum Circuit Dataset for Machine Learning on/for Quantum Computers in the NISQ era

Welcome to MNISQ, a powerful resource designed to propel Quantum Machine Learning forward during the NISQ era. As we undergo the review process, anticipate exciting additions in the near future!

## Accessing the Datasets
Our datasets are now fully accessible, offering a plethora of opportunities for exploration and experimentation.

### Executing with Qiskit
To leverage the dataset using Qiskit, refer to our comprehensive guide: [Qiskit Quickstart Notebook](doc/source/notebooks/qiskit_quickstart.ipynb).

### Executing with PennyLane
For executing the dataset using PennyLane, we've prepared a dedicated guide: [PennyLane Tutorial Notebook](doc/source/notebooks/Tutorial_Pennylane.ipynb).

### Local Dataset Download
Should you prefer working with datasets locally and employing the standard QASM formalism, our guide [Downloading Datasets](doc/source/notebooks/download_datasets.py) will walk you through the process.

## Getting Started
Embark on your journey with the MNISQ dataset and Quantum Machine Learning experiments.

Join us in pushing the boundaries of Quantum Machine Learning during the NISQ era! Your exploration starts here.


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

# Contributors
This project was developed by:
- Koki Aoyama(@kotamanegi)
- Hayata Morisaki
- Kouki Kawamura(@KowerKoint)
- Toshio Mori(@forest1040)
- Leonardo Placidi(@Gruntrexpewrus)
- Ryuichiro Hataya
- Kosuke Mitarai
- Keisuke Fujii

## Citation

If you find the MNISQ dataset valuable for your research or work, please consider citing our paper:

```
@misc{placidi2023mnisq,
      title={MNISQ: A Large-Scale Quantum Circuit Dataset for Machine Learning on/for Quantum Computers in the NISQ era}, 
      author={Leonardo Placidi and Ryuichiro Hataya and Toshio Mori and Koki Aoyama and Hayata Morisaki and Kosuke Mitarai and Keisuke Fujii},
      year={2023},
      eprint={2306.16627},
      archivePrefix={arXiv},
      primaryClass={quant-ph}
}
```

Your acknowledgment helps us in further advancing the field of Quantum Machine Learning and fostering a collaborative research community.
