import numpy as np
from qiskit import QuantumCircuit
from oracle.oracle_with_ancillas import oracle_with_ancillas
from oracle.oracle_single import oracle_no_ancilla
from diffusion import diffusion
from qiskit.quantum_info import Statevector

def grover_circuit(n, targets, iterations, ancilla_qubits=0):
    """
    Grover circuit simulation returning:
        qc: QuantumCircuit with measurements
        probs: list of probabilities of measuring a target after each iteration
    Parameters:
        n: number of data qubits
        targets: list of bitstrings representing marked states
        iterations: number of Grover iterations
        ancilla_qubits: number of ancilla qubits (0 for ancilla-free)
    """
    probs = []
    total_qubits = n + ancilla_qubits

    # Circuit sans mesure pour le statevector
    qc_sv = QuantumCircuit(total_qubits)
    qc_sv.h(range(n))  # superposition initiale sur les qubits de données

    # Construire l'oracle et la diffusion
    if ancilla_qubits > 0:
        oracle = oracle_with_ancillas(n, targets, ancilla_qubits)
        qc_sv.compose(oracle, qubits=range(total_qubits), inplace=True)
    else:
        # ancilla-free: composer plusieurs oracles si plusieurs targets
        oracle = QuantumCircuit(n)
        for t in targets:
            oracle.compose(oracle_no_ancilla(n, t), inplace=True)
        qc_sv.compose(oracle, qubits=range(n), inplace=True)

    diffuser = diffusion(n)

    for _ in range(iterations):
        # Appliquer oracle (déjà composé pour ancilla-free ou ancilla-based)
        if ancilla_qubits > 0:
            qc_sv.compose(oracle, qubits=range(total_qubits), inplace=True)
        else:
            qc_sv.compose(oracle, qubits=range(n), inplace=True)

        # Appliquer diffusion
        qc_sv.compose(diffuser, qubits=range(n), inplace=True)

        # Récupérer le statevector
        statevector = Statevector.from_instruction(qc_sv)

        # Calculer probabilité des états marqués
        if ancilla_qubits > 0:
            prob = sum(
                abs(statevector[int(t,2) + k*2**n])**2
                for t in targets
                for k in range(2**ancilla_qubits)
            )
        else:
            prob = sum(abs(statevector[int(t,2)])**2 for t in targets)

        probs.append(prob)

    # Circuit final avec mesure
    qc = QuantumCircuit(total_qubits)
    qc.compose(qc_sv, inplace=True)
    qc.measure_all()

    return qc, probs