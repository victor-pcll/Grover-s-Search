import numpy as np
from qiskit import QuantumCircuit, transpile
from oracle.oracle_with_ancillas import oracle_with_ancillas
from diffusion import diffusion
from qiskit_aer import AerSimulator

def grover_circuit(n, targets, iterations, ancilla_qubits=1):
    """
    Return Grover circuit + probability of marked states after each iteration
    using AerSimulator in statevector mode.
    """
    probs = []
    total_qubits = n + ancilla_qubits

    # Circuit sans mesure pour statevector
    qc = QuantumCircuit(total_qubits)
    qc.h(range(n))

    oracle = oracle_with_ancillas(n, targets, ancilla_qubits)
    diffuser = diffusion(n)

    backend = AerSimulator(method="statevector")

    for _ in range(iterations):
        qc.compose(oracle, qubits=range(total_qubits), inplace=True)
        qc.compose(diffuser, qubits=range(n), inplace=True)

        # Transpile and run
        t_qc = transpile(qc, backend)
        result = backend.run(t_qc).result()

        # Get statevector
        statevector = result.get_statevector(t_qc)

        # Compute probability of marked states
        prob = sum([abs(statevector[int(t, 2)])**2 for t in targets])
        probs.append(prob)

    return qc, probs