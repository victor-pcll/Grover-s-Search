import numpy as np
from qiskit import QuantumCircuit

def oracle_single_target(n, target):
    qc = QuantumCircuit(n)

    # Flip |0> bits so that the target matches |111...1>
    for i, bit in enumerate(target):
        if bit == "0":
            qc.x(i)

    # Multi-controlled Z implemented via H–MCX–H
    if n == 1:
        qc.z(0)
    else:
        qc.h(n-1)
        qc.mcx(list(range(n-1)), n-1)
        qc.h(n-1)

    # Undo X flips
    for i, bit in enumerate(target):
        if bit == "0":
            qc.x(i)

    return qc