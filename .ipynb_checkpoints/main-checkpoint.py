import mrmustard.lab as lab
import numpy as np

# 1. Define the 2-mode Fock state |1, 0> directly
# n=[1, 0] means 1 photon in Mode 0, 0 photons in Mode 1
# cutoffs=[3, 3] ensures we have enough space for the math
state = lab.Fock(n=[1, 0], cutoffs=[3, 3])

# 2. Apply the 50/50 Beam Splitter
bs = lab.BSgate(theta=np.pi/4)
output_state = state >> bs[0, 1]

# 3. Extract probabilities
# We check the grid of all possibilities up to 2 photons per mode
probs = output_state.fock_probabilities(cutoffs=[3, 3])

print("Output Probabilities:")
print(f"|0, 0> (Vacuum): {probs[0, 0]*100:.1f}%")
print(f"|1, 0> (Stayed): {probs[1, 0]*100:.1f}%")
print(f"|0, 1> (Crossed): {probs[0, 1]*100:.1f}%")