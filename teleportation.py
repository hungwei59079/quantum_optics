from mrmustard import math

math.change_backend(
    "tensorflow"
)  # numpy backend lacks `convolution`, needed by PNRDetector

import mrmustard.lab as lab
import numpy as np

from display_utils import explain_circuit, state_to_braket

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
# Modes 0-3 are padded to dimension 3 (not 2) so the Fock space has
# room for 2-photon states that arise after the BS (HOM bunching).
# Without this, mrmustard truncates at index 1 and the bunched
# outcomes |2,0,0,0>, |0,2,0,0>, etc. are all silently zeroed out.
input_ket = np.zeros((3, 3, 3, 3, 2, 2), dtype=complex)
input_ket[:2, :2, :2, :2, :, :] = np.einsum("ij,klmn->ijklmn", psi_C, bell_AB)
input_state = lab.State(ket=input_ket)

# --- Bell measurement apparatus on (C, A) -------------------------
bs_H = lab.BSgate(theta=np.pi / 4)
bs_V = lab.BSgate(theta=np.pi / 4)
circuit = lab.Circuit([
    bs_H[0, 2],   # mix C_H with A_H
    bs_V[1, 3],   # mix C_V with A_V
])

mode_labels = ["C_H", "C_V", "A_H", "A_V", "B_H", "B_V"]
mode_groups = [[0, 1], [2, 3], [4, 5]]

print("=" * 60)
print("QUANTUM TELEPORTATION (Bell measurement on C and A)")
print("=" * 60)
explain_circuit(circuit, mode_labels)
print()
print("Detectors: PNR on modes 0..3 (C_H, C_V, A_H, A_V)")
print()
print(f"State to teleport: |psi>_C = {alpha.real:.4f} |H> + {beta.real:.4f} |V>")
print()
input_braket = state_to_braket(input_state, [2, 2, 2, 2, 2, 2], mode_groups)
print("INPUT |psi>_C ⊗ |Bell>_AB (groups: C, A, B):")
print(f"  {input_braket}")
print()

# --- Run the circuit and extract Bob's conditional state ----------
output_state = input_state >> circuit
out_ket = np.asarray(output_state.ket(cutoffs=[3, 3, 3, 3, 2, 2]))

print("=" * 60)
print("Outcomes |n_C_H, n_C_V, n_A_H, n_A_V> and Bob's conditional state:")
print("=" * 60)

threshold = 1e-6
total_p = 0.0
for n0, n1, n2, n3 in np.ndindex(3, 3, 3, 3):
    if n0 + n1 + n2 + n3 != 2:
        continue  # photon-number conservation: 2 photons land on the C/A side
    sub = out_ket[n0, n1, n2, n3, :, :]
    prob = float(np.sum(np.abs(sub) ** 2))
    if prob < threshold:
        continue
    total_p += prob
    cond_ket = sub / np.sqrt(prob)
    bob_state = lab.State(ket=cond_ket)
    bob_braket = state_to_braket(bob_state, [2, 2], [[0, 1]])
    outcome = f"|{n0},{n1},{n2},{n3}>"
    print(f"  {outcome:<13} P={prob*100:6.2f}%   Bob -> {bob_braket}")

print()
print(f"Total probability over listed outcomes: {total_p*100:6.2f}%")
