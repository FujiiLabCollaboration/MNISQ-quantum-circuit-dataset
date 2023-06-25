#import cirq
import qiskit
from qiskit.circuit.library.standard_gates import *
from qiskit.extensions import UnitaryGate
import numpy as np
#from qulacs import QuantumCircuit
from scipy import linalg

def normalize(arr, axis=0):
    norm = linalg.norm(arr, axis=axis)
    return arr / norm

def qulacs_gates_to_qiskit(circ_qulacs):
    nqubits = circ_qulacs.get_qubit_count()
    qiskit_circuit = qiskit.QuantumCircuit(nqubits)
    #n = cirq.LineQubit.range(nqubits)
    for i in range (circ_qulacs.get_gate_count()):
        gate = circ_qulacs.get_gate(i)
        gate_type = gate.get_name()
        control = gate.get_control_index_list()
        target = gate.get_target_index_list()
        ###convert indices into the cirq ones###
        # control = [(nqubits - 1) - i for i in control]
        # control.reverse()
        # target = [(nqubits - 1) - i for i in target]
        # target.reverse()
        if gate_type == 'X':
            #qiskit_circuit.append(XGate, control + target, [])
            qiskit_circuit.append(XGate(), control + target, [])
        # elif gate_type == 'Y':
        #     qiskit_circuit.append(YGate(), control + target, [])
        # elif gate_type == 'Z':
        #     qiskit_circuit.append(ZGate(), control + target, [])
        # elif gate_type == 'H':
        #     qiskit_circuit.append(HGate(), control + target, [])
        # elif gate_type == 'S':
        #     qiskit_circuit.append(SGate(), control + target, [])
        # elif gate_type == 'T':
        #     qiskit_circuit.append(TGate(), control + target, [])
        # elif gate_type == 'I':
        #     pass
        # elif gate_type == 'CNOT':
        #     qiskit_circuit.append(CXGate(), control + target, [])
        # elif gate_type == 'SWAP':
        #     qiskit_circuit.append(SwapGate(), control + target, [])
        # elif gate_type == 'CZ':
        #     qiskit_circuit.append(CZGate(), control + target, [])
        # elif gate_type == 'ParametricRX':
        #     angle = gate.get_parameter_value()
        #     cirq_gates.append(cirq.Rx(rads = -1 * angle).on(n[target[0]]))
        # elif gate_type == 'ParametricRY':
        #     angle = gate.get_parameter_value()
        #     cirq_gates.append(cirq.Ry(rads = -1 * angle).on(n[target[0]]))
        # elif gate_type == 'ParametricRZ':
        #     angle = gate.get_parameter_value()
        #     cirq_gates.append(cirq.Rz(rads = -1 * angle).on(n[target[0]]))
        elif gate_type == 'X-rotation':
            #angle = gate.get_angle() * -1
            angle = gate.get_angle()
            qiskit_circuit.append(RXGate(angle), control + target, [])
        elif gate_type == 'Y-rotation':
            #angle = gate.get_angle() * -1
            angle = gate.get_angle()
            qiskit_circuit.append(RYGate(angle), control + target, [])
        elif gate_type == 'Z-rotation':
            #angle = gate.get_angle() * -1
            angle = gate.get_angle()
            qiskit_circuit.append(RZGate(angle), control + target, [])
        elif gate_type == 'DenseMatrix' or gate_type == 'Pauli-rotation':
            # ユニタリー近似
            mat = gate.get_matrix()
            X, _, Y = np.linalg.svd(mat, full_matrices=True)
            I = np.identity(len(mat))
            V = X @ I @ Y
            V = normalize(V)
            qiskit_circuit.append(UnitaryGate(V), control + target, [])
        else:
            print('--------Invalid Gate--------')
            print(gate_type)
            print('----------------------------')
    return qiskit_circuit
