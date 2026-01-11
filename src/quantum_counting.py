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

def get_quantum_counting_circuit(n, targets, t_bits=3):
    # --- 1. Gestion Intelligente des Ancillas ---
    # Pour n=3 (2 contrôles), pas besoin d'ancilla.
    # Pour n>=4, on utilise v-chain pour réduire la profondeur.
    num_controls = n - 1
    use_ancilla = num_controls >= 3 
    
    num_ancillas = max(0, num_controls - 2) if use_ancilla else 0
    total_oracle_qubits = n + num_ancillas
    
    # Indices
    work_qubits = list(range(n)) 
    ancilla_qubits = list(range(n, total_oracle_qubits)) 
    
    # --- 2. Construction de l'Oracle ---
    oracle = QuantumCircuit(total_oracle_qubits)
    
    for target in targets:
        rev_target = target[::-1]
        
        # A. Flip des 0
        for i, bit in enumerate(rev_target):
            if bit == '0': oracle.x(work_qubits[i])
        
        # B. Porte MCX (Conditionnelle)
        target_qubit = work_qubits[-1]
        control_qubits = work_qubits[:-1]
        
        oracle.h(target_qubit) # On passe en mode Phase (Z)
        
        if use_ancilla:
            # Mode optimisé pour grands circuits
            oracle.mcx(
                control_qubits=control_qubits,
                target_qubit=target_qubit,
                ancilla_qubits=ancilla_qubits,
                mode='v-chain'
            )
        else:
            # Mode standard pour n=3 (Toffoli simple)
            oracle.mcx(control_qubits, target_qubit)
            
        oracle.h(target_qubit) # Retour en mode Bit
        
        # C. Uncomputation
        for i, bit in enumerate(rev_target):
            if bit == '0': oracle.x(work_qubits[i])

    # --- 3. Grover Operator ---
    # IMPORTANT: On ne diffuse QUE sur les qubits de travail
    grover_op = GroverOperator(oracle, reflection_qubits=work_qubits)
    
    # --- 4. QPE ---
    pe = PhaseEstimation(t_bits, grover_op)
    
    # --- 5. Assemblage Final ---
    grand_total = t_bits + total_oracle_qubits
    qc = QuantumCircuit(grand_total, t_bits)
    
    # Init |+> sur les qubits de travail UNIQUEMENT
    # Les ancillas restent à |0> (c'est crucial pour v-chain)
    state_qubits_indices = range(t_bits, t_bits + n)
    for q in state_qubits_indices:
        qc.h(q)
        
    qc.append(pe, range(grand_total))
    
    qc.measure(range(t_bits), range(t_bits))
    
    return qc