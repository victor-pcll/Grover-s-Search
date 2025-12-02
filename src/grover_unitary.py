import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import MCXGate
from oracle.oracle_with_ancillas import oracle_with_ancillas
from diffusion import diffusion

def grover_unitary(n, targets, ancilla_qubits=1):
    total_qubits = n + ancilla_qubits
    qc = QuantumCircuit(total_qubits)

    oracle = oracle_with_ancillas(n, targets, ancilla_qubits=ancilla_qubits)
    diffuser = diffusion(n)

    # Compose oracle on all qubits (data + ancilla)
    qc.compose(oracle, qubits=range(total_qubits), inplace=True)
    # Compose diffuser on data qubits only
    qc.compose(diffuser, qubits=range(n), inplace=True)

    return qc