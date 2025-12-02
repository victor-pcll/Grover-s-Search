# Qiskit Reference Guide

This document summarizes the principal Qiskit functions, their purpose, and examples of how to use them. It is intended as a personal reference while developing quantum circuits.

---

1. Quantum Circuits and Registers

Qiskit uses QuantumCircuit, QuantumRegister, and ClassicalRegister as the basic building blocks.

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

# Quantum register with 3 qubits
qr = QuantumRegister(3, 'q')

# Classical register with 3 bits
cr = ClassicalRegister(3, 'c')

# Quantum circuit using the registers
qc = QuantumCircuit(qr, cr)

	•	QuantumRegister(n, name): collection of n qubits.
	•	ClassicalRegister(n, name): collection of n classical bits to store measurements.
	•	QuantumCircuit(qr, cr): builds a circuit from quantum and classical registers.

---

2. Basic Quantum Gates

Gate	Function	Example
x(q)	Pauli-X (NOT)	qc.x(q[0])
h(q)	Hadamard	qc.h(q)
cx(q0, q1)	CNOT	qc.cx(q[0], q[1])
z(q)	Pauli-Z	qc.z(q[0])
rx(theta, q)	Rotation around X	qc.rx(np.pi/2, q[0])
ry(theta, q)	Rotation around Y	qc.ry(np.pi/2, q[0])
rz(theta, q)	Rotation around Z	qc.rz(np.pi/2, q[0])

	•	Use qc.draw('mpl') to visualize the circuit.

---

3. Multi-Controlled Gates

from qiskit.circuit.library import MCXGate

# Multi-controlled X (Toffoli for 2 controls)
mcx = MCXGate(2)
qc.append(mcx, [0,1,2])  # controls: q0,q1, target: q2

	•	MCXGate can use ancilla qubits for more than 2 controls.

---

4. Measurement

qc.measure(qr, cr)

	•	Measures all qubits in qr into classical bits cr.
	•	Measurement is needed to get results from a quantum circuit.

---

5. Simulators and Execution

from qiskit_aer import AerSimulator
from qiskit import transpile

# Initialize simulator
sim = AerSimulator()

# Transpile for backend optimization
tqc = transpile(qc, sim)

# Run the circuit
job = sim.run(tqc, shots=1024)
result = job.result()

# Get measurement counts
counts = result.get_counts()

	•	shots: number of repetitions to get statistics.
	•	result.get_counts(): returns a dict of bitstrings with their counts.
	•	plot_histogram(counts): visualizes the results.

---

6. Statevector Simulation

sim_sv = AerSimulator(method='statevector')
job = sim_sv.run(tqc)
state = job.result().get_statevector()

	•	Returns the full quantum state vector.
	•	Useful for debugging algorithms like Grover or phase estimation.

---

7. Quantum Circuit Composition

qc1 = QuantumCircuit(2)
qc1.h(0)

qc2 = QuantumCircuit(2)
qc2.cx(0,1)

# Compose circuits
```
qc1.compose(qc2, inplace=True)
```

Combines circuits sequentially.  
inplace=True modifies the original circuit.  

---

8. Common Libraries

```
from qiskit.circuit.library import PhaseEstimation, QFT
from qiskit.quantum_info import Operator
```

PhaseEstimation: builds circuits for quantum counting / estimation.  
QFT: Quantum Fourier Transform.   
Operator: converts a circuit into a matrix operator.

---

9. Visualization
```
from qiskit.visualization import plot_histogram
```

# Plot measurement histogram
```
plot_histogram(counts)
```

# Draw circuit
```
qc.draw('mpl')
````

'mpl' → matplotlib plot  
'text' → ASCII diagram  
'latex' → LaTeX rendering  
'iqx' → IBM Quantum Experience style  

---

10. Tips
	
Always transpile circuits for the backend before running.  
Use AerSimulator for local simulation.  
For real devices, you need to account for gate errors and noise.  
For algorithms like Grover or phase estimation, separate statevector simulation (debug) and shot-based simulation (measurements).