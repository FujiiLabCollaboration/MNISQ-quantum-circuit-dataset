import os
import subprocess
from typing import List


def qsub(
    name: str, command: str, parallel: int, cpus: int = 16, dependency: List[str] = []
) -> str:
    os.makedirs("workspace", exist_ok=True)
    with open(f"workspace/{name}.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("cd $PBS_O_WORKDIR\n")
        f.write(command)
    qsub_command = f"qsub -N {name} -l select=1:ncpus={cpus} -o workspace -e workspace "
    if parallel != 1:
        qsub_command += f" -J 1-{parallel} "
    if len(dependency) != 0:
        qsub_command += "-W depend=afterany"
        for x in dependency:
            qsub_command += f":{x}"
        qsub_command += " "
    qsub_command += f" workspace/{name}.sh"
    result = subprocess.check_output(
        qsub_command,
        shell=True,
    )
    # result should be like 12345[].{clustername}
    job_id = result.decode().split(".")[0]
    return job_id


def qdel(job_id: str) -> None:
    subprocess.run(f"qdel {job_id}", shell=True)
