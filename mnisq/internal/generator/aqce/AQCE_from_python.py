#%%
import math

import numpy as np
from qulacs import QuantumState
from qulacs.gate import DenseMatrix, Identity, X, Y, Z
from qulacs.state import inner_product

Pauli_matrix = [
    np.array([[1, 0], [0, 1]], dtype=complex),
    np.array([[0, 1], [1, 0]], dtype=complex),
    np.array(
        [
            [0, -1j],
            [1j, 0],
        ],
        dtype=complex,
    ),
    np.array([[1, 0], [0, -1]], dtype=complex),
]
Pauli_matrix_product = [
    [np.kron(Pauli_matrix[i], Pauli_matrix[j]) for j in range(4)] for i in range(4)
]


def evaluate_F(target_state, Phi_state, Psi_state, idx):
    n_qubits = target_state.get_qubit_count()
    i = idx[0]
    j = idx[1]

    Pauli_i = [Identity(i), X(i), Y(i), Z(i)]
    Pauli_j = [Identity(j), X(j), Y(j), Z(j)]
    Pauli_Psi_state = QuantumState(n_qubits)

    F = np.zeros((4, 4), dtype=complex)
    for k in range(4):
        for l in range(4):
            Pauli_Psi_state.load(Psi_state)
            Pauli_i[k].update_quantum_state(Pauli_Psi_state)
            Pauli_j[l].update_quantum_state(Pauli_Psi_state)
            f_kl = inner_product(Phi_state, Pauli_Psi_state) / 4
            F += f_kl * Pauli_matrix_product[k][l]

    return F


def evaluate_Rho(target_state, Psi_state, idx):
    n_qubits = target_state.get_qubit_count()
    i = idx[0]
    j = idx[1]

    Pauli_i = [Identity(i), X(i), Y(i), Z(i)]
    Pauli_j = [Identity(j), X(j), Y(j), Z(j)]
    Pauli_Psi_state = QuantumState(n_qubits)

    Rho = np.zeros((4, 4), dtype=complex)
    for k in range(4):
        for l in range(4):
            Pauli_Psi_state.load(Psi_state)
            Pauli_i[k].update_quantum_state(Pauli_Psi_state)
            Pauli_j[l].update_quantum_state(Pauli_Psi_state)
            rho_kl = inner_product(Psi_state, Pauli_Psi_state) / 4
            Rho += rho_kl * Pauli_matrix_product[k][l]

    return Rho


def AQCE_python(target_state, M_0, M_delta, M_max, N):
    n_qubits = target_state.get_qubit_count()
    I_gate = DenseMatrix(0, [[1, 0], [0, 1]])
    C = [I_gate for i in range(M_0)]
    C_inv = [I_gate for i in range(M_0)]
    M = M_0
    Psi_state = QuantumState(n_qubits)
    Phi_state = QuantumState(n_qubits)

    while M < M_max:
        for add_couont in range(M_delta):
            max = -1
            idx = (-1, -1)

            Psi_state.load(target_state)
            for k in reversed(range(M)):
                C_inv[k].update_quantum_state(Psi_state)

            for i in range(n_qubits):
                for j in range(i + 1, n_qubits):
                    Rho = evaluate_Rho(target_state, Psi_state, (i, j))
                    eigenvalue = np.linalg.eigvalsh(Rho)
                    if eigenvalue[-1] > max:
                        max = eigenvalue[-1]
                        idx = (i, j)
                        max_Rho = Rho

            eigenvalue, eigenvec = np.linalg.eigh(max_Rho)
            V = np.fliplr(eigenvec)
            C.insert(0, DenseMatrix([idx[1], idx[0]], V))
            C_inv.insert(0, DenseMatrix([idx[1], idx[0]], np.conjugate(V.T)))
            M += 1

        for sweep_count in range(N):
            for m in range(M):
                max = -1
                idx = (-1, -1)

                Phi_state.set_zero_state()
                for k in range(m):
                    C[k].update_quantum_state(Phi_state)

                Psi_state.load(target_state)
                for k in reversed(range(m + 1, M)):
                    C_inv[k].update_quantum_state(Psi_state)

                for i in range(n_qubits):
                    for j in range(i + 1, n_qubits):
                        F = evaluate_F(target_state, Phi_state, Psi_state, (i, j))
                        D = np.linalg.svd(F, compute_uv=False)
                        if sum(D) > max:
                            max = sum(D)
                            idx = (i, j)
                            max_F = F

                X, D, Y = np.linalg.svd(max_F, full_matrices=True)
                U = X @ Y
                C[m] = DenseMatrix([idx[1], idx[0]], U)
                C_inv[m] = DenseMatrix([idx[1], idx[0]], np.conjugate(U.T))

    return C


def get_cost(target_state, C):
    n_qubits = target_state.get_qubit_count()
    state = QuantumState(n_qubits)
    for k in range(len(C)):
        C[k].update_quantum_state(state)
    f = inner_product(state, target_state)
    # return abs(f)
    return 1 - math.pow(abs(f), 1 / n_qubits)


def get_state(n_qubits, C):
    state = QuantumState(n_qubits)
    for k in range(len(C)):
        C[k].update_quantum_state(state)
    return state
