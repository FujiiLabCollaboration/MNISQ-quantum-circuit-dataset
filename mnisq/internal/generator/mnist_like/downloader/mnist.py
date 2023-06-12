# This source code is from book "ゼロから作る Deep Learning".
# Adjusted for mnisq usage by kotamanegi.
# Original source code: https://github.com/oreilly-japan/deep-learning-from-scratch/blob/master/dataset/mnist.py

import gzip
import os
import os.path
import pickle
import urllib.request
from dataclasses import dataclass
from logging import getLogger
from typing import Dict, Tuple

import numpy as np
from numpy.typing import NDArray

logger = getLogger(__name__)


@dataclass
class mnist_files:
    @dataclass
    class external_file:
        url: str
        file_name: str

    train_img: external_file
    train_label: external_file
    pickle_file_name: str


dataset_dir = os.path.dirname(os.path.abspath(__file__))

train_num = 60000
img_dim = (1, 28, 28)
img_size = 784


def _download(file: mnist_files.external_file) -> None:
    file_path = dataset_dir + "/" + file.file_name

    if os.path.exists(file_path):
        return

    logger.info(f"Downloading {file.file_name} from {file.url} ... ")
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"
    }
    request = urllib.request.Request(file.url, headers=headers)
    response = urllib.request.urlopen(request).read()
    with open(file_path, mode="wb") as f:
        f.write(response)
    logger.info("Done")


def download_mnist(files: mnist_files) -> None:
    _download(files.train_img)
    _download(files.train_label)


def _load_label(file: mnist_files.external_file) -> NDArray[np.uint8]:
    file_path = dataset_dir + "/" + file.file_name

    logger.info(f"Converting {file.file_name} to NumPy Array ...")
    with gzip.open(file_path, "rb") as f:
        labels = np.frombuffer(f.read(), np.uint8, offset=8)
    logger.info("Done")

    return labels


def _load_img(file: mnist_files.external_file) -> NDArray[np.uint8]:
    file_path = dataset_dir + "/" + file.file_name

    logger.info(f"Converting {file.file_name} to NumPy Array ...")
    with gzip.open(file_path, "rb") as f:
        data = np.frombuffer(f.read(), np.uint8, offset=16)
    data = data.reshape(-1, img_size)
    logger.info("Done")

    return data


def _convert_numpy(files: mnist_files) -> Dict[str, NDArray[np.uint8]]:
    dataset = {}
    dataset["train_img"] = _load_img(files.train_img)
    dataset["train_label"] = _load_label(files.train_label)

    return dataset


def init_mnist(files: mnist_files) -> None:
    save_file = dataset_dir + "/" + files.pickle_file_name
    download_mnist(files)
    dataset = _convert_numpy(files)
    logger.info("Creating pickle file ...")
    with open(save_file, "wb") as f:
        pickle.dump(dataset, f, -1)
    logger.info("Done!")


def _change_one_hot_label(X: NDArray[np.uint8]) -> NDArray[np.uint8]:
    T: NDArray[np.uint8] = np.zeros((X.size, 10), np.uint8)
    for idx, row in enumerate(T):
        row[X[idx]] = 1
    return T


def load_mnist(
    files: mnist_files,
    normalize: bool = True,
    flatten: bool = True,
    one_hot_label: bool = False,
) -> Tuple[NDArray[np.uint8], NDArray[np.uint8]]:
    """MNISTデータセットの読み込み
    Parameters
    ----------
    normalize : 画像のピクセル値を0.0~1.0に正規化する
    one_hot_label :
        one_hot_labelがTrueの場合、ラベルはone-hot配列として返す
        one-hot配列とは、たとえば[0,0,1,0,0,0,0,0,0,0]のような配列
    flatten : 画像を一次元配列に平にするかどうか
    Returns
    -------
    (訓練画像, 訓練ラベル), (テスト画像, テストラベル)
    """
    save_file = dataset_dir + "/" + files.pickle_file_name
    if not os.path.exists(save_file):
        init_mnist(files)

    with open(save_file, "rb") as f:
        dataset = pickle.load(f)

    if normalize:
        dataset["train_img"] = dataset["train_img"].astype(np.float32)
        dataset["train_img"] /= 255.0

    if one_hot_label:
        dataset["train_label"] = _change_one_hot_label(dataset["train_label"])

    if not flatten:
        dataset["train_img"] = dataset["train_img"].reshape(-1, 1, 28, 28)

    return (dataset["train_img"], dataset["train_label"])
