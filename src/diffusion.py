import numpy as np
from qiskit import QuantumCircuit

def diffusion(n):
    qc = QuantumCircuit(n)
    qc.h(range(n))
    qc.x(range(n))
    if n == 1:
        qc.z(0)
    elif n == 2:
        qc.h(1)
        qc.cx(0,1)
        qc.h(1)
    else:
        qc.h(n-1)
        qc.mcx(list(range(n-1)), n-1)
        qc.h(n-1)
    qc.x(range(n))
    qc.h(range(n))
    return qc