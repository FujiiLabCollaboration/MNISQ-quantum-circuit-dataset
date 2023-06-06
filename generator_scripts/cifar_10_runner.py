from typing import List

from .pbspro import qsub

parameters = [
    {
        "name": "f80",
        "M_0": 6,
        "M_delta": 3,
        "M_max": 25,
        "N": 10,
    },
    {"name": "f90", "M_0": 12, "M_delta": 6, "M_max": 50, "N": 10},
    {"name": "f95", "M_0": 24, "M_delta": 12, "M_max": 100, "N": 10},
]


def cifar_10_run(dep: List[str]) -> List[str]:
    print("Submitting the job for downloading dataset ...")
    download_dataset = []
    download_dataset.append(
        qsub(
            "download-cifar-10-dataset",
            "singularity run mnist.sif poetry run python cifar_10_worker.py --start=1 --end=2 --program-path=./AQCE.out"
            + "--save-path=./data/cifar_10_testrun --m-0=1 --m-delta=2 --m-max=3 --n=4 --flag=test",
            1,
            16,
            dep,
        )
    )
    print(f"Done. ID = {download_dataset}")

    print("Submitting the job for executing dataset creation ...")
    execute_dataset_creation = []
    for y in parameters:

        # train.
        script = (
            "singularity run mnist.sif poetry run python cifar_10_worker.py --flag=train "
            + "--start=$(( 500 * ($PBS_ARRAY_INDEX - 1) / 100)) --end=$(( 500 * $PBS_ARRAY_INDEX / 100)) "
            + f" --program-path=./AQCE.out --save-path=./data/cifar_10_small_{y['name']}_train_$PBS_ARRAY_INDEX "
            + f" --m-0={y['M_0']} --m-delta={y['M_delta']} --m-max={y['M_max']} --n={y['N']}"
        )
        execute_dataset_creation.append(
            qsub(
                f"run-aqce-for-cifar-10-small-{y['name']}-train",
                script,
                100,
                16,
                download_dataset,
            )
        )

        # test.
        script = (
            "singularity run mnist.sif poetry run python cifar_10_worker.py --flag=test "
            + "--start=$(( 100 * ($PBS_ARRAY_INDEX - 1) / 100)) --end=$(( 100 * $PBS_ARRAY_INDEX / 100)) "
            + f" --program-path=./AQCE.out --save-path=./data/cifar_10_small_{y['name']}_test_$PBS_ARRAY_INDEX "
            + f" --m-0={y['M_0']} --m-delta={y['M_delta']} --m-max={y['M_max']} --n={y['N']}"
        )
        execute_dataset_creation.append(
            qsub(
                f"run-aqce-for-cifar-10-small-{y['name']}-test",
                script,
                100,
                16,
                download_dataset,
            )
        )

    print(f"Done. ID = {execute_dataset_creation}")

    print("Submitting the job for merge previous dataset creation result ...")
    merge_job = []
    for y in parameters:
        script = f"singularity run mnist.sif poetry run python merge.py cifar_10_small_{y['name']}_train 100"
        merge_job.append(
            qsub(
                f"merge-dataset-cifar-10-small-{y['name']}-train",
                script,
                1,
                96,
                execute_dataset_creation,
            )
        )
        script = f"singularity run mnist.sif poetry run python merge.py cifar_10_small_{y['name']}_test 100"
        merge_job.append(
            qsub(
                f"merge-dataset-cifar-10-small-{y['name']}-train",
                script,
                1,
                96,
                execute_dataset_creation,
            )
        )
    print(f"Done. ID = {merge_job}")
    return merge_job
