import logging

from qulacs_dataset.internal.dataset.dataset import (
    load_raw_dataset,
    save_raw_dataset,
)
from qulacs_dataset.mnist.loader import _load_from_path

logging.basicConfig(level=logging.INFO)
hoge = _load_from_path("mnist_1")

print(hoge)
