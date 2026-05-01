from mrmustard import math

math.change_backend(
    "tensorflow"
)  # numpy backend lacks `convolution`, needed by PNRDetector

import mrmustard.lab as lab
import numpy as np
import matplotlib.pyplot as plt

from display_utils import explain_circuit, state_to_braket
from teleportation_utils import bell_measurement

# ============================================================
# QUANTUM TELEPORTATION
# ============================================================
# Extends the Bell-state-measurement apparatus by adding a third
# qubit C carrying the state we want to teleport. Six-mode layout:
#
#   Mode 0: C_H \  state to teleport
#   Mode 1: C_V /
#   Mode 2: A_H \  Alice's half of the Bell pair
#   Mode 3: A_V /
#   Mode 4: B_H \  Bob's half of the Bell pair
#   Mode 5: B_V /
#
# Bell measurement is performed on (C, A): a 50/50 BS on each
# polarization followed by photon-number-resolving detection on
# modes 0..3. Bob's qubit (modes 4, 5) carries the post-measurement
# state. The classical X/Z correction Bob applies based on the
# measurement result is left for later.

# --- Bell pair on AB: (|HH> - |VV>) / sqrt(2) ---------------------
bell_AB = np.zeros((2, 2, 2, 2), dtype=complex)
bell_AB[1, 0, 1, 0] =  1 / np.sqrt(2)   # |H>_A |H>_B
bell_AB[0, 1, 0, 1] = -1 / np.sqrt(2)   # |V>_A |V>_B

# --- Pre-build circuits for each phi_error (independent of alpha/beta) ---
phi_errors = [np.pi / 40 * m for m in range(-40, 41)]
circuits = []
for phi_error in phi_errors:
    ps_H = lab.Rgate(angle=phi_error)
    bs_H = lab.BSgate(theta=np.pi / 4)
    bs_V = lab.BSgate(theta=np.pi / 4)
    circuits.append(lab.Circuit([
        ps_H[0],     # relative phase error on C_H only
        bs_H[0, 2],  # mix C_H with A_H
        bs_V[1, 3],  # mix C_V with A_V
    ]))

phi_deg = np.degrees(phi_errors)

# --- Sweep over (alpha, beta) pairs -----------------------------------
# alpha^2 steps from 0 to 1 in increments of 0.1; beta = sqrt(1 - alpha^2)
alpha_sq_values = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.55, 0.65, 0.75, 0.85, 0.95]
colors = plt.cm.plasma(np.linspace(0.05, 0.95, len(alpha_sq_values)))

fig, ax = plt.subplots(figsize=(8, 5))

for color, alpha_sq in zip(colors, alpha_sq_values):
    alpha = float(np.sqrt(alpha_sq))
    beta  = float(np.sqrt(1.0 - alpha_sq))

    psi_C = np.zeros((2, 2), dtype=complex)
    psi_C[1, 0] = alpha   # |H>_C
    psi_C[0, 1] = beta    # |V>_C

    input_ket = np.zeros((3, 3, 3, 3, 2, 2), dtype=complex)
    input_ket[:2, :2, :2, :2, :, :] = np.einsum("ij,klmn->ijklmn", psi_C, bell_AB)
    input_state = lab.State(ket=input_ket)

    all_fidelities = []
    for circuit in circuits:
        output_state = input_state >> circuit
        out_ket = np.asarray(output_state.ket(cutoffs=[3, 3, 3, 3, 2, 2]))
        fidelities = bell_measurement(out_ket, "Phi_minus", psi_C, verbose=False)
        all_fidelities.append(fidelities)

    outcomes = list(all_fidelities[0].keys())
    stacked = np.stack([np.array([fd[k] for fd in all_fidelities]) for k in outcomes])

    # Verify outcomes agree; average for the plot
    per_phi_spread = stacked.max(axis=0) - stacked.min(axis=0)
    max_spread = float(per_phi_spread.max())
    print(f"α²={alpha_sq:.1f}  α={alpha:.4f}  β={beta:.4f}  | max spread between outcomes = {max_spread:.2e}")

    mean_fidelity = stacked.mean(axis=0)
    beta_sq = round(1.0 - alpha_sq, 10)
    label = rf"α=$\sqrt{{{alpha_sq:.4g}}}$, β=$\sqrt{{{beta_sq:.4g}}}$"
    ax.plot(phi_deg, mean_fidelity, color=color, linewidth=1.5, marker="o", markersize=3, label=label)

ax.set_xlabel("Phase error φ (degrees)")
ax.set_ylabel("Fidelity F")
ax.set_title("Teleportation fidelity vs. phase error (resource: Φ⁻)")
ax.set_ylim(-0.05, 1.05)
ax.axhline(1.0, color="gray", linestyle="--", linewidth=0.8)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=7, ncol=2, loc="lower center")
plt.tight_layout()
plt.savefig("fidelity_vs_phase_error.png", dpi=150)
plt.show()
print("Plot saved to fidelity_vs_phase_error.png")
