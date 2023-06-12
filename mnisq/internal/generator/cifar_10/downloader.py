import io
import os
import pickle
import tarfile
from typing import Any, Dict, List

import numpy as np
import requests

dataset_dir = os.path.dirname(os.path.abspath(__file__)) + "/cache"
download_url = "https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz"


def download_zip() -> None:
    if os.path.exists(dataset_dir + "/cifar-10-batches-py"):
        # already downloaded.
        return

    urlData = requests.get(download_url).content
    data_obj = io.BytesIO(urlData)
    tar = tarfile.open(fileobj=data_obj, mode="r")
    os.makedirs(dataset_dir + "/cifar-10-batches-py")
    for member in tar.getmembers():
        f = tar.extractfile(member)
        if f is not None:
            with open(os.path.join(dataset_dir, member.name), "wb") as w:
                w.write(f.read())


def merge(a: Dict[bytes, Any], b: Dict[bytes, Any]) -> Dict[bytes, Any]:
    keys = [b"labels", b"data"]
    result: Dict[bytes, Any] = {}
    for x in keys:
        if isinstance(a[x], np.ndarray):
            result[x] = np.concatenate([a[x], b[x]])
        else:
            result[x] = a[x] + b[x]
    return result


def load_train() -> Dict[bytes, Any]:
    download_zip()
    filename = [
        dataset_dir + "/cifar-10-batches-py/data_batch_1",
        dataset_dir + "/cifar-10-batches-py/data_batch_2",
        dataset_dir + "/cifar-10-batches-py/data_batch_3",
        dataset_dir + "/cifar-10-batches-py/data_batch_4",
        dataset_dir + "/cifar-10-batches-py/data_batch_5",
    ]

    result: Dict[bytes, Any] = {}
    with open(filename[0], "rb") as fo:
        result = pickle.load(fo, encoding="bytes")
    for i in range(1, len(filename)):
        with open(filename[i], "rb") as fo:
            dict = pickle.load(fo, encoding="bytes")
            result = merge(result, dict)

    return result


def load_test() -> Dict[bytes, Any]:
    download_zip()
    filename = dataset_dir + "/cifar-10-batches-py/test_batch"
    with open(filename, "rb") as fo:
        return pickle.load(fo, encoding="bytes")
