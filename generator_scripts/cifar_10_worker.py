import configparser
import sys

import typer

from mnisq.internal.dataset import save_raw_dataset
from mnisq.internal.generator.cifar_10.main import (
    generate_test_dataset,
    generate_train_dataset,
)

app = typer.Typer()


@app.command()
def main(
    start: int = typer.Option(...),
    end: int = typer.Option(...),
    flag: str = typer.Option(...),
    program_path: str = typer.Option(...),
    save_path: str = typer.Option(...),
    m_0: int = typer.Option(...),
    m_delta: int = typer.Option(...),
    m_max: int = typer.Option(...),
    n: int = typer.Option(...),
) -> None:
    if flag == "train":
        items = generate_train_dataset(
            start,
            end,
            {"M_0": m_0, "M_delta": m_delta, "M_max": m_max, "N": n},
            program_path,
        )
    elif flag == "test":
        items = generate_test_dataset(
            start,
            end,
            {"M_0": m_0, "M_delta": m_delta, "M_max": m_max, "N": n},
            program_path,
        )
    else:
        raise RuntimeError("Wrong flag specified.")
    save_raw_dataset(items, save_path)
    return


if __name__ == "__main__":
    app()
