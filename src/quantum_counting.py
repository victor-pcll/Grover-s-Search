from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.circuit.library import PhaseEstimation
from grover_unitary import grover_unitary

def quantum_counting(n, targets, t_bits=6, shots=4000, ancilla_qubits=1):

    # Build Grover gate
    G = grover_unitary(n, targets, ancilla_qubits=ancilla_qubits)
    # PhaseEstimation expects a unitary (Gate or Circuit)
    pe = PhaseEstimation(t_bits, G)

    # Build the full circuit: evaluation qubits (t_bits) + target register (G.num_qubits)
    total_qubits = pe.num_qubits  # should equal t_bits + G.num_qubits
    qc = QuantumCircuit(total_qubits, t_bits)

    # Prepare target register in uniform superposition (indices t_bits ... total_qubits-1)
    for q in range(t_bits, total_qubits):
        qc.h(q)

    # Append phase estimation circuit (it expects evaluation then target)
    qc.append(pe, range(total_qubits))

    # Measure evaluation (first t_bits)
    qc.measure(range(t_bits), range(t_bits))

    # Run on QASM simulator (shots)
    backend = AerSimulator()
    t_qc = transpile(qc, backend)
    job = backend.run(t_qc, shots=shots)
    result = job.result()
    counts = result.get_counts()
    return counts