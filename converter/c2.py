import numpy as np
import pickle
from math import pi
from qiskit_convert import qulacs_gates_to_qiskit
from qulacs import QuantumState
from os import makedirs
import re
import sys

from qasm_convert import QASM_to_qulacs
from qasm_converter_fixed import convert_QASM_to_qulacs_circuit

from qiskit import QuantumCircuit, Aer, execute

def expand_qasm_macros(src_qasm):
    pi_mul_pattern = re.compile(r'pi\*([+-]?\d+(?:\.\d*)?|.\d+)')
    pi_div_pattern = re.compile(r'pi/([+-]?\d+(?:\.\d*)?|.\d+)')
    mul_pattern_minus = re.compile(r'-\d\*([+-]?\d+(?:\.\d*)?|.\d+)')
    div_pattern_minus = re.compile(r'-\d/([+-]?\d+(?:\.\d*)?|.\d+)')
    mul_pattern = re.compile(r'\d\*([+-]?\d+(?:\.\d*)?|.\d+)')
    div_pattern = re.compile(r'\d/([+-]?\d+(?:\.\d*)?|.\d+)')
    lines = src_qasm.splitlines()
    macros = {}
    res_qasm = ''
    for line in lines:
        if line == "":
            continue
        line = pi_mul_pattern.sub(lambda match : str(pi*float(match.group(1))), line)
        line = pi_div_pattern.sub(lambda match : str(pi/float(match.group(1))), line)
        line = mul_pattern_minus.sub(lambda match : str(eval(match.group(0))), line)
        line = div_pattern_minus.sub(lambda match : str(eval(match.group(0))), line)
        line = mul_pattern.sub(lambda match : str(eval(match.group(0))), line)
        line = div_pattern.sub(lambda match : str(eval(match.group(0))), line)
        #print("line:",line)
        line = line.replace('pi', str(pi))
        words = line.split()
        name = words[0]
        if name == 'gate':
            key = words[1]
            args = words[2].split(',')
            gates = list(map(lambda g:g + ';' , ' '.join(words[4:-1]).split(';')[:-1]))
            macros[key] = (args, gates)
        elif name in macros:
            img_args = words[1][:-1].split(',')
            data = macros[name]
            for gate in data[1]:
                res_line = gate.strip()
                for i in range(len(img_args)):
                    res_line = res_line.replace(data[0][i], img_args[i])
                res_qasm += res_line + '\n'
        else:
            res_qasm += line + '\n'
    return res_qasm


def convert(input_circuit_dir, output_qasm_dir, testcase_id, test_output=False):
    with open(f'%s/circuit_%05d.pickle' % (input_circuit_dir, testcase_id), 'rb') as f:
        circ_qulacs = pickle.load(f)

    standard_circ_qiskit = qulacs_gates_to_qiskit(circ_qulacs)
    standard_circ_qasm = standard_circ_qiskit.qasm()
    final_qasm = expand_qasm_macros(standard_circ_qasm)

    makedirs(output_qasm_dir, exist_ok=True)
    with open('%s/%d' % (output_qasm_dir, testcase_id), 'w') as f:
        f.write(final_qasm)

    if test_output:
        print("test")
        nqubits = circ_qulacs.get_qubit_count()
        state1 = QuantumState(nqubits)
        circ_qulacs.update_quantum_state(state1)
        v1 = state1.get_vector()

        # qubits = [cirq.LineQubit(i) for i in range(nqubits)]
        # simulator = cirq.Simulator()
        # result = simulator.simulate(standard_circ_cirq, qubit_order=qubits)
        # v2 = result.final_state_vector

        # state2 = QuantumState(nqubits)
        # standard_circ_qulacs = QASM_to_qulacs(final_qasm.splitlines())
        # # standard_circ_qulacs = convert_QASM_to_qulacs_circuit(
        # #     final_qasm.splitlines())
        # standard_circ_qulacs.update_quantum_state(state2)
        # v3 = state2.get_vector()
        
        circ_qulacs2 = convert_QASM_to_qulacs_circuit(final_qasm.splitlines())
        state2 = QuantumState(nqubits)
        circ_qulacs2.update_quantum_state(state2)
        v2 = state2.get_vector()

        qc = QuantumCircuit.from_qasm_str(final_qasm)
        backend = Aer.get_backend("statevector_simulator")
        job = execute(qc, backend)
        result = job.result()
        #v3 = result.get_statevector(qc, decimals=3)
        v3 = result.get_statevector(qc)
        # print(state[0])
        # print(result.get_counts())

        for i in range(2**nqubits):
            #assert abs(v1[i] - v2[i]) <= 1e-3
            #assert abs(v1[i] - v3[i]) <= 1e-3
            #print(f"{v1[i]}: {v2[i]}")
            print(f"{v1[i]} : {v2[i]} : {v3[i]}")


input_circuit_dir = sys.argv[1]
output_qasm_dir = sys.argv[2]
testset_id_st = int(sys.argv[3])
testset_id_ed = int(sys.argv[4])
for testset_id in range(testset_id_st, testset_id_ed+1):
    convert(input_circuit_dir, output_qasm_dir, testset_id)
