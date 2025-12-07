from qiskit import QuantumCircuit

def oracle_with_ancillas(n, targets, ancilla_qubits=0):
    """
    Build an oracle that flips the phase of all target states.
    The oracle acts on n data qubits + ancilla_qubits (optional).
    Returns a QuantumCircuit on (n + ancilla_qubits).
    
    Parameters:
    - n: number of data qubits
    - targets: list of bitstrings of length n
    - ancilla_qubits: number of ancilla qubits for multi-controlled X
    """
    total = n + ancilla_qubits
    qc = QuantumCircuit(total)

    for t in targets:
        # Step 1: flip qubits to prepare controls
        for i, b in enumerate(t):
            if b == "0":
                qc.x(i)

        # Step 2: apply multi-controlled X to ancilla (or last qubit if no ancilla)
        if ancilla_qubits > 0:
            # Use first ancilla as target for MCX
            target_anc = n
            extra_ancillas = list(range(n+1, total)) if ancilla_qubits > 1 else []
            if extra_ancillas:
                qc.mcx(list(range(n)), target_anc, extra_ancillas)
            else:
                qc.mcx(list(range(n)), target_anc)
            # Step 3: phase flip
            qc.z(target_anc)
            # Step 4: uncompute
            if extra_ancillas:
                qc.mcx(list(range(n)), target_anc, extra_ancillas)
            else:
                qc.mcx(list(range(n)), target_anc)
        else:
            # Ancilla-free: use last data qubit as target for phase flip
            if n == 1:
                qc.z(0)
            else:
                qc.h(n-1)
                qc.mcx(list(range(n-1)), n-1)
                qc.h(n-1)

        # Step 5: undo flips
        for i, b in enumerate(t):
            if b == "0":
                qc.x(i)

    return qc