from typing import Any, Dict

import numpy as np
from qulacs import QuantumCircuit, QuantumState
from qulacs.converter import convert_qulacs_circuit_to_QASM
from qulacs.state import inner_product

from mnisq.internal.generator.aqce import AQCE_program, AQCE_python
from mnisq.internal.generator.mnist_like.downloader import (
    load_mnist,
    mnist_files,
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
    pict: np.ndarray, parameters: Dict[str, int]
) -> QuantumCircuit:
    state = convert_to_quantum_state(pict)
    C = AQCE_python(
        state,
        M_0=parameters["M_0"],
        M_delta=parameters["M_delta"],
        M_max=parameters["M_max"],
        N=parameters["N"],
    )
    circuit = QuantumCircuit(state.get_qubit_count())
    for x in C:
        circuit.add_gate(x)
    return circuit


def generate_dataset(
    files: mnist_files,
    start: int,
    end: int,
    parameters: Dict[str, int],
    program_path: str = "",
) -> Dict[str, Any]:
    if program_path == "":
        return generate_dataset_python(files, start, end, parameters)
    return generate_dataset_program(files, start, end, parameters, program_path)


def generate_dataset_python(
    files: mnist_files, start: int, end: int, parameters: Dict[str, int]
) -> Dict[str, Any]:
    train_data, _ = load_mnist(files)
    items: Dict[str, Any] = {"qasm": [], "label": [], "state": [], "fidelity": []}
    for x in range(start, end):
        pict = train_data[0][x]

        items["label"].append(str(train_data[1][x]).encode())

        state = convert_to_quantum_state(pict)
        state_list_float = state.get_vector().tolist()
        state_list_str = [str(x.real) + " " + str(x.imag) for x in state_list_float]
        state_str = "\n".join(state_list_str)
        items["state"].append(state_str.encode())

        circuit = get_circuit_representation(pict, parameters)
        circuit_str = "\n".join(convert_qulacs_circuit_to_QASM(circuit))
        items["qasm"].append(circuit_str.encode())

        circuit_state = QuantumState(10)
        circuit.update_quantum_state(circuit_state)
        items["fidelity"].append(str(inner_product(state, circuit_state).real).encode())
    return items


def generate_dataset_program(
    files: mnist_files,
    start: int,
    end: int,
    parameters: Dict[str, int],
    program_path: str,
) -> Dict[str, Any]:
    train_data = load_mnist(files)
    items: Dict[str, Any] = {"qasm": [], "label": [], "state": [], "fidelity": []}
    for x in range(start, end):
        pict = train_data[0][x]

        items["label"].append(str(train_data[1][x]).encode())

        state = convert_to_quantum_state(pict)
        state_list_float = state.get_vector().tolist()
        state_list_str = [str(x.real) + " " + str(x.imag) for x in state_list_float]
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
