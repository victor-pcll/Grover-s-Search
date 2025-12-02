# ===============================
# Visualization Helpers
# ===============================

import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram
import numpy as np

# --- 2) Quantum counting + estimate number of marked items ---
def counts_to_m(counts, n, t_bits):
    """
    Convert the output of quantum counting to an estimate of m
    counts: dict from quantum_counting
    n: number of data qubits
    t_bits: number of counting qubits
    """
    # Take the most frequent measurement
    measured_bin = max(counts, key=counts.get)
    k = int(measured_bin, 2)
    
    # Phase phi and Grover angle theta
    phi = k / (2**t_bits)
    theta = 2 * np.pi * phi
    
    # Estimate number of marked items
    N = 2**n
    m_est = N * (np.sin(theta/2))**2
    return m_est, measured_bin, phi