from mnisq.mnist import *
from mnisq.fashion_mnist import *
from mnisq.kuzushiji_mnist import *
from names import set_names

from os import makedirs
import pickle

load_funcs = [
    load_mnist_original_f80,
    load_mnist_original_f90,
    load_mnist_original_f95,
    load_mnist_test_f80,
    load_mnist_test_f90,
    load_mnist_test_f95,
    load_Fashion_original_f80,
    load_Fashion_original_f90,
    load_Fashion_original_f95,
    load_Fashion_test_f80,
    load_Fashion_test_f90,
    load_Fashion_test_f95,
    load_Kuzushiji_original_f80,
    load_Kuzushiji_original_f90,
    load_Kuzushiji_original_f95,
    load_Kuzushiji_test_f80,
    load_Kuzushiji_test_f90,
    load_Kuzushiji_test_f95,
]

for i in range(len(set_names)):
    dataset = load_funcs[i]()
    dirname = 'data/%s' % set_names[i]
    makedirs(dirname, exist_ok=True)
    circuit_list = dataset['circuit']
    for i in range(len(circuit_list)):
        with open('%s/circuit_%05d.pickle' % (dirname, i), 'wb') as f:
            pickle.dump(circuit_list[i], f)
