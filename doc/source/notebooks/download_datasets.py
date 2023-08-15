import requests
import zipfile
import os


import requests
import zipfile
import os
import logging

# Configure logging
logging.basicConfig(filename='YOURPATH/download_log.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# List of dataset parameters (data, type, fidelity)
datasets = [
    {"data": "base_test", "type": "mnist_784", "fidelity": "f80"},
    {"data": "base_train_orig", "type": "mnist_784", "fidelity": "f80"},
    {"data": "base_test", "type": "mnist_784", "fidelity": "f90"},
    {"data": "base_train_orig", "type": "mnist_784", "fidelity": "f90"},
    {"data": "base_test", "type": "mnist_784", "fidelity": "f95"},
    {"data": "base_train_orig", "type": "mnist_784", "fidelity": "f95"},
    
    {"data": "base_test", "type": "Fashion-MNIST", "fidelity": "f80"},
    {"data": "base_train_orig", "type": "Fashion-MNIST", "fidelity": "f80"},
    {"data": "base_test", "type": "Fashion-MNIST", "fidelity": "f90"},
    {"data": "base_train_orig", "type": "Fashion-MNIST", "fidelity": "f90"},
    {"data": "base_test", "type": "Fashion-MNIST", "fidelity": "f95"},
    {"data": "base_train_orig", "type": "Fashion-MNIST", "fidelity": "f95"},
    
    {"data": "base_test", "type": "Kuzushiji-MNIST", "fidelity": "f80"},
    {"data": "base_train_orig", "type": "Kuzushiji-MNIST", "fidelity": "f80"},
    {"data": "base_test", "type": "Kuzushiji-MNIST", "fidelity": "f90"},
    {"data": "base_train_orig", "type": "Kuzushiji-MNIST", "fidelity": "f90"},
    {"data": "base_test", "type": "Kuzushiji-MNIST", "fidelity": "f95"},
    {"data": "base_train_orig", "type": "Kuzushiji-MNIST", "fidelity": "f95"},
    # Add more datasets as needed
]

base_url = "https://qulacs-quantum-datasets.s3.us-west-1.amazonaws.com/"
extract_path = "YOURPATH/data_folder"  # Folder where the extracted files will be stored

# Create the extraction folder if it doesn't exist
if not os.path.exists(extract_path):
    os.makedirs(extract_path)

for dataset in datasets:
    data = dataset["data"]
    data_type = dataset["type"]
    fidelity = dataset["fidelity"]
    
    # Construct the URL
    url = f"{base_url}{data}_{data_type}_{fidelity}.zip"
    
    # Construct the filename
    filename = f"{data}_{data_type}_{fidelity}.zip"
    
    # Download the zip file
    response = requests.get(url)
    with open(filename, "wb") as zip_file:
        zip_file.write(response.content)

    # Extract the downloaded zip file
    with zipfile.ZipFile(filename, "r") as zip_ref:
        zip_ref.extractall(extract_path)

    message = f"Download and extraction of {filename} complete."
    print(message)
    logging.info(message)

    # Remove the downloaded zip file if needed
    os.remove(filename)