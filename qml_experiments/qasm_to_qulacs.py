import re
import typing
from cmath import phase
from typing import List
import numpy as np
import qulacs_core

from qulacs import QuantumCircuit
from qulacs.gate import DenseMatrix, Identity

FIXED_POINT_PATTERN = r"[+-]?\d+(?:\.\d*)?|\.\d+"
FLOATING_POINT_PATTERN = r"[eE][-+]?\d+"
GENERAL_NUMBER_PATTERN = (
    rf"(?:{FIXED_POINT_PATTERN})(?:{FLOATING_POINT_PATTERN})?"  # noqa
)

def convert_QASM_to_qulacs_circuit(
    input_strs: typing.List[str], *, remap_remove: bool = False
) -> QuantumCircuit:
    # convert QASM List[str] to qulacs QuantumCircuit.
    # constraints: qreg must be named q, and creg cannot be used.

    mapping: List[int] = []

    for instr_moto in input_strs:
        # process input string for parsing instruction.
        instr = instr_moto.lower().strip().replace(" ", "").replace("\t", "")
        if instr == "":
            continue
        if instr[0:4] == "qreg":
            matchobj = re.match(r"qregq\[(\d+)\];", instr)
            assert matchobj is not None
            ary = matchobj.groups()
            cir = QuantumCircuit(int(ary[0]))
            if len(mapping) == 0:
                mapping = list(range(int(ary[0])))
        elif instr[0:2] == "cx":
            matchobj = re.match(r"cxq\[(\d+)\],q\[(\d+)\];", instr)
            assert matchobj is not None
            ary = matchobj.groups()
            cir.add_CNOT_gate(mapping[int(ary[0])], mapping[int(ary[1])])
        elif instr[0:2] == "cz":
            matchobj = re.match(r"czq\[(\d+)\],q\[(\d+)\];", instr)
            assert matchobj is not None
            ary = matchobj.groups()
            cir.add_CZ_gate(mapping[int(ary[0])], mapping[int(ary[1])])
        elif instr[0:4] == "swap":
            matchobj = re.match(r"swapq\[(\d+)\],q\[(\d+)\];", instr)
            assert matchobj is not None
            ary = matchobj.groups()
            cir.add_SWAP_gate(mapping[int(ary[0])], mapping[int(ary[1])])
        elif instr[0:2] == "id":
            matchobj = re.match(r"idq\[(\d+)\];", instr)
            assert matchobj is not None
            ary = matchobj.groups()
            cir.add_gate(Identity(mapping[int(ary[0])]))
        elif instr[0:2] == "xq":
            matchobj = re.match(r"xq\[(\d+)\];", instr)
            assert matchobj is not None
            ary = matchobj.groups()
            cir.add_X_gate(mapping[int(ary[0])])
        elif instr[0:2] == "yq":
            matchobj = re.match(r"yq\[(\d+)\];", instr)
            assert matchobj is not None
            ary = matchobj.groups()
            cir.add_Y_gate(mapping[int(ary[0])])
        elif instr[0:2] == "zq":
            matchobj = re.match(r"zq\[(\d+)\];", instr)
            assert matchobj is not None
            ary = matchobj.groups()
            cir.add_Z_gate(mapping[int(ary[0])])
        elif instr[0:2] == "hq":
            matchobj = re.match(r"hq\[(\d+)\];", instr)
            assert matchobj is not None
            ary = matchobj.groups()
            cir.add_H_gate(mapping[int(ary[0])])
        elif instr[0:2] == "sq":
            matchobj = re.match(r"sq\[(\d+)\];", instr)
            assert matchobj is not None
            ary = matchobj.groups()
            cir.add_S_gate(mapping[int(ary[0])])
        elif instr[0:4] == "sdgq":
            matchobj = re.match(r"sdgq\[(\d+)\];", instr)
            assert matchobj is not None
            ary = matchobj.groups()
            cir.add_Sdag_gate(mapping[int(ary[0])])
        elif instr[0:2] == "tq":
            matchobj = re.match(r"tq\[(\d+)\];", instr)
            assert matchobj is not None
            ary = matchobj.groups()
            cir.add_T_gate(mapping[int(ary[0])])
        elif instr[0:4] == "tdgq":
            matchobj = re.match(r"tdgq\[(\d+)\];", instr)
            assert matchobj is not None
            ary = matchobj.groups()
            cir.add_Tdag_gate(mapping[int(ary[0])])
        elif instr[0:2] == "rx":
            matchobj = re.match(rf"rx\(({GENERAL_NUMBER_PATTERN})\)q\[(\d+)\];", instr)
            assert matchobj is not None
            ary = matchobj.groups()
            cir.add_RX_gate(mapping[int(ary[1])], -float(ary[0]))
        elif instr[0:2] == "ry":
            matchobj = re.match(rf"ry\(({GENERAL_NUMBER_PATTERN})\)q\[(\d+)\];", instr)
            assert matchobj is not None
            ary = matchobj.groups()
            cir.add_RY_gate(mapping[int(ary[1])], -float(ary[0]))
        elif instr[0:2] == "rz":
            matchobj = re.match(rf"rz\(({GENERAL_NUMBER_PATTERN})\)q\[(\d+)\];", instr)
            assert matchobj is not None
            ary = matchobj.groups()
            cir.add_RZ_gate(mapping[int(ary[1])], -float(ary[0]))
        elif instr[0:1] == "p":
            matchobj = re.match(rf"p\({GENERAL_NUMBER_PATTERN}\)q\[(\d+)\];", instr)
            assert matchobj is not None
            ary = matchobj.groups()
            cir.add_U1_gate(mapping[int(ary[1])], float(ary[0]))
        elif instr[0:2] == "u1":
            matchobj = re.match(rf"u1\(({GENERAL_NUMBER_PATTERN})\)q[(\d+)];", instr)
            assert matchobj is not None
            ary = matchobj.groups()
            cir.add_U1_gate(mapping[int(ary[1])], float(ary[0]))
        elif instr[0:2] == "u2":
            matchobj = re.match(
                rf"u2\(({GENERAL_NUMBER_PATTERN}),"
                + rf"({GENERAL_NUMBER_PATTERN})\)q\[(\d+)\];",
                instr,
            )
            assert matchobj is not None
            ary = matchobj.groups()
            cir.add_U2_gate(mapping[int(ary[2])], float(ary[0]), float(ary[1]))
        elif instr[0:2] == "u3":
            matchobj = re.match(
                rf"u3\(({GENERAL_NUMBER_PATTERN}),"
                + rf"({GENERAL_NUMBER_PATTERN}),"
                + rf"({GENERAL_NUMBER_PATTERN})\)q\[(\d+)\];",
                instr,
            )
            assert matchobj is not None
            ary = matchobj.groups()
            cir.add_U3_gate(
                mapping[int(ary[3])], float(ary[0]), float(ary[1]), float(ary[2])
            )
        elif instr[0:1] == "u":
            matchobj = re.match(
                rf"u\(({GENERAL_NUMBER_PATTERN}),"
                + rf"({GENERAL_NUMBER_PATTERN}),"
                + rf"({GENERAL_NUMBER_PATTERN})\)q\[(\d+)\];",
                instr,
            )
            assert matchobj is not None
            ary = matchobj.groups()
            cir.add_U3_gate(
                mapping[int(ary[3])], float(ary[0]), float(ary[1]), float(ary[2])
            )
        elif instr[0:3] == "sxq":
            matchobj = re.match(r"sxq\[(\d+)\];", instr)
            assert matchobj is not None
            ary = matchobj.groups()
            cir.add_sqrtX_gate(mapping[int(ary[0])])
        elif instr[0:5] == "sxdgq":
            matchobj = re.match(r"sxdgq\[(\d+)\];", instr)
            assert matchobj is not None
            ary = matchobj.groups()
            cir.add_sqrtXdag_gate(mapping[int(ary[0])])
        elif instr[0:11] == "densematrix":
            # Matches all matrix elements and qubit indexes
            deary = re.findall(r"[+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?", instr)
            target_qubit_count = int(deary[0])
            control_qubit_count = int(deary[1])

            gate_mat = np.zeros(
                (2**target_qubit_count, 2**target_qubit_count), dtype="complex"
            )
            bas = 2
            for i in range(2**target_qubit_count):
                for j in range(2**target_qubit_count):
                    gate_mat[i][j] = float(deary[bas]) + float(deary[bas + 1]) * 1.0j
                    bas += 2
            control_values = []
            for i in range(control_qubit_count):
                control_values.append(mapping[int(deary[bas])])
                bas += 1
            terget_indexes = []
            for i in range(target_qubit_count):
                terget_indexes.append(mapping[int(deary[bas])])
                bas += 1

            dense_gate = DenseMatrix(terget_indexes, gate_mat)  # type:ignore
            for i in range(control_qubit_count):
                control_index = int(deary[bas])
                bas += 1
                dense_gate.add_control_qubit(control_index, control_values[i])
            cir.add_gate(dense_gate)
        elif remap_remove and instr[0:4] == "//q[":
            matchobj = re.match(r"//q\[(\d+)-->q\[(\d+)\]", instr)
            assert matchobj is not None
            ary = matchobj.groups()
            if not (ary is None):
                mapping[int(ary[0])] = int(ary[1])
        elif remap_remove and instr[0:8] == "//qubits":
            matchobj = re.match(r"//qubits:(\d+)", instr)
            assert matchobj is not None
            ary = matchobj.groups()
            mapping = list(range(int(ary[0])))
        elif instr == "openqasm2.0;" or instr == 'include"qelib1.inc";':
            # related to file format, not for read.
            pass
        else:
            raise RuntimeError(f"unknown line: {instr}")
    return cir