### This code is not parallel because is not useful parallel

"""I will generate 3 versions for every kernel
train
1) 1,000x1,000
2) 30,000x30,000
3) 60,000x60,000 (max)

test
1) 1,000x1,000
2) 5,000x5,000
3) 10,000x10,000 (max)
"""
    
    
#load all the paths for the datasets to loop on

# some imports
#from mpi4py import MPI
import os
import multiprocessing
import numpy as np
seed_value = 42  # for reproducibility

np.random.seed(seed_value)

from sklearn.model_selection import train_test_split
#from sklearn.preprocessing import LabelEncoder

from qasm_to_qulacs import convert_QASM_to_qulacs_circuit

from qulacs.gate import BitFlipNoise, DephasingNoise, IndependentXZNoise, DepolarizingNoise, TwoQubitDepolarizingNoise
#from qulacs import DensityMatrix
#from qulacs import QuantumCircuit
from qulacs.state import inner_product
from qulacs import QuantumState

#from sklearn.svm import SVC
#from sklearn import svm
#from sklearn.metrics import accuracy_score
#from sklearn.multiclass import OneVsOneClassifier
#from sklearn.multiclass import OneVsRestClassifier
import os
import pandas as pd

# Setup logging
import logging
def log_and_print(message):
    print(message)
    logging.info(message)

logging.basicConfig(filename= os.path.abspath(__file__) +'Ideals.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filemode='w')

 
log_and_print("Starting computation...")



#Import circuits
def import_circuits(path_qasm, path_label, data_type, lim):
    #lim = 976 #len(os.listdir(path_label))

    circuits_qasm = []
    labels = []

    for i in range(lim):
        with open(os.path.join(path_qasm, str(i))) as f:
            qasm = f.read()
            converted_qasm = convert_QASM_to_qulacs_circuit(qasm.split('\n'))

        with open(os.path.join(path_label, str(i))) as g:
            label = g.read()

        
        # Append the circuit and label to the respective lists
        circuits_qasm.append(converted_qasm)
        labels.append(label)

    # Convert the lists to numpy arrays (sometime is useful)
    circuits_array = np.array(circuits_qasm)
    labels_array = np.array(labels, dtype=int)
    log_and_print("type:{}".format(data_type))
    log_and_print("Number of circuits: {},".format(len(circuits_array)))
    log_and_print("Number of labels: {}".format(len(labels_array)))
    return circuits_array, labels_array

def compute_Ideal_kernel(c1, c2, num_qubits = 10):
    #state_a = QuantumState(num_qubits)
    #state_b = QuantumState(num_qubits)
    len_1 = c1.shape[0]
    len_2 = c2.shape[0]
    kernel_matrix = np.zeros((len_1, len_2))
    
    c1_states = []
    for i in range(len_1):
        state_a = QuantumState(num_qubits)
        state_a.set_zero_state()
        c1[i].update_quantum_state(state_a)
        c1_states.append(state_a.get_vector())

    if len_1 == len_2:
        for i in range(len_1):
            for j in range(len_2):
                if i>=j: 
                    value = abs(np.vdot(c1_states[i],c1_states[j])) ** 2
                    value = min(value, 1)
                    kernel_matrix[i][j] = value
                    kernel_matrix[j][i] = value
                     
    else:
        c2_states = []
        for i in range(len_2):
            state_a = QuantumState(num_qubits)
            state_a.set_zero_state()
            c2[i].update_quantum_state(state_a)
            c2_states.append(state_a.get_vector())
            
        for i in range(len_1):
            for j in range(len_2):
                value = abs(np.vdot(c1_states[i],c2_states[j])) ** 2
                value = min(value, 1)
                kernel_matrix[i][j] = value
        
    return kernel_matrix


# Loop through the subdirectories in the "data" directory
def process_folder(folder_name):
    Train_or_Test = 0  # 0 for Train
    folder_path = os.path.join(data_directory, folder_name)
    log_and_print(f"Processing data in folder: {folder_name}")

    ########## For the test kernel, you need test and training data
    if folder_name.startswith("test"):
        Train_or_Test = 1
        # Extract the test folder name without "test"
        test_folder_name = folder_name[4:]

        # Construct the corresponding "train" folder name (USED FOR THE KERNEL)
        train_folder_name = "train_orig" + test_folder_name

        ########### In this case, you need 2 sets of circuits (test and train)
        TEST_path_qasm = os.path.join(data_directory, folder_name, "qasm")  # change the dir if it does not work
        TEST_path_label = os.path.join(data_directory, folder_name, "label")
        log_and_print("train qasm path {}".format(TEST_path_qasm))
        TEST_circuits_array, labels_array = import_circuits(TEST_path_qasm, TEST_path_label, "data", len(os.listdir(TEST_path_label)))

        TRAIN_path_qasm = os.path.join(data_directory, train_folder_name, "qasm")  # change the dir if it does not work
        TRAIN_path_label = os.path.join(data_directory, train_folder_name, "label")
        log_and_print("train qasm path {}".format(TRAIN_path_qasm))
        TRAIN_circuits_array, TRAIN_labels_array = import_circuits(TRAIN_path_qasm, TRAIN_path_label, "data", len(os.listdir(TRAIN_path_label)))
        log_and_print("Kernel Computation...")
        Kernel = compute_Ideal_kernel(TEST_circuits_array, TRAIN_circuits_array)
        log_and_print("Kernel DONE")
    else:
        path_qasm = os.path.join(data_directory, folder_name, "qasm")  # change the dir if it does not work
        path_label = os.path.join(data_directory, folder_name, "label")
        log_and_print("qasm path {}".format(path_qasm))
        circuits_array, labels_array = import_circuits(path_qasm, path_label, "data", len(os.listdir(path_label)))
        log_and_print("Kernel Computation...")
        Kernel = compute_Ideal_kernel(circuits_array, circuits_array)
        log_and_print("Kernel DONE")

    # Now you have the kernel
    # Save it in a folder in npy format
    numpy_K = np.array(Kernel)

    if Train_or_Test == 0:
        k1 = numpy_K[:1000, :1000]
        k2 = numpy_K[:10000, :10000]
        np.save( "YOURPATH/" + folder_name + "_v1000.npy", k1)
        np.save( "YOURPATH/" + folder_name + "_v10000.npy", k2)
        np.save( "YOURPATH/" + folder_name + "_vFULL.npy", numpy_K)
    else:
        k1 = numpy_K[:1000, :1000]
        k2 = numpy_K[:5000, :5000]
        np.save( "YOURPATH/" + folder_name + "_v1000.npy", k1)
        np.save( "YOURPATH/" + folder_name + "_v5000.npy", k2)
        np.save( "YOURPATH/" + folder_name + "_vFULL.npy", numpy_K)
        
    np.save( "YOURPATH/LABELS_" + folder_name + ".npy", labels_array)

    del k1
    del k2
    del numpy_K
    log_and_print("DONE {}".format(folder_name))

if __name__ == "__main__":
    # Define the parent directory where "data" and "scripts" folders are located
    parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(parent_directory)
    # Define the path to the "data" directory
    data_directory = os.path.join(parent_directory, 'qulacs_data_folder')
    # Loop through the subdirectories sequentially
    folder_names = os.listdir(data_directory)
    for folder_name in folder_names:
        process_folder(folder_name)