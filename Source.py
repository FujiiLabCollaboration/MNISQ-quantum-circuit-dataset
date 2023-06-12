import logging

from mnisq.internal.dataset.dataset import (
    load_raw_dataset,
    save_raw_dataset,
)
from mnisq.mnist.loader import _load_from_path

logging.basicConfig(level=logging.INFO)
hoge = _load_from_path("mnist_1")

print(hoge)
