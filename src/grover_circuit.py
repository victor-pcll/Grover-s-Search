import numpy as np
from qiskit import QuantumCircuit
from oracle.oracle_with_ancillas import oracle_with_ancillas
from diffusion import diffusion
from qiskit.quantum_info import Statevector

def grover_circuit(n, targets, iterations, ancilla_qubits=1):
    """
    Returns:
        qc: QuantumCircuit with measurements (can be drawn)
        probs: list of probabilities of marked states after each Grover iteration
    """
    probs = []
    total_qubits = n + ancilla_qubits

    # Circuit sans mesure pour statevector
    qc_sv = QuantumCircuit(total_qubits)
    qc_sv.h(range(n))  # superposition initiale

    oracle = oracle_with_ancillas(n, targets, ancilla_qubits)
    diffuser = diffusion(n)

    for _ in range(iterations):
        qc_sv.compose(oracle, qubits=range(total_qubits), inplace=True)
        qc_sv.compose(diffuser, qubits=range(n), inplace=True)

        # ✅ Récupérer directement le statevector
        statevector = Statevector.from_instruction(qc_sv)

        # Probabilité des états marqués
        prob = sum([abs(statevector[int(t,2)])**2 for t in targets])
        probs.append(prob)

    # Créer un circuit final pour la mesure (si nécessaire)
    qc = QuantumCircuit(total_qubits)
    qc.compose(qc_sv, inplace=True)
    qc.measure_all()

    return qc, probs