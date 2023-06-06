import subprocess
import tempfile
from typing import Tuple

from qulacs import QuantumState


def AQCE_program(
    target_state: QuantumState,
    M_0: int,
    M_delta: int,
    M_max: int,
    N: int,
    program_path: str,
) -> Tuple[bytes, bytes]:
    with tempfile.TemporaryDirectory() as dir:
        state_list_float = target_state.get_vector().tolist()
        state_list_str = [str(x.real) + " " + str(x.imag) for x in state_list_float]
        state_str = "\n".join(state_list_str)

        with open(dir + "/state.txt", "wb") as f:
            f.write(state_str.encode())

        return_code = subprocess.call(
            f'{program_path} {dir + "/state.txt"} {dir + "/qasm.txt"} {dir + "/fidelity.txt"} {parameters["M_0"]} {parameters["M_delta"]} {parameters["N"]} {parameters["M_max"]}',
            shell=True,
        )
        if return_code != 0:
            raise RuntimeError(
                f"Something happened during AQCE program. Return code is {return_code}"
            )

        with open(dir + "/qasm.txt", "rb") as f:
            qasm = f.read()
        with open(dir + "/fidelity.txt", "rb") as f:
            fidelity = f.read()
        return (qasm, fidelity)
