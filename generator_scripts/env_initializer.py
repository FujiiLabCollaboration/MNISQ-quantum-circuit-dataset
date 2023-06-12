import os
from typing import List

from .pbspro import qsub


def env_initialize(dep: List[str]) -> List[str]:
    print("Creating directory...")
    os.makedirs("outcome", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    print("Done.")

    print("Submitting the job for initialization of python ...")
    initialize_python: List[str] = [
        qsub(
            "initialize_python",
            "singularity run mnist.sif g++ ../mnisq/internal/generator/aqce/AQCE.cpp -o ./AQCE.out -lcppsim_static -lcsim_static -lvqcsim_static -fopenmp && singularity run mnist.sif poetry install",
            1,
            96,
            dep,
        )
    ]
    print(f"Done. ID = {initialize_python}")
    return initialize_python
