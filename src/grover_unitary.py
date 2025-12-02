import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from oracle.oracle_with_ancillas import oracle_with_ancillas
from diffusion import diffusion

def grover_unitary(n, targets, iterations=1, ancilla_qubits=1):
    total_qubits = n + ancilla_qubits
    qc = QuantumCircuit(total_qubits)

    oracle = oracle_with_ancillas(n, targets, ancilla_qubits)
    diffuser = diffusion(n)

    for _ in range(iterations):
        qc.compose(oracle, qubits=range(total_qubits), inplace=True)
        qc.compose(diffuser, qubits=range(n), inplace=True)

    return qc 