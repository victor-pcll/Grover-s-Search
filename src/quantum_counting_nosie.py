import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
from qiskit.circuit.library import PhaseEstimation, GroverOperator

def quantum_counting_nosie(n, targets, t_bits=6, shots=4000, noisy=False, error_prob=0.005):
    
    # --- 1. Construction de l'Oracle Robuste ---
    oracle = QuantumCircuit(n)
    for target in targets:
        rev_target = target[::-1]
        for i, bit in enumerate(rev_target):
            if bit == '0': oracle.x(i)
        
        # MCZ (H -> MCX -> H)
        oracle.h(n-1)
        oracle.mcx(list(range(n-1)), n-1)
        oracle.h(n-1)
        
        for i, bit in enumerate(rev_target):
            if bit == '0': oracle.x(i)

    # --- 2. Opérateur de Grover ---
    grover_op = GroverOperator(oracle)

    # --- 3. Circuit Phase Estimation ---
    pe = PhaseEstimation(t_bits, grover_op)
    
    total_qubits = t_bits + n
    qc = QuantumCircuit(total_qubits, t_bits)

    # Initialisation : Seulement les qubits de recherche en |+>
    for q in range(t_bits, total_qubits):
        qc.h(q)

    qc.append(pe, range(total_qubits))
    qc.measure(range(t_bits), range(t_bits))

    # --- 4. Configuration du Bruit ---
    backend = AerSimulator()
    noise_model = None
    
    if noisy:
        noise_model = NoiseModel()
        # Erreur sur les portes à 1 qubit (u1, u2, u3 -> ou générique 'u', 'sx', 'rz')
        error_1q = depolarizing_error(error_prob, 1)
        # Erreur sur les CNOT (2 qubits) - souvent plus bruyantes
        error_2q = depolarizing_error(error_prob * 10, 2)
        
        # On ajoute le bruit aux portes standards (basis gates)
        noise_model.add_all_qubit_quantum_error(error_1q, ['u', 'sx', 'rz', 'x', 'h'])
        noise_model.add_all_qubit_quantum_error(error_2q, ['cx'])
        
        print(f"Simulation avec bruit (p1={error_prob}, p2={error_prob*10}) activée.")
    else:
        print("Simulation idéale (sans bruit).")

    # --- 5. Exécution ---
    # Important : définir basis_gates pour que le bruit s'applique correctement lors de la transpilation
    basis_gates = noise_model.basis_gates if noise_model else None
    
    t_qc = transpile(qc, backend, basis_gates=basis_gates)
    job = backend.run(t_qc, shots=shots, noise_model=noise_model)
    
    return job.result().get_counts()