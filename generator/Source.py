import numpy as np
from qulacs import QuantumState

from typing import Any, Dict, Tuple

import numpy as np
from numpy.typing import NDArray
import pickle
from AQCE_from_program import AQCE_program


def _change_one_hot_label(X: NDArray[np.uint8]) -> NDArray[np.uint8]:
    T: NDArray[np.uint8] = np.zeros((X.size, 10), np.uint8)
    for idx, row in enumerate(T):
        row[X[idx]] = 1
    return T


def load_mnist(
    pickle_file_name: str,
    normalize: bool = True,
    flatten: bool = True,
    one_hot_label: bool = False,
) -> Tuple[NDArray[np.uint8], NDArray[np.uint8]]:
    save_file = pickle_file_name

    with open(save_file, "rb") as f:
        dataset = pickle.load(f)

    if normalize:
        dataset["train_img"] = dataset["train_img"].astype(np.float32)
        dataset["train_img"] /= 255.0

    if one_hot_label:
        dataset["train_label"] = _change_one_hot_label(dataset["train_label"])

    if not flatten:
        dataset["train_img"] = dataset["train_img"].reshape(-1, 1, 28, 28)

    return (dataset["train_img"], dataset["train_label"])


def convert_to_quantum_state(pict) -> QuantumState:
    qubits = 1
    while (1 << qubits) < len(pict):
        qubits += 1
    paded_pict = np.pad(
        pict, (0, (1 << qubits) - len(pict)), mode="constant", constant_values=0
    )
    state = QuantumState(qubits)
    state.load(paded_pict)
    state.normalize(state.get_squared_norm())
    return state


def generate_dataset(
    pickle_file_name: str,
    start: int,
    end: int,
    parameters: Dict[str, int],
    program_path: str,
) -> Dict[str, Any]:
    train_data = load_mnist(pickle_file_name)
    items: Dict[str, Any] = {"qasm": [],
                             "label": [], "state": [], "fidelity": []}
    for x in range(start, end):
        pict = train_data[0][x]

        items["label"].append(str(train_data[1][x]).encode())

        state = convert_to_quantum_state(pict)
        state_list_float = state.get_vector().tolist()
        state_list_str = [str(x.real) + " " + str(x.imag)
                          for x in state_list_float]
        state_str = "\n".join(state_list_str)
        items["state"].append(state_str.encode())

        qasm, fidelity = AQCE_program(
            state,
            M_0=parameters["M_0"],
            M_delta=parameters["M_delta"],
            M_max=parameters["M_max"],
            N=parameters["N"],
            program_path=program_path,
        )
        items["qasm"].append(qasm)
        items["fidelity"].append(fidelity)

    return items
