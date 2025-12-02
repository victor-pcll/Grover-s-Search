from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, thermal_relaxation_error
from qiskit.circuit.library import PhaseEstimation
from grover_unitary import grover_unitary

def quantum_counting_nosie(n, targets, t_bits=6, shots=4000, ancilla_qubits=1, noisy=False):
    # Build Grover unitary
    Gqc = grover_unitary(n, targets, ancilla_qubits=ancilla_qubits)

    # Phase estimation
    pe = PhaseEstimation(t_bits, Gqc)

    total_qubits = t_bits + n + ancilla_qubits
    qc = QuantumCircuit(total_qubits, t_bits)

    # Initialize data qubits
    for i in range(t_bits, total_qubits):
        qc.h(i)

    # Append phase estimation
    qc.append(pe, range(total_qubits))
    qc.measure(range(t_bits), range(t_bits))

    # Backend
    backend = AerSimulator()
    noise_model = None
    if noisy:
        noise_model = NoiseModel()
        p1 = 0.001  # probabilité de dépolarisation 1-qubit
        p2 = 0.01   # probabilité de dépolarisation 2-qubits
        noise_model.add_all_qubit_quantum_error(depolarizing_error(p1, 1), ['u1','u2','u3'])
        noise_model.add_all_qubit_quantum_error(depolarizing_error(p2, 2), ['cx'])

    job = backend.run(transpile(qc, backend), shots=shots, noise_model=noise_model)
    result = job.result()
    return result.get_counts()