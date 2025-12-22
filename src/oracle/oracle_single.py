import numpy as np
from qiskit import QuantumCircuit

def oracle_no_ancilla(n, target):
    """
    Ancilla-free *phase* oracle for a single target bitstring of length n.
    It flips the phase of |target>.
    """
    qc = QuantumCircuit(n)
    rev_t = target[::-1]
    for i, b in enumerate(rev_t):
        if b=='0': qc.x(i)
    qc.h(n-1); qc.mcx(list(range(n-1)), n-1); qc.h(n-1)
    for i, b in enumerate(rev_t):
        if b=='0': qc.x(i)
    return qc