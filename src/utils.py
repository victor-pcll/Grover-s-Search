import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram
import numpy as np

def counts_to_m(counts, n, t_bits):
    """
    Convertit les coups (counts) en m estimé, EN INVERSANT LES BITS.
    """
    if not counts:
        return 0.0, None, None

    # 1. On prend la mesure la plus fréquente
    measured_bin = max(counts, key=counts.get)
    
    # --- CORRECTION CRITIQUE ICI ---
    # On inverse la chaîne binaire car Qiskit/QPE sort souvent les bits 
    # dans l'ordre inverse de la lecture binaire standard pour la phase.
    measured_bin_reversed = measured_bin[::-1] 
    
    k = int(measured_bin_reversed, 2)
    
    # 2. Calcul de la phase phi
    phi = k / (2**t_bits)
    
    # 3. Calcul de m
    N = 2**n
    m_est = N * (np.sin(np.pi * phi))**2 # Note: theta/2 = pi*phi
    
    return m_est, measured_bin_reversed, phi

def analyze_and_plot(counts, n, t_bits, m_expected):
    N = 2**n
    
    # --- PRÉ-TRAITEMENT DES DONNÉES (INVERSION DES BITS) ---
    # On crée un nouveau dictionnaire avec les clés (entiers) corrigées
    counts_corrected = {}
    for bitstring, count in counts.items():
        # On inverse chaque bitstring mesuré
        val_int = int(bitstring[::-1], 2)
        counts_corrected[val_int] = count

    # Trouver le pic dans les données corrigées
    measured_int = max(counts_corrected, key=counts_corrected.get)
    phi_measured = measured_int / (2**t_bits)
    m_est = N * (np.sin(np.pi * phi_measured)**2)
    
    print(f"--- RÉSULTATS CORRIGÉS ---")
    print(f"Index mesuré (après inversion bits) : {measured_int}")
    print(f"Phase mesurée φ                     : {phi_measured:.6f}")
    print(f"Nombre d'éléments marqués estimé    : {m_est:.2f}")
    print(f"Nombre réel attendu (m)             : {m_expected}")
    
    # --- CALCUL THÉORIQUE ---
    theta_theo = 2 * np.arcsin(np.sqrt(m_expected / N))
    phi_theo_1 = theta_theo / (2 * np.pi)
    phi_theo_2 = 1.0 - phi_theo_1
    
    k_theo_1 = phi_theo_1 * (2**t_bits)
    k_theo_2 = phi_theo_2 * (2**t_bits)
    
    print(f"Pics théoriques attendus aux entiers : {k_theo_1:.1f} et {k_theo_2:.1f}")

    # --- VISUALISATION ---
    plt.figure(figsize=(12, 6))
    
    # On plotte les données corrigées
    plt.bar(counts_corrected.keys(), counts_corrected.values(), width=1.0, label="Mesures (Bits Inversés)")
    
    plt.axvline(k_theo_1, color='r', linestyle='--', linewidth=2, label=f"Théorie 1 ≈ {k_theo_1:.1f}")
    plt.axvline(k_theo_2, color='g', linestyle='--', linewidth=2, label=f"Théorie 2 ≈ {k_theo_2:.1f}")
    
    plt.title(f"Quantum Counting (Corrigé) - n={n}, t={t_bits}")
    plt.xlabel(f"Valeur de Phase (Entier 0 à {2**t_bits - 1})")
    plt.ylabel("Nombre de coups")
    plt.legend()
    plt.xlim(0, 2**t_bits)
    plt.grid(alpha=0.3)
    plt.show()

def analyze_results(counts, t_bits, label="Données"):
    # Correction de l'ordre des bits
    counts_corrected = {int(k[::-1], 2): v for k, v in counts.items()}
    return counts_corrected