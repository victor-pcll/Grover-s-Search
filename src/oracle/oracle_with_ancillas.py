import numpy as np
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library.standard_gates import MCXGate

def oracle_with_ancillas(n, targets, ancilla_qubits=1):
    qr = QuantumRegister(n, "q")
    anc = QuantumRegister(ancilla_qubits, "anc") if ancilla_qubits > 0 else None
    qc = QuantumCircuit(qr, anc) if anc else QuantumCircuit(qr)

    for t in targets:
        # Prepare controls by flipping 0s
        for i, b in enumerate(t):
            if b == "0":
                qc.x(qr[i])

        # MCX with explicit ancilla if requested
        if anc:
            qc.append(MCXGate(n-1), list(range(n-1)) + [n-1])
        else:
            qc.h(n-1)
            qc.mcx(list(range(n-1)), n-1)
            qc.h(n-1)

        # Undo flips
        for i, b in enumerate(t):
            if b == "0":
                qc.x(qr[i])

    return qc