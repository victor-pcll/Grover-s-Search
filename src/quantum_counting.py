import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.circuit.library import PhaseEstimation, GroverOperator

def quantum_counting(n, targets, t_bits=6, shots=4000, ancilla_qubits=0):
    
    # --- 1. Construction de l'Oracle de Phase ---
    # L'oracle doit inverser le signe (|x> -> -|x>) des états cibles.
    oracle = QuantumCircuit(n)
    for target in targets:
        # Inverse l'ordre pour correspondre à la convention Qiskit (q0 à droite)
        rev_target = target[::-1]
        
        # Applique des portes X pour que l'état cible devienne |11...1>
        for i, bit in enumerate(rev_target):
            if bit == '0':
                oracle.x(i)
        
        # Applique un Z multi-contrôlé (MCZ) sur tout le registre
        # Astuce: H -> MCX -> H est équivalent à MCZ
        oracle.h(n-1)
        oracle.mcx(list(range(n-1)), n-1)
        oracle.h(n-1)
        
        # Annule les portes X (Uncomputation)
        for i, bit in enumerate(rev_target):
            if bit == '0':
                oracle.x(i)

    # --- 2. Opérateur de Grover ---
    # Utiliser GroverOperator gère automatiquement le Diffuseur et les phases globales
    grover_op = GroverOperator(oracle)

    # --- 3. Phase Estimation ---
    pe = PhaseEstimation(t_bits, grover_op)

    # Le circuit total contient: t_bits (comptage) + n (recherche)
    total_qubits = t_bits + n
    qc = QuantumCircuit(total_qubits, t_bits)

    # Préparation: Registre de recherche (n derniers qubits) en superposition uniforme |+>
    # Note: Dans QPE, le registre d'état est après le registre de comptage
    state_qubits = range(t_bits, total_qubits)
    for q in state_qubits:
        qc.h(q)

    # Ajout du bloc Phase Estimation
    qc.append(pe, range(total_qubits))

    # Mesure du registre de comptage (les t_bits premiers qubits)
    qc.measure(range(t_bits), range(t_bits))

    # --- 4. Simulation ---
    backend = AerSimulator()
    # Transpile assure la compatibilité des portes
    t_qc = transpile(qc, backend)
    job = backend.run(t_qc, shots=shots)
    
    return job.result().get_counts()

def get_quantum_counting_circuit(n, targets, t_bits=3): # t_bits réduit à 3 pour minimiser le bruit
    # 1. Oracle (Code repris de votre fichier src/quantum_counting.py)
    oracle = QuantumCircuit(n)
    for target in targets:
        rev_target = target[::-1]
        for i, bit in enumerate(rev_target):
            if bit == '0': oracle.x(i)
        oracle.h(n-1)
        oracle.mcx(list(range(n-1)), n-1)
        oracle.h(n-1)
        for i, bit in enumerate(rev_target):
            if bit == '0': oracle.x(i)

    # 2. Grover Operator & QPE
    grover_op = GroverOperator(oracle)
    pe = PhaseEstimation(t_bits, grover_op)
    
    total_qubits = t_bits + n
    qc = QuantumCircuit(total_qubits, t_bits)
    
    # Initialisation |+> sur les qubits de recherche
    for q in range(t_bits, total_qubits):
        qc.h(q)
        
    qc.append(pe, range(total_qubits))
    qc.measure(range(t_bits), range(t_bits))
    
    return qc