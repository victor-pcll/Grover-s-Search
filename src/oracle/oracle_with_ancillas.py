from qiskit import QuantumCircuit

def oracle_with_ancillas(n, targets, ancilla_qubits=0):
    qc = QuantumCircuit(n + ancilla_qubits)
    for t in targets:
        # Flip 0s pour préparer les contrôles
        for i, b in enumerate(t):
            if b == "0":
                qc.x(i)
        
        # Appliquer MCX avec ou sans ancillas
        if n > 2:
            if ancilla_qubits > 0:
                qc.mcx(list(range(n-1)), n-1, list(range(n, n+ancilla_qubits)))
            else:
                qc.mcx(list(range(n-1)), n-1)
        else:
            # Cas n=2 ou n=1
            if n == 2:
                qc.cx(0,1)
            else:
                qc.z(0)
        
        # Undo flips
        for i, b in enumerate(t):
            if b == "0":
                qc.x(i)
    return qc