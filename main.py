from mrmustard import math
math.change_backend("tensorflow")  # numpy backend lacks `convolution`, needed by PNRDetector

import mrmustard.lab as lab
import numpy as np
from mrmustard.lab import circuit_drawer

# ============================================================
# BELL STATE MEASUREMENT APPARATUS (for quantum teleportation)
# ============================================================
# Mode layout (polarization encoded as separate bosonic modes):
#   Mode 0: spatial port A, Horizontal (H)
#   Mode 1: spatial port A, Vertical   (V)
#   Mode 2: spatial port B, Horizontal (H)
#   Mode 3: spatial port B, Vertical   (V)
#
# Note on PBS: because H and V are already represented as
# *distinct* modes, the polarizing beam splitter at each output
# arm is just spatial routing — it has no operator to apply.

# --- Components --------------------------------------------------

# 50/50 beam splitter, polarization-preserving:
# acts independently on the H pair (0,2) and the V pair (1,3).
bs_H = lab.BSgate(theta=np.pi/4)
bs_V = lab.BSgate(theta=np.pi/4)

# Four photon-number-resolving detectors, one per output mode.
det_AH = lab.PNRDetector(modes=[0])
det_AV = lab.PNRDetector(modes=[1])
det_BH = lab.PNRDetector(modes=[2])
det_BV = lab.PNRDetector(modes=[3])

# --- Circuit -----------------------------------------------------

circuit = lab.Circuit([
    bs_H[0, 2],
    bs_V[1, 3],
])

print("=" * 60)
print("BELL STATE MEASUREMENT APPARATUS")
print("=" * 60)
print(circuit_drawer.circuit_text(circuit.ops))
print()
print("Detectors: PNR on modes 0 (A_H), 1 (A_V), 2 (B_H), 3 (B_V)")
print()

# --- Input state: |Psi+> = (|HV> + |VH>) / sqrt(2) ---------------
# In the 4-mode encoding (A_H, A_V, B_H, B_V):
#   |H>_A |V>_B = |1,0,0,1>
#   |V>_A |H>_B = |0,1,1,0>
ket = np.zeros((2, 2, 2, 2), dtype=complex)
ket[1, 0, 0, 1] = 1 / np.sqrt(2)
ket[0, 1, 1, 0] = 1 / np.sqrt(2)
psi_plus = lab.State(ket=ket)

# --- Apply the circuit and read joint photon-number probabilities --
output_state = psi_plus >> circuit
# cutoff 3 per mode lets us also see Phi-state outcomes (2 photons in one mode)
probs = output_state.fock_probabilities(cutoffs=[3, 3, 3, 3])

def p(a_h, a_v, b_h, b_v):
    return float(probs[a_h, a_v, b_h, b_v])

print("=" * 60)
print("INPUT: |Psi+> = (|HV> + |VH>) / sqrt(2)")
print("=" * 60)
print(f"  Both clicks in arm A (A_H & A_V): {p(1,1,0,0)*100:6.2f}%")
print(f"  Both clicks in arm B (B_H & B_V): {p(0,0,1,1)*100:6.2f}%")
print(f"  Split: A_H & B_V                : {p(1,0,0,1)*100:6.2f}%")
print(f"  Split: A_V & B_H                : {p(0,1,1,0)*100:6.2f}%")
