import matplotlib.pyplot as plt
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
from qiskit.circuit.library import GroverOperator, MCMT, ZGate

def get_grover_probability(n, iterations, noise_model=None):
    """
    Exécute Grover pour un nombre donné d'itérations et retourne P(success).
    """
    # 1. Oracle pour l'état |1...1>
    # Pour GroverOperator, l'oracle doit inverser la phase.
    # On utilise MCMT (Multi-Controlled Multi-Target) avec la porte Z
    oracle = QuantumCircuit(n)
    oracle.append(MCMT(ZGate(), num_ctrl_qubits=n-1, num_target_qubits=1), range(n))

    # 2. Grover Operator
    grover_op = GroverOperator(oracle)
    
    # 3. Circuit Complet
    qc = QuantumCircuit(n)
    qc.h(range(n)) # Superposition initiale
    
    for _ in range(iterations):
        qc.compose(grover_op, inplace=True)
        
    qc.measure_all()
    
    # 4. Simulation
    backend = AerSimulator()
    
    # Si on a du bruit, il faut transpiler avec les portes de base du modèle
    basis_gates = noise_model.basis_gates if noise_model else None
    
    t_qc = transpile(qc, backend, basis_gates=basis_gates)
    result = backend.run(t_qc, noise_model=noise_model, shots=1000).result()
    counts = result.get_counts()
    
    # Compter les succès (Cible = '11...1')
    target_state = '1' * n
    success_count = counts.get(target_state, 0)
    
    return success_count / 1000.0


def generate_noise_model(p_err):
    """Crée un modèle de bruit dépolarisant simple."""
    if p_err == 0:
        return None
    noise_model = NoiseModel()
    # Erreur sur les portes 1 qubit (faible)
    noise_model.add_all_qubit_quantum_error(depolarizing_error(p_err, 1), ['u', 'sx', 'rz', 'h', 'x'])
    # Erreur sur les CNOT (souvent 10x plus forte)
    noise_model.add_all_qubit_quantum_error(depolarizing_error(p_err*10, 2), ['cx'])
    return noise_model


def get_max_grover_success(n, p_error):
    """
    Retourne la probabilité de succès de Grover pour n qubits
    au nombre optimal d'itérations, sous un bruit donné.
    """
    # 1. Calcul du nombre d'itérations optimal
    N = 2**n
    optimal_iterations = int(np.floor(np.pi/4 * np.sqrt(N)))
    
    # 2. Construction du Circuit
    # Oracle de phase (marque l'état |1...1>)
    oracle = QuantumCircuit(n)
    # MCMT est une façon propre de faire un Z multi-contrôlé
    oracle.append(MCMT(ZGate(), num_ctrl_qubits=n-1, num_target_qubits=1), range(n))
    
    grover_op = GroverOperator(oracle)
    
    qc = QuantumCircuit(n)
    qc.h(range(n))
    
    for _ in range(optimal_iterations):
        qc.compose(grover_op, inplace=True)
        
    qc.measure_all()
    
    # 3. Modèle de Bruit
    noise_model = None
    if p_error > 0:
        noise_model = NoiseModel()
        # On met du bruit surtout sur les portes à 2 qubits (les plus fragiles)
        # On suppose que l'erreur 2-qubits est 10x l'erreur 1-qubit
        noise_model.add_all_qubit_quantum_error(depolarizing_error(p_error, 1), ['u', 'sx', 'rz', 'h', 'x'])
        noise_model.add_all_qubit_quantum_error(depolarizing_error(p_error*10, 2), ['cx'])
    
    # 4. Simulation
    backend = AerSimulator()
    # Transpilation nécessaire pour appliquer le bruit sur les portes natives
    t_qc = transpile(qc, backend, basis_gates=noise_model.basis_gates if noise_model else None)
    
    # On augmente les shots pour avoir une bonne statistique
    shots = 2000
    result = backend.run(t_qc, noise_model=noise_model, shots=shots).result()
    counts = result.get_counts()
    
    # Cible = tout à 1
    target = '1' * n
    success_prob = counts.get(target, 0) / shots
    
    return success_prob

def get_success_rate(n, error_rate, shots=1024):
    """
    Simule Grover pour une taille n et un taux d'erreur donné.
    Retourne la probabilité de succès (0.0 à 1.0).
    """
    # Nombre d'itérations optimal
    N = 2**n
    k_opt = int(np.floor(np.pi/4 * np.sqrt(N)))
    
    # Construction du circuit
    # Oracle 'noancilla' implicite via MCMT (le plus sensible au bruit car profond)
    oracle = QuantumCircuit(n)
    oracle.append(MCMT(ZGate(), num_ctrl_qubits=n-1, num_target_qubits=1), range(n))
    
    grover_op = GroverOperator(oracle)
    
    qc = QuantumCircuit(n)
    qc.h(range(n))
    for _ in range(k_opt):
        qc.compose(grover_op, inplace=True)
    qc.measure_all()
    
    # Modèle de bruit
    noise_model = None
    if error_rate > 0:
        noise_model = NoiseModel()
        # On assume que l'erreur 2-qubits (CX) est dominante
        error_gate = depolarizing_error(error_rate, 2)
        noise_model.add_all_qubit_quantum_error(error_gate, ['cx'])
        # On ajoute un peu de bruit 1-qubit aussi (10x moins)
        error_1q = depolarizing_error(error_rate/10, 1)
        noise_model.add_all_qubit_quantum_error(error_1q, ['u', 'sx', 'rz', 'h', 'x'])

    # Simulation
    backend = AerSimulator()
    t_qc = transpile(qc, backend, basis_gates=noise_model.basis_gates if noise_model else None)
    
    # On utilise 'method="density_matrix"' si n est petit pour plus de précision, 
    # mais 'standard' (shots) est plus rapide et robuste.
    result = backend.run(t_qc, noise_model=noise_model, shots=shots).result()
    counts = result.get_counts()
    
    target = '1' * n
    return counts.get(target, 0) / shots