import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from oracle.oracle_with_ancillas import oracle_with_ancillas
from oracle.oracle_single import oracle_no_ancilla
from diffusion import diffusion

def grover_circuit(n, targets, iterations, ancilla_qubits=0):
    probs = []
    total_qubits = n + ancilla_qubits

    # 1. Initialisation : Superposition
    qc_sv = QuantumCircuit(total_qubits)
    qc_sv.h(range(n)) 

    # 2. Préparation des objets (Oracle et Diffuser) pour ne pas les recréer en boucle
    if ancilla_qubits > 0:
        # On crée un gros oracle qui gère tout
        oracle_gate = oracle_with_ancillas(n, targets, ancilla_qubits)
    else:
        # Ancilla-free : on combine les oracles si plusieurs cibles
        oracle_gate = QuantumCircuit(n)
        for t in targets:
            oracle_gate.compose(oracle_no_ancilla(n, t), inplace=True)
            
    diffuser_gate = diffusion(n)

    # 3. Boucle de Grover
    for _ in range(iterations):
        # --- A. Appliquer l'Oracle ---
        if ancilla_qubits > 0:
            qc_sv.compose(oracle_gate, qubits=range(total_qubits), inplace=True)
        else:
            qc_sv.compose(oracle_gate, qubits=range(n), inplace=True)

        # --- B. Appliquer la Diffusion ---
        qc_sv.compose(diffuser_gate, qubits=range(n), inplace=True)

        # --- C. Calculer la probabilité ---
        # Note: Statevector.from_instruction est lourd, mais ok pour la simulation
        statevector = Statevector.from_instruction(qc_sv)

        if ancilla_qubits > 0:
            # On somme sur tous les états des ancillas (k) pour chaque target (t)
            # Attention à l'endianness de tes targets vs Qiskit
            prob = sum(
                abs(statevector[int(t[::-1], 2) + k*(2**n)])**2 
                for t in targets 
                for k in range(2**ancilla_qubits)
            )
            # Note sur int(t[::-1], 2) : 
            # Qiskit lit de droite à gauche (Little Endian). 
            # Si tes targets sont "100" pour le chiffre 4, Qiskit attend '001'.
            # Essaie avec et sans [::-1] si tes probs restent faibles.
        else:
            # Même remarque pour l'inversion des bits si nécessaire
            prob = sum(abs(statevector[int(t, 2)])**2 for t in targets)

        probs.append(prob)

    # Circuit final avec mesure
    qc = QuantumCircuit(total_qubits)
    qc.compose(qc_sv, inplace=True)
    qc.measure_all()

    return qc, probs