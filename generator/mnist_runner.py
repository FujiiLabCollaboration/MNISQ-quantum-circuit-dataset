from typing import List
import typer
from pbspro import qsub

app = typer.Typer()

target_datatype: list[str] = [
    "mnist_784",
    "Fashion-MNIST",
    "Kuzushiji-MNIST",
    ]

data_for = [
    {
        "type": "train",
        "prefix": "data_augmented",
        "size": 480000,
        #"size": 4,
    },
    {
        "type": "test",
        "prefix": "data_test",
        "size": 10000,
        #"size": 2,
    }
]

# data_for = [
#     {
#         "type": "train_orig",
#         "prefix": "data",
#         "size": 60000,
#     },
# ]

parameters = [
    {
        "name": "f80",
        "M_0": 6,
        "M_delta": 3,
        "M_max": 25,
        "N": 10,
    },
    {
        "name": "f90",
        "M_0": 12,
        "M_delta": 6,
        "M_max": 50,
        "N": 10,
    },
    {
        "name": "f95",
        "M_0": 24,
        "M_delta": 12,
        "M_max": 100,
        "N": 10,
    },
]

def mnist_run(save_base_path: str, parallel: int) -> List[str]:
    print("Submitting the job for executing dataset creation ...")
    execute_dataset_creation = []
    for td in target_datatype:
        for df in data_for:
            for param in parameters:
                for p in range(1, parallel+1):
                    script = f"singularity run mnist.sif poetry run python generator/mnist_worker.py --start={int(df['size'] * (p - 1) / parallel)} --end={int(df['size'] * p / parallel)} "
                    script += f" --program-path=AQCE.out --save-path={save_base_path}/{df['type']}_{td}_{param['name']} --datatypes={td} "
                    script += f" --m-0={param['M_0']} --m-delta={param['M_delta']} --m-max={param['M_max']} --n={param['N']}"
                    script += f" --pickle-file-name={df['prefix']}_{td}.pkl"
                    execute_dataset_creation.append(
                        qsub(
                            f"aqce-{td}-{param['name']}-p{'{:0>4}'.format(p)}", script)
                    )
    print(f"Done. ID = {execute_dataset_creation}")
    return execute_dataset_creation

@app.command()
def main(
    save_base_path: str = typer.Option(...),
    parallel: int = typer.Option(...),
) -> None:
    mnist_run(save_base_path, parallel)

if __name__ == "__main__":
    app()
