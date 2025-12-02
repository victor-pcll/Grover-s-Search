from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.circuit.library import PhaseEstimation
from grover_unitary import grover_unitary

def quantum_counting(n, targets, t_bits=6, shots=2048, ancilla_qubits=1):

    # Build Grover unitary as a QuantumCircuit
    Gqc = grover_unitary(n, targets, ancilla_qubits=ancilla_qubits)

    # Phase estimation with QuantumCircuit
    pe = PhaseEstimation(t_bits, Gqc)

    total_qubits = t_bits + n + ancilla_qubits
    qc = QuantumCircuit(total_qubits, t_bits)

    # Initialize data qubits in uniform superposition
    for i in range(t_bits, total_qubits):
        qc.h(i)

    # Append Phase Estimation
    qc.append(pe, range(total_qubits))
    qc.measure(range(t_bits), range(t_bits))

    backend = AerSimulator()
    job = backend.run(transpile(qc, backend), shots=shots)
    result = job.result()
    return result.get_counts()