# Here I code the series of kernels and save the results of the trainings in a pandas dataset.
#I also print some stuff and save it as a log file to see
import numpy as np
from qulacs import QuantumState

from sklearn.svm import SVC
from sklearn.multiclass import OneVsOneClassifier
import os
import pandas as pd
######### setting a seed for reproducibility purposes
seed = 7
np.random.seed(seed)
################################
# Create an empty dataset as a DataFrame
dataset_to_save = pd.DataFrame(columns=["dataset", "accuracy"])

import sys
sys.path.append('/home/leonardo/Research/quantum_MNIST')
import mnisq as qs


from tqdm import tqdm

#file = "/logs.txt"
#name = "/home/leonardo/Research/quantum_MNIST/leo_dev" 
#sys.stdout = open(name+file, "w")
print("Here starts the code")
print(">>>>>>>>>>>>>>>>>>>>>>>>>")


datasets = {"mnist80" : [qs.load_mnist_original_f80, qs.load_mnist_test_f80],
            "mnist90" : [qs.load_mnist_original_f90, qs.load_mnist_test_f90],
            "mnist95" : [qs.load_mnist_original_f95, qs.load_mnist_test_f95],
            "fashion80" : [qs.load_Fashion_original_f80, qs.load_Fashion_test_f80], 
            "fashion90" : [qs.load_Fashion_original_f90, qs.load_Fashion_test_f90],
            "fashion95" : [qs.load_Fashion_original_f95, qs.load_Fashion_test_f95],
            "Kaz80" : [qs.load_Kuzushiji_original_f80, qs.load_Kuzushiji_test_f80],
            "Kaz90" : [qs.load_Kuzushiji_original_f90, qs.load_Kuzushiji_test_f90], 
            "Kaz95" : [qs.load_Kuzushiji_original_f95, qs.load_Kuzushiji_test_f95]}

order = ["mnist80", "mnist90", "mnist95", "fashion80", "fashion90", "fashion95", "Kaz80","Kaz90", "Kaz95"]

for dataset in order:
    print("Dataset in progress is: ", dataset)
    #########access data
    print("accessing data train")
    train_data = datasets[dataset][0]()
    print("accessing data test")
    test_data = datasets[dataset][1]()
    
    labels_train = train_data["label"]
    states_train = train_data["state"]
    labels_train = np.array(labels_train, dtype=int)
    
    labels_test = test_data["label"]
    states_test = test_data["state"]
    labels_test = np.array(labels_test, dtype=int)
    
    ############# create the quantum_x_train
    quantum_x_train_ = []
    L = len(states_train)
    for i in range(L):
        quantum_x_train_.append(states_train[i].get_vector())
     
    quantum_x_train = np.vstack(quantum_x_train_)
    print("example of quantum state TRAIN", quantum_x_train[0])
    ############# create the quantum_x_test
    quantum_x_test_ = []
    L = len(states_test)
    for i in range(L):
        quantum_x_test_.append(states_test[i].get_vector())
     
    quantum_x_test = np.vstack(quantum_x_test_)
    print("example of quantum state TEST", quantum_x_test[0])
    ############### generate first kernel
    
    # use the same circuit as scikit-qulacs do.
    clf = OneVsOneClassifier(SVC(kernel="precomputed"))
    print("calculating kernel")
    
    len_train = len(quantum_x_train)
    
    train_kernel = np.zeros((len_train, len_train))
    for i in tqdm(range(len_train)):
        for j in range(i,len_train):
            train_kernel[i][j] = abs(np.vdot(quantum_x_train[i],quantum_x_train[j])) ** 2
            train_kernel[j][i] = train_kernel[i][j]

    clf.fit(train_kernel, labels_train)
    len_test = len(quantum_x_test)
    
    test_kernel = np.zeros((len_test, len_train))
    for i in tqdm(range(len_test)):
        for j in range(len_train):
            test_kernel[i][j] = abs(np.vdot(quantum_x_test[i],quantum_x_train[j])) ** 2
            
    pred = clf.predict(test_kernel)
    accuracy = (pred == labels_test).mean()
    print(f"Test Accuracy: ", accuracy)
    print("preds example", pred[:100])
    print("real example", labels_test[:100])
    
    # Append the new data and accuracy to the dataset
    dataset_to_save = dataset_to_save.append({"dataset": dataset, "accuracy": accuracy}, ignore_index=True)
    folder_path = "/home/leonardo/Research/quantum_MNIST/leo_dev/final_results"
    dataset_to_save.to_csv(os.path.join(folder_path, "results_states_1v1.csv"), index=False)