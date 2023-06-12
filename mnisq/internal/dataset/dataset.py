import os
import re
from logging import getLogger
from typing import Any, Dict, List, Union

import requests
import tqdm

logger = getLogger(__name__)


def load_raw_dataset_from_url(
    url: str, cache_dir: str = "mnisq_cache"
) -> Union[List[bytes], Dict[str, Any]]:
    zip_path = _download_dataset(url, cache_dir)
    dataset_path = _unzip_dataset(zip_path, cache_dir)
    return load_raw_dataset(dataset_path)


def load_raw_dataset(dataset_dir: str) -> Union[List[bytes], Dict[str, Any]]:
    dataset_dir = os.path.abspath(dataset_dir)
    directory_info = os.scandir(dataset_dir)
    list_type = 0
    dict_type = 0
    for entry in directory_info:
        if entry.is_file():
            list_type = 1
        else:
            dict_type = 1

    if dict_type == 1 and list_type == 1:
        logger.warning(f"directory {dataset_dir} contains both directory and file.")

    if dict_type == 1:
        logger.info(f"Loading directory {dataset_dir} ...")
        directory_info = os.scandir(dataset_dir)
        result_dict: Dict[str, Any] = {}
        for key in directory_info:
            result_dict[key.name] = load_raw_dataset(key.path)
        return result_dict

    if list_type == 1:
        logger.info(f"Loading items from directory {dataset_dir} ...")
        directory_info = os.scandir(dataset_dir)
        filelist: List[str] = []
        for x in directory_info:
            filelist.append(str(x.path))
        filelist = _numerical_sorted(filelist)
        result_list: List[bytes] = []
        for itr in tqdm.tqdm(range(len(filelist))):
            key_name = os.path.abspath(filelist[itr])
            with open(key_name, "rb") as f:
                result_list.append(f.read())
        return result_list

    raise RuntimeError("Directory {dataset_dir} does not contain informations.")


def save_raw_dataset(items: Union[List[bytes], Dict[str, Any]], save_dir: str) -> None:
    logger.info(f"Creating directory {save_dir} ...")
    os.makedirs(save_dir, exist_ok=True)

    if type(items) is list:
        logger.info(f"Saving data to directory {save_dir} ...")
        for itr in tqdm.tqdm(range(len(items))):
            filename = str(itr)
            with open(_safe_path_join(save_dir, filename), "wb") as f:
                f.write(bytes(items[itr]))
        logger.info("Save complete.")
    elif type(items) is dict:
        for key, value in items.items():
            next_directory = _safe_path_join(save_dir, str(key))
            save_raw_dataset(value, next_directory)
    else:
        raise RuntimeError(
            f"Expected List[Any] or Dict[Any,Any], but was unknown type: {type(items)}"
        )
    return


def merge_dataset(
    a: Union[List[bytes], Dict[str, Any]], b: Union[List[bytes], Dict[str, Any]]
) -> Union[List[bytes], Dict[str, Any]]:
    if type(a) is list:
        if type(b) is not list:
            raise RuntimeError("structure of dataset does not match")
        result_l: List[bytes] = []
        for x in a:
            result_l.append(x)
        for x in b:
            result_l.append(x)
        return result_l
    elif type(a) is dict:
        if type(b) is not dict:
            raise RuntimeError("structure of dataset does not match")
        result_d: Dict[str, Any] = {}
        for key, _ in a.items():
            result_d[key] = merge_dataset(a[key], b[key])
        return result_d
    else:
        raise RuntimeError(f"Invalid type: {type(a)}")


def _unzip_dataset(zip_path: str, cache_dir: str) -> str:
    logger.info(f"unzip dataset {zip_path} ...")
    import shutil

    shutil.unpack_archive(zip_path, cache_dir)
    return _safe_path_join(cache_dir, zip_path[:-4])


def _download_dataset(url: str, cache_dir: str) -> str:
    filename = os.path.basename(url).split("?")[0]
    path = _safe_path_join(cache_dir, filename)
    if os.path.exists(path) is False:
        logger.info(f"downloading file from {url} ...")
        r = requests.get(url)
        data = r.content

        os.makedirs(cache_dir, exist_ok=True)
        with open(path, "wb") as f:
            f.write(data)
    else:
        logger.info(f"Using cache from {url}")

    return path


def _safe_path_join(faith_path: str, suspicious_path: str) -> str:
    faith_path = os.path.realpath(faith_path)
    suspicious_merged_path = os.path.join(faith_path, suspicious_path)

    common_path: str = os.path.commonpath([faith_path, suspicious_merged_path])
    if common_path != faith_path:
        raise RuntimeError(
            "Directory Traversal was detected on path "
            + f"{suspicious_merged_path} \n"
            + "This dataset may contain malicious items."
        )
    return suspicious_merged_path


def _numerical_sorted(inputs: List[str]) -> List[str]:
    def alphanum_key(s: str) -> List[Union[int, str]]:
        return [int(c) if c.isdecimal() else c for c in re.split("([0-9]+)", s)]

    return sorted(inputs, key=alphanum_key)
