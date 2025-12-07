import numpy as np
from qiskit import QuantumCircuit

def oracle_no_ancilla(n, target):
    """
    Ancilla-free *phase* oracle for a single target bitstring of length n.
    It flips the phase of |target>.
    """
    qc = QuantumCircuit(n)
    # flip 0-bits so target becomes all ones
    for i, b in enumerate(target):
        if b == '0':
            qc.x(i)
    # multi-controlled Z via H + MCX + H on last qubit
    if n == 1:
        qc.z(0)
    else:
        qc.h(n-1)
        qc.mcx(list(range(n-1)), n-1)
        qc.h(n-1)
    # undo flips
    for i, b in enumerate(target):
        if b == '0':
            qc.x(i)
    return qc