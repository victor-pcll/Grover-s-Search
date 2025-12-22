from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import MCXGrayCode, MCXVChain
from qiskit_aer import AerSimulator

def get_oracle_complexity(n, method='noancilla'):
    """
    Construit un circuit équivalent à un Oracle (MCX) et mesure sa profondeur.
    """
    num_controls = n - 1
    
    if method == 'noancilla':
        # MCXGrayCode : 0 ancilla nécessaire
        gate = MCXGrayCode(num_controls)
        num_ancillas = 0
        
        qc = QuantumCircuit(n)
        qc.append(gate, range(n))
        
    elif method == 'ancilla':
        # MCXVChain : Besoin de (num_controls - 2) ancillas
        # Si num_controls <= 2 (donc n <= 3), on a besoin de 0 ancilla (c'est une Toffoli)
        num_ancillas = max(0, num_controls - 2)
        
        # On instancie la porte
        gate = MCXVChain(num_controls, dirty_ancillas=False)
        
        # Total qubits = données + ancillas
        total_qubits = n + num_ancillas
        qc = QuantumCircuit(total_qubits)
        
        # Ordre des qubits pour append : [contrôles, cible, ancillas]
        controls = list(range(num_controls))
        target = [n - 1]
        
        # S'il y a des ancillas, on les ajoute à la liste
        if num_ancillas > 0:
            ancillas = list(range(n, total_qubits))
            qc.append(gate, controls + target + ancillas)
        else:
            # Cas n=3 (Toffoli simple), pas d'ancillas dans l'append
            qc.append(gate, controls + target)

    # --- TRANSPILATION ---
    # On utilise AerSimulator juste pour avoir un backend de référence, 
    # mais on force les basis_gates pour standardiser la métrique.
    backend = AerSimulator()
    t_qc = transpile(qc, basis_gates=['u', 'cx'], optimization_level=1)
    
    return t_qc.depth()