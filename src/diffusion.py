import numpy as np
from qiskit import QuantumCircuit

def diffusion(n):
    qc = QuantumCircuit(n)
    qc.h(range(n))
    qc.x(range(n))
    qc.h(n-1); qc.mcx(list(range(n-1)), n-1); qc.h(n-1)
    qc.x(range(n))
    qc.h(range(n))
    return qc