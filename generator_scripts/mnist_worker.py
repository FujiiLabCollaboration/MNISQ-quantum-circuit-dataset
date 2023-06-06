import configparser
import sys

import typer

from qulacs_dataset.internal.dataset import save_raw_dataset
from qulacs_dataset.internal.generator.mnist_like.downloader import mnist_files
from qulacs_dataset.internal.generator.mnist_like.Source import (
    generate_dataset,
)

app = typer.Typer()


@app.command()
def main(
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
    target_file_info = config[datatypes]

    target_files = mnist_files(
        mnist_files.external_file(
            target_file_info["train_img_url"], target_file_info["train_img_name"]
        ),
        mnist_files.external_file(
            target_file_info["train_label_url"], target_file_info["train_label_name"]
        ),
        target_file_info["pickle_name"],
    )

    items = generate_dataset(
        target_files,
        start,
        end,
        {"M_0": m_0, "M_delta": m_delta, "M_max": m_max, "N": n},
        program_path,
    )
    save_raw_dataset(items, save_path)
    return


if __name__ == "__main__":
    app()
