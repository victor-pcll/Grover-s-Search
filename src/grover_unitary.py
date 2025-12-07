import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from oracle.oracle_with_ancillas import oracle_with_ancillas
from oracle.oracle_single import oracle_no_ancilla
from diffusion import diffusion

def grover_unitary(n, targets, iterations=1, ancilla_qubits=1):
    total = n + ancilla_qubits
    qc = QuantumCircuit(total, name="G")

    # choose oracle implementation depending on ancilla_qubits
    if ancilla_qubits == 0:
        # For simplicity, assume single target if ancilla-free.
        # If targets has multiple elements and ancilla_qubits==0, we compose flips for each.
        for t in targets:
            qc.compose(oracle_no_ancilla(n, t), qubits=range(n), inplace=True)
    else:
        qc.compose(oracle_with_ancillas(n, targets, ancilla_qubits), qubits=range(total), inplace=True)

    # diffusion acts only on the first n qubits — embed it
    qc.compose(diffusion(n), qubits=list(range(n)), inplace=True)

    # Convert to gate
    G = qc.to_gate()
    G.name = "G"
    return G