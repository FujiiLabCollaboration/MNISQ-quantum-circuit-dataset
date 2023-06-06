from typing import List

from .pbspro import qsub

target_datatype: list[str] = ["mnist", "kuzushiji_mnist", "fashion_mnist"]
parameters = [
    {
        "name": "small_f80",
        "M_0": 6,
        "M_delta": 3,
        "M_max": 25,
        "N": 10,
        "Size": 600,
    },
    {
        "name": "small_f90",
        "M_0": 12,
        "M_delta": 6,
        "M_max": 50,
        "N": 10,
        "Size": 600,
    },
    {
        "name": "small_f95",
        "M_0": 24,
        "M_delta": 12,
        "M_max": 100,
        "N": 10,
        "Size": 600,
    },
    {"name": "large_f80", "M_0": 6, "M_delta": 3, "M_max": 25, "N": 10, "Size": 60000},
    {
        "name": "large_f90",
        "M_0": 12,
        "M_delta": 6,
        "M_max": 50,
        "N": 10,
        "Size": 60000,
    },
    {
        "name": "large_f95",
        "M_0": 24,
        "M_delta": 12,
        "M_max": 100,
        "N": 10,
        "Size": 60000,
    },
]


def mnist_run(dep: List[str]) -> List[str]:
    print("Submitting the job for downloading dataset ...")
    download_dataset = []
    for x in target_datatype:
        download_dataset.append(
            qsub(
                f"download-{x}-dataset",
                f"singularity run mnist.sif poetry run python mnist.py --start=1 --end=2 --program-path=./AQCE.out --save-path=./data/{x}_testrun --datatypes={x} --m-0=1 --m-delta=2 --m-max=3 --n=4",
                1,
                16,
                dep,
            )
        )
    print(f"Done. ID = {download_dataset}")

    print("Submitting the job for executing dataset creation ...")
    execute_dataset_creation = []
    for x in target_datatype:
        for y in parameters:
            script = f"singularity run mnist.sif poetry run python mnist_worker.py --start=$(( {y['Size']} * ($PBS_ARRAY_INDEX - 1) / 100)) --end=$(( {y['Size']} * $PBS_ARRAY_INDEX / 100)) "
            script += f" --program-path=./AQCE.out --save-path=./data/{x}_{y['name']}_$PBS_ARRAY_INDEX --datatypes={x} "
            script += f" --m-0={y['M_0']} --m-delta={y['M_delta']} --m-max={y['M_max']} --n={y['N']}"
            execute_dataset_creation.append(
                qsub(f"run-aqce-for-{x}-{y['name']}", script, 100, 16, download_dataset)
            )
    print(f"Done. ID = {execute_dataset_creation}")

    print("Submitting the job for merge previous dataset creation result ...")
    merge_job = []
    for x in target_datatype:
        for y in parameters:
            script = f"singularity run mnist.sif poetry run python merge.py {x}_{y['name']} 100"
            merge_job.append(
                qsub(
                    f"merge-dataset-{x}-{y['name']}",
                    script,
                    1,
                    96,
                    execute_dataset_creation,
                )
            )
    print(f"Done. ID = {merge_job}")
    return merge_job
