import os
import configparser

import typer
from typing import Any, Dict, List, Union

from logging import getLogger
import tqdm

from Source import (
    generate_dataset,
)

app = typer.Typer()
logger = getLogger(__name__)


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


def save_raw_dataset(items: Union[List[bytes], Dict[str, Any]], save_dir: str, start_pos: int) -> None:
    logger.info(f"Creating directory {save_dir} ...")
    os.makedirs(save_dir, exist_ok=True)

    if type(items) is list:
        logger.info(f"Saving data to directory {save_dir} ...")
        for itr in tqdm.tqdm(range(len(items))):
            filename = str(start_pos + itr)
            with open(_safe_path_join(save_dir, filename), "wb") as f:
                f.write(bytes(items[itr]))
        logger.info("Save complete.")
    elif type(items) is dict:
        for key, value in items.items():
            next_directory = _safe_path_join(save_dir, str(key))
            save_raw_dataset(value, next_directory, start_pos)
    else:
        raise RuntimeError(
            f"Expected List[Any] or Dict[Any,Any], but was unknown type: {type(items)}"
        )
    return


@app.command()
def main(
    pickle_file_name: str = typer.Option(...),
    start: int = typer.Option(...),
    end: int = typer.Option(...),
    program_path: str = typer.Option(...),
    save_path: str = typer.Option(...),
    datatypes: str = typer.Option(...),
    m_0: int = typer.Option(...),
    m_delta: int = typer.Option(...),
    m_max: int = typer.Option(...),
    n: int = typer.Option(...),
) -> None:
    config = configparser.ConfigParser()
    config.read("config.ini")
    items = generate_dataset(
        pickle_file_name,
        start,
        end,
        {"M_0": m_0, "M_delta": m_delta, "M_max": m_max, "N": n},
        program_path,
    )
    save_raw_dataset(items, save_path, start)
    return


if __name__ == "__main__":
    app()
