# Grover’s Search & Quantum Counting — EPFL PHYS-541 Project (2025–2026)

This repository contains my work for Project 6 — Grover and Quantum Counting
Course: Quantum Computing (PHYS-541), 2025–2026
Teacher: Vincenzo Savona — vincenzo.savona@epfl.ch
Assistants: Sara Alves dos Santos, David Linteau, Shao Chiew

⸻

## 🎯 Project Goals

This project studies Grover’s search algorithm and the quantum counting extension. It combines a careful theoretical presentation with hands-on implementations and noise-sensitivity studies using Qiskit (QASM simulator).

Specifically:
1.	Read and understand Grover’s algorithm (Nielsen & Chuang and other sources) and present:
	•	algorithm derivation,
	•	amplitude amplification,
	•	geometric picture and Grover angle \theta,
	•	quantum counting (phase estimation applied to the Grover operator).
2.	Analyze Grover’s algorithm from a complexity perspective:
	•	importance for quantum computational complexity,
	•	limitations on speedups for NP problems,
	•	optimality proof and lower bounds.
3.	Implement Grover’s algorithm in Qiskit (QASM simulator):
	•	build oracles for f(x):\{0,1\}^n\to\{0,1\} with m solutions (try m=1 and m=2),
	•	explore implementations with and without ancilla qubits,
	•	use ancillas and Toffoli gates where useful (similar to Fig. 4.10 in Nielsen & Chuang),
	•	implement the full Grover iteration and run searches for several n.
4.	Implement and test the quantum counting algorithm (estimate m via phase estimation of the Grover operator).
5.	Study algorithm robustness to noise:
	•	simulate noise with Qiskit Aer noise models,
	•	measure how success probability degrades as n and circuit depth increase,
	•	focus on regimes with small Grover angle (\theta/2 \sim \sqrt{m/N}) where many Grover iterations are required,
	•	find the largest practical n before noise dominates.

⸻

## 🔧 Implementation Notes
	•	Oracles: implement flexible oracle constructors that can represent any chosen set of targets (binary strings). Provide:
	•	ancilla-based oracles using multi-controlled Toffolis, and
	•	ancilla-free constructions when possible (discuss tradeoffs).
	•	Grover iteration: compose oracle + diffusion operator; allow variable number of iterations.
	•	Quantum counting: implement phase estimation on the Grover operator to extract the eigenphase and infer m.
	•	Noise study: compare ideal (noiseless) QASM simulator and noisy simulations (Aer noise models). When comparing encoded vs unencoded or single-qubit experiments, remember to apply identity gates to trigger noise on “idle” qubits.

⸻

## 📂 Suggested Repository Structure

```
.
├── src/
│   ├── grover/
│   │   ├── oracle.py            # oracle builders (ancilla-based, ancilla-free)
│   │   ├── diffusion.py         # diffusion operator implementations
│   │   ├── grover.py            # compose iterations, run experiments
│   │   └── counting.py          # quantum counting (phase estimation on Grover)
│   ├── utils.py                 # helpers: state prep, bitstrings, measurement
│   └── noise_experiments.py     # scripts to run noisy simulations and aggregate results
├── results/
│   ├── success_probabilities/   # JSON/CSV with experimental data
│   ├── noise_plots/             # plots comparing noise levels and n
│   └── readme_results.md
├── requirements.txt
├── notebook.ipynb
└── README.md
```

⸻

## 🧪 Usage & Quick Start

Install dependencies (recommended inside a virtualenv):

pip install -r requirements.txt

Typical workflow examples:
	•	Run a single Grover experiment (noiseless) for n=5, m=1:

python -m src.grover.grover --n 5 --targets "00101" --iterations 7 --backend qasm_simulator

	•	Run quantum counting to estimate m:

python -m src.grover.counting --n 5 --targets_file targets.json --precision 6

	•	Run noisy simulations (Aer noise model):

python src/noise_experiments.py --n 6 --m 1 --noise_model depolarizing --p 0.001 --shots 2000

(Concrete CLI flags and scripts should be implemented inside src/ according to the repo’s design.)

⸻

## 📈 Experiments to Include
	•	Success probability vs number of Grover iterations for various n, m.
	•	Probability of measuring a target vs total database size N=2^n.
	•	Quantum counting accuracy vs precision of phase estimation.
	•	Noise sensitivity: compare ideal vs noisy runs; plot threshold where noise obliterates advantage.
	•	Comparison of ancilla-based vs ancilla-free oracle depth/gate counts.

⸻

## ⚙️ Requirements
	•	Python 3.11+
	•	Qiskit (qiskit, qiskit-aer)
	•	NumPy, SciPy, Matplotlib, Pandas (for data analysis)
	•	Jupyter

Example requirements.txt:

qiskit
qiskit-aer
numpy
scipy
matplotlib
pandas
jupyter

⸻

## 📚 References
	•	M. A. Nielsen & I. L. Chuang — Quantum Computation and Quantum Information (Grover chapter)
	•	L. K. Grover — A fast quantum mechanical algorithm for database search
	•	Brassard, Høyer, Mosca, Tapp — Quantum Amplitude Amplification and Estimation
	•	Textbooks and lecture notes on complexity theory and lower bounds for quantum search# Grover-s-Search
