# ===============================
# Visualization Helpers
# ===============================

import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram
import numpy as np

# --- 2) Quantum counting + estimate number of marked items ---
def counts_to_m(counts, n, t_bits):
    """
    Convert counts (from quantum_counting) into estimated m.
    Returns: (m_est, measured_bin, phi)
    - measured_bin: most frequent bitstring on the counting register (MSB...LSB)
    - phi = k / 2^t  (fractional phase)
    - m_est = N * sin^2(theta/2) where theta = 2*pi*phi
    """
    if not counts:
        return 0.0, None, None

    measured_bin = max(counts, key=counts.get)  # most frequent
    k = int(measured_bin, 2)
    phi = k / (2**t_bits)
    theta = 2 * np.pi * phi
    N = 2**n
    m_est = N * (np.sin(theta/2))**2
    return m_est, measured_bin, phi