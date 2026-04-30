from mrmustard import math

math.change_backend(
    "tensorflow"
)  # numpy backend lacks `convolution`, needed by PNRDetector

import mrmustard.lab as lab
import numpy as np

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

# --- State to teleport: |psi>_C = alpha |H> + beta |V> ------------
alpha = 0.6 + 0.0j
beta  = 0.8 + 0.0j

psi_C = np.zeros((2, 2), dtype=complex)
psi_C[1, 0] = alpha   # |H>_C
psi_C[0, 1] = beta    # |V>_C

# --- Bell pair on AB: (|HH> - |VV>) / sqrt(2) ---------------------
bell_AB = np.zeros((2, 2, 2, 2), dtype=complex)
bell_AB[1, 0, 1, 0] =  1 / np.sqrt(2)   # |H>_A |H>_B
bell_AB[0, 1, 0, 1] = -1 / np.sqrt(2)   # |V>_A |V>_B

# --- Full input state |psi>_C ⊗ |Bell>_AB on six modes ------------
input_ket = np.zeros((3, 3, 3, 3, 2, 2), dtype=complex)
input_ket[:2, :2, :2, :2, :, :] = np.einsum("ij,klmn->ijklmn", psi_C, bell_AB)
input_state = lab.State(ket=input_ket)

# --- Bell measurement apparatus on (C, A) -------------------------
phi_error = np.pi / 10
ps_H = lab.Rgate(angle=phi_error)
bs_H = lab.BSgate(theta=np.pi / 4)
bs_V = lab.BSgate(theta=np.pi / 4)
circuit = lab.Circuit([
    ps_H[0],     # relative phase error on C_H only (e^{i*phi}*alpha|H> + beta|V>)
    bs_H[0, 2],  # mix C_H with A_H
    bs_V[1, 3],  # mix C_V with A_V
])

mode_labels = ["C_H", "C_V", "A_H", "A_V", "B_H", "B_V"]
mode_groups = [[0, 1], [2, 3], [4, 5]]

explain_circuit(circuit, mode_labels)
print(f"State to teleport: |psi>_C = {alpha.real:.4f} |H> + {beta.real:.4f} |V>")
print()
input_braket = state_to_braket(input_state, [2, 2, 2, 2, 2, 2], mode_groups)
print("INPUT |psi>_C ⊗ |Bell>_AB (groups: C, A, B):")
print(f"  {input_braket}")
print()

# --- Run the circuit and extract Bob's conditional state ----------
output_state = input_state >> circuit
out_ket = np.asarray(output_state.ket(cutoffs=[3, 3, 3, 3, 2, 2]))

bell_measurement(out_ket, "Phi_minus", psi_C)
