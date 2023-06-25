from typing import Any, Dict, List

from qulacs import QuantumState
#from qulacs.converter import convert_QASM_to_qulacs_circuit
from mnisq.internal.generator.mnist_like.qasm_converter import convert_QASM_to_qulacs_circuit

from mnisq.internal.dataset import load_raw_dataset_from_url


def qasm_formatter(qasm: bytes, index: int) -> List[str]:
    # print("idx:", index)
    data = qasm.decode().split("\n")
    for itr in range(len(data)):
        if len(data[itr]) != 0 and data[itr][-1] != ";":
            data[itr] += ";"
    return data


def load_mnist_like_dataset(download_URL: str) -> Dict[str, Any]:
    items = {"circuit": [], "state": [], "qasm": [], "label": [], "fidelity": []}
    raw_items = load_raw_dataset_from_url(download_URL)
    items["qasm"] = [x.decode() for x in raw_items["qasm"]]
    items["circuit"] = [
        convert_QASM_to_qulacs_circuit(qasm_formatter(x, i)) for i, x in enumerate(raw_items["qasm"])
    ]
    items["label"] = [int(x.decode()) for x in raw_items["label"]]
    items["fidelity"] = [float(x.decode()) for x in raw_items["fidelity"]]
    state_list_str = [y.decode().split("\n") for y in raw_items["state"]]
    for x in range(len(state_list_str)):
        state_str = state_list_str[x]
        state_separated = [x.split(" ") for x in state_str]
        state_complex = [complex(float(x[0]), float(x[1])) for x in state_separated]
        state = QuantumState(10)
        state.load(state_complex)
        items["state"].append(state)
    return items
