from typing import Any, Dict

from mnisq.config import download_URL as URL
from mnisq.internal.loader.mnist_like import load_mnist_like_dataset


def load_mnist_original_f80() -> Dict[str, Any]:
    return load_mnist_like_dataset(URL + "/train_orig_mnist_784_f80.zip")


def load_mnist_original_f90() -> Dict[str, Any]:
    return load_mnist_like_dataset(URL + "/train_orig_mnist_784_f90.zip")


def load_mnist_original_f95() -> Dict[str, Any]:
    return load_mnist_like_dataset(URL + "/train_orig_mnist_784_f95.zip")


def load_mnist_test_f80() -> Dict[str, Any]:
    return load_mnist_like_dataset(URL + "/test_mnist_784_f80.zip")


def load_mnist_test_f90() -> Dict[str, Any]:
    return load_mnist_like_dataset(URL + "/test_mnist_784_f90.zip")


def load_mnist_test_f95() -> Dict[str, Any]:
    return load_mnist_like_dataset(URL + "/test_mnist_784_f95.zip")


def load_mnist_train_f80() -> Dict[str, Any]:
    return load_mnist_like_dataset(URL + "/train_mnist_784_f80.zip")


def load_mnist_train_f90() -> Dict[str, Any]:
    return load_mnist_like_dataset(URL + "/train_mnist_784_f90.zip")


def load_mnist_train_f95() -> Dict[str, Any]:
    return load_mnist_like_dataset(URL + "/train_mnist_784_f95.zip")
