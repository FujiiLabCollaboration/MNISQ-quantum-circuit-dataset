from typing import Any, Dict, Tuple

import numpy as np
from qulacs import QuantumCircuit, QuantumState
from qulacs.converter import convert_qulacs_circuit_to_QASM
from qulacs.state import inner_product

from mnisq.internal.generator.aqce import AQCE_program, AQCE_python
from mnisq.internal.generator.cifar_10.downloader import (
    load_test,
    load_train,
)
from mnisq.internal.generator.cifar_10.gray_scale import (
    decomposite_to_RGB,
    to_grayscale,
)


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


def get_circuit_representation(
    pict: np.ndarray, parameters: Dict[str, int], program_path: str
) -> QuantumCircuit:
    state = convert_to_quantum_state(pict)
    if program_path == "":
        C = AQCE_python(
            state,
            M_0=parameters["M_0"],
            M_delta=parameters["M_delta"],
            M_max=parameters["M_max"],
            N=parameters["N"],
        )
    else:
        C = AQCE_program(
            state,
            M_0=parameters["M_0"],
            M_delta=parameters["M_delta"],
            M_max=parameters["M_max"],
            N=parameters["N"],
            program_path=program_path,
        )

    circuit = QuantumCircuit(state.get_qubit_count())
    for x in C:
        circuit.add_gate(x)
    return circuit


def generator(
    data: Dict[bytes, Any],
    start: int,
    end: int,
    parameters: Dict[str, int],
    program_path: str,
) -> Dict[str, Any]:
    items: Dict[str, Any] = {"qasm": [], "label": [], "state": [], "fidelity": []}
    for x in range(start, end):
        pict = np.ravel(to_grayscale(decomposite_to_RGB(data[b"data"][x])))

        label = data[b"labels"][x]

        items["label"].append(label)

        state = convert_to_quantum_state(pict)
        state_list_float = state.get_vector().tolist()
        state_list_str = [str(x.real) + " " + str(x.imag) for x in state_list_float]
        state_str = "\n".join(state_list_str)
        items["state"].append(state_str.encode())

        circuit = get_circuit_representation(pict, parameters, program_path)
        circuit_str = "\n".join(convert_qulacs_circuit_to_QASM(circuit))
        items["qasm"].append(circuit_str.encode())

        circuit_state = QuantumState(10)
        circuit.update_quantum_state(circuit_state)
        items["fidelity"].append(str(inner_product(state, circuit_state).real).encode())
    return items


def generate_train_dataset(
    start: int, end: int, parameters: Dict[str, int], program_path: str = ""
) -> Dict[str, Any]:
    return generator(load_train(), start, end, parameters, program_path)


def generate_test_dataset(
    start: int, end: int, parameters: Dict[str, int], program_path: str = ""
) -> Dict[str, Any]:
    return generator(load_test(), start, end, parameters, program_path)
