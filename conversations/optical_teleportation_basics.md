# Quantum_Teleportation_Corrections_Explained

**Source:** [https://gemini.google.com/share/2b621b1c4948](https://gemini.google.com/share/2b621b1c4948)
**Created:** 發布時間：2026年5月13日 下午04:29

---


## User (建議不要嘗試讀我貼上的code，直接跳到Gemini回覆就好)
This is my (vibe coded) simulation of a quantum teleportation (resource state directly prepared, no SPDC yet) 
 from mrmustard import math 
 math.change_backend( 
     "tensorflow" 
 )  # numpy backend lacks `convolution`, needed by PNRDetector 
 import mrmustard.lab as lab 
 import numpy as np 
 from display_utils import explain_circuit, state_to_braket 
 #### ============================================================ 
 #### QUANTUM TELEPORTATION 
 #### ============================================================ 
 #### Extends the Bell-state-measurement apparatus by adding a third 
 #### qubit C carrying the state we want to teleport. Six-mode layout: 
 #### 
 #   Mode 0: C_H \  state to teleport 
 ####   Mode 1: C_V / 
 ####   Mode 2: A_H \  Alice's half of the Bell pair 
 ####   Mode 3: A_V / 
 ####   Mode 4: B_H \  Bob's half of the Bell pair 
 ####   Mode 5: B_V / 
 #### 
 # Bell measurement is performed on (C, A): a 50/50 BS on each 
 #### polarization followed by photon-number-resolving detection on 
 #### modes 0..3. Bob's qubit (modes 4, 5) carries the post-measurement 
 #### state. The classical X/Z correction Bob applies based on the 
 #### measurement result is left for later. 
 #### --- State to teleport: |psi>_C = alpha |H> + beta |V> ------------ 
 alpha = 0.6 + 0.0j 
 beta  = 0.8 + 0.0j 
 psi_C = np.zeros((2, 2), dtype=complex) 
 psi_C[1, 0] = alpha   # |H>_C 
 psi_C[0, 1] = beta    # |V>_C 
 #### --- Bell pair on AB: (|HH> - |VV>) / sqrt(2) --------------------- 
 bell_AB = np.zeros((2, 2, 2, 2), dtype=complex) 
 bell_AB[1, 0, 1, 0] =  1 / np.sqrt(2)   # |H>_A |H>_B 
 bell_AB[0, 1, 0, 1] = -1 / np.sqrt(2)   # |V>_A |V>_B 
 #### --- Full input state |psi>_C ⊗ |Bell>_AB on six modes ------------ 
 input_ket = np.zeros((3, 3, 3, 3, 2, 2), dtype=complex) 
 input_ket[:2, :2, :2, :2, :, :] = np.einsum("ij,klmn->ijklmn", psi_C, bell_AB) 
 input_state = lab.State(ket=input_ket) 
 #### --- Bell measurement apparatus on (C, A) ------------------------- 
 bs_H = lab.BSgate(theta=np.pi / 4) 
 bs_V = lab.BSgate(theta=np.pi / 4) 
 circuit = lab.Circuit([ 
     bs_H[0, 2],   # mix C_H with A_H 
     bs_V[1, 3],   # mix C_V with A_V 
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
 print(f"  {input_braket}") 
 print() 
 #### --- Run the circuit and extract Bob's conditional state ---------- 
 output_state = input_state >> circuit 
 out_ket = np.asarray(output_state.ket(cutoffs=[3, 3, 3, 3, 2, 2])) 
 def apply_X(ket): 
     """X on Bob's polarization qubit: swap |H> and |V>.""" 
     return np.swapaxes(ket, 0, 1) 
 def apply_Z(ket): 
     """Z on Bob's polarization qubit: phase flip on |V>.""" 
     new_ket = ket.copy() 
     new_ket[:, 1] *= -1 
     return new_ket 
 #### Derived for resource state |Phi-> = (|HH> - |VV>)/sqrt(2). 
 #### Bunched outcomes (Phi+/Phi- ambiguous in this BS-only scheme) get 
 #### no entry: no single Pauli correction recovers |psi> from them. 
 corrections = { 
     (1, 0, 0, 1): ("X",), 
     (0, 1, 1, 0): ("X",), 
     (1, 1, 0, 0): ("X", "Z"),  # apply X first, then Z 
     (0, 0, 1, 1): ("Z", "X"),  # apply Z first, then X 
 } 
 print("=" * 60) 
 print("Outcomes |n_C_H, n_C_V, n_A_H, n_A_V> -- Bob raw, then post-correction:") 
 print("=" * 60) 
 threshold = 1e-6 
 total_p = 0.0 
 for n0, n1, n2, n3 in np.ndindex(3, 3, 3, 3): 
     if n0 + n1 + n2 + n3 != 2: 
         continue  # photon-number conservation: 2 photons land on the C/A side 
     sub = out_ket[n0, n1, n2, n3, :, :] 
     prob = float(np.sum(np.abs(sub) ** 2)) 
     if prob < threshold: 
         continue 
     total_p += prob 
     cond_ket = sub / np.sqrt(prob) 
     raw_braket = state_to_braket(lab.State(ket=cond_ket), [2, 2], [[0, 1]]) 
     outcome = f"|{n0},{n1},{n2},{n3}>" 
     print(f"  {outcome:<13} P={prob*100:6.2f}%   raw : {raw_braket}") 
     key = (n0, n1, n2, n3) 
     if key in corrections: 
         ops = corrections[key] 
         corr_ket = cond_ket 
         for op in ops: 
             corr_ket = apply_X(corr_ket) if op == "X" else apply_Z(corr_ket) 
         corr_braket = state_to_braket( 
             lab.State(ket=corr_ket), [2, 2], [[0, 1]], 
         ) 
         ops_str = " then ".join(ops) 
         print(f"  {'':<13}                apply {ops_str}: {corr_braket}") 
     else: 
         print(f"  {'':<13}                [Phi+/Phi- ambiguous -- no Pauli correction recovers |psi>]") 
 print() 
 print(f"Total probability over listed outcomes: {total_p*100:6.2f}%") 
 Could you explain why when the resource state is $\Phi-$, the correction is as given by the dictionary "correction"? I think you need to write the rewrite the input state as linear combination of Bell state $\otimes$ unknown state (but here the Bell state refers to Alice's pair) and then see what happens to this state after applying BS.


## Gemini
You are absolutely spot on with your intuition. To understand why those specific corrections work, we need to do exactly what you suggested: write the total input state, rewrite the Charlie-Alice ($CA$) portion in the Bell basis, and evaluate what state Bob ($B$) is left holding. Then, we map those $CA$ Bell states to the physical photon-number outcomes created by the beamsplitters.
Here is the step-by-step derivation of your simulation's logic.

#### 1. The Total Input State
First, we define the resource state on Alice and Bob's side, which in your code is the $\Phi^-$ Bell state:
$$
|\Phi^-\rangle_{AB} = \frac{1}{\sqrt{2}}(|H_A H_B\rangle - |V_A V_B\rangle)
$$
The unknown state we want to teleport on Charlie's mode is:
$$
|\psi\rangle_C = \alpha|H_C\rangle + \beta|V_C\rangle
$$
The total state of the system before the beamsplitters is the tensor product of these two:
$$
|\Psi\rangle_{CAB} = |\psi\rangle_C \otimes |\Phi^-\rangle_{AB}
$$
$$
|\Psi\rangle_{CAB} = \frac{1}{\sqrt{2}} (\alpha|H_C\rangle + \beta|V_C\rangle) \otimes (|H_A H_B\rangle - |V_A V_B\rangle)
$$
Expanding this out gives us four terms:
$$
|\Psi\rangle_{CAB} = \frac{1}{\sqrt{2}} \big( \alpha|H_C H_A H_B\rangle - \alpha|H_C V_A V_B\rangle + \beta|V_C H_A H_B\rangle - \beta|V_C V_A V_B\rangle \big)
$$

#### 2. Rewriting in the CA Bell Basis
Now, we perform the change of basis you mentioned. We want to express the joint state of modes $C$ and $A$ in terms of the four standard Bell states:
$$
|\Phi^\pm\rangle_{CA} = \frac{1}{\sqrt{2}}(|H_C H_A\rangle \pm |V_C V_A\rangle)
$$
$$
|\Psi^\pm\rangle_{CA} = \frac{1}{\sqrt{2}}(|H_C V_A\rangle \pm |V_C H_A\rangle)
$$
By inverting these relations, we can replace the tensor products in our expanded total state:
- $|H_C H_A\rangle = \frac{1}{\sqrt{2}}(|\Phi^+\rangle_{CA} + |\Phi^-\rangle_{CA})$
- $|V_C V_A\rangle = \frac{1}{\sqrt{2}}(|\Phi^+\rangle_{CA} - |\Phi^-\rangle_{CA})$
- $|H_C V_A\rangle = \frac{1}{\sqrt{2}}(|\Psi^+\rangle_{CA} + |\Psi^-\rangle_{CA})$
- $|V_C H_A\rangle = \frac{1}{\sqrt{2}}(|\Psi^+\rangle_{CA} - |\Psi^-\rangle_{CA})$
Substituting these back into $|\Psi\rangle_{CAB}$ and grouping the terms by the $CA$ Bell states, we get the classic teleportation equation, specifically tailored to your $\Phi^-$ resource state:
$$
|\Psi\rangle_{CAB} = \frac{1}{2} \Big[ |\Phi^+\rangle_{CA}(\alpha|H_B\rangle - \beta|V_B\rangle) + |\Phi^-\rangle_{CA}(\alpha|H_B\rangle + \beta|V_B\rangle) + |\Psi^+\rangle_{CA}(\beta|H_B\rangle - \alpha|V_B\rangle) - |\Psi^-\rangle_{CA}(\beta|H_B\rangle + \alpha|V_B\rangle) \Big]
$$

#### 3. Mapping Optics to Outcomes
In a linear optical Bell-State Measurement (BSM), you cannot deterministically distinguish all four Bell states using just beamsplitters and photon counters. When modes $C$ and $A$ pass through the 50/50 beamsplitters (which mix $H$ with $H$, and $V$ with $V$), Hong-Ou-Mandel (HOM) interference dictates the physical outcomes:
- **The Φ± States (Bunched):** Because the photons have identical polarizations ($HH$ or $VV$), HOM interference forces them to bunch together. They will both exit the same port of the beamsplitter. You will detect 2 photons in one mode and 0 in the other. Your simple PNR setup cannot distinguish the $\pm$ phase of this bunching, which is why your code correctly notes they are "ambiguous" and discards them.
- **The Ψ± States (Anti-bunched):** Because the photons have orthogonal polarizations ($HV$ or $VH$), they do not bunch in the same way. They trigger coincidence counts (1 photon in two different detectors).
  - $|\Psi^-\rangle_{CA}$ results in photons in different spatial modes but different polarizations: Outcomes **`1,0,0,1`** ($C_H, A_V$) and **`0,1,1,0`** ($C_V, A_H$).
  - $|\Psi^+\rangle_{CA}$ results in photons in the same spatial mode but different polarizations: Outcomes **`1,1,0,0`** ($C_H, C_V$) and **`0,0,1,1`** ($A_H, A_V$).

#### 4. Deriving the Dictionary Corrections
Now we can look at what state Bob is holding for these anti-bunched outcomes and verify your dictionary.

##### The ∣Ψ−⟩CA​ Outcomes: `(1,0,0,1)` and `(0,1,1,0)`
If the detectors register one of these patterns, the $CA$ system collapsed into $|\Psi^-\rangle$. Looking back at our grouped equation, Bob is left holding:
$$
|\psi_{Bob}\rangle = -(\beta|H_B\rangle + \alpha|V_B\rangle)
$$
To recover the original state $|\psi\rangle_C = \alpha|H\rangle + \beta|V\rangle$, Bob needs to swap the amplitudes of $H$ and $V$. This is the bit-flip operator, $X$:
$$
X \big( -(\beta|H_B\rangle + \alpha|V_B\rangle) \big) = -\alpha|H_B\rangle - \beta|V_B\rangle = -|\psi\rangle_C
$$
Because global phases (the minus sign) do not affect measurement probabilities or the density matrix, Bob has successfully recovered the state.
**Conclusion:** Applying `"X"` is correct.

##### The ∣Ψ+⟩CA​ Outcomes: `(1,1,0,0)` and `(0,0,1,1)`
If the detectors register these patterns, the $CA$ system collapsed into $|\Psi^+\rangle$. Bob is left holding:
$$
|\psi_{Bob}\rangle = \beta|H_B\rangle - \alpha|V_B\rangle
$$
To fix this, Bob must swap the amplitudes *and* fix the relative phase.
- **For `(1,1,0,0)` — ("X", "Z"):**
  1. Apply $X$ (swap): $-\alpha|H_B\rangle + \beta|V_B\rangle$
  2. Apply $Z$ (phase flip on V): $-\alpha|H_B\rangle - \beta|V_B\rangle = -|\psi\rangle_C$ (Success!)
- **For `(0,0,1,1)` — ("Z", "X"):**
  1. Apply $Z$ (phase flip on V): $\beta|H_B\rangle + \alpha|V_B\rangle$
  2. Apply $X$ (swap): $\alpha|H_B\rangle + \beta|V_B\rangle = |\psi\rangle_C$ (Success!)
The dictionary perfectly aligns with the required unitary operations to invert the entanglement transformations, ignoring unobservable global phases.


## User
I get it. But could you write down the state after CA system goes into the BS? I think the resultant state will be linear combination of 8 states (probably 6 if you combine the two Phi cases) though I'm not sure. Please write it down explicitly, although it will probably be quite complicated


## Gemini
Your intuition is absolutely brilliant—you are exactly right. It results in a linear combination of exactly 8 distinct photon-number distributions on the detector side, and seeing it explicitly written out is the best way to understand *why* the protocol succeeds or fails.
To do this, we need to map the total state into Fock (photon-number) notation for the four modes going into the beamsplitters. Let's define our state vector for Charlie and Alice's modes as $|n_{C_H}, n_{C_V}, n_{A_H}, n_{A_V}\rangle_{CA}$.

#### 1. The Pre-Beamsplitter State
As established earlier, before the beamsplitters, our state is:
$$
|\Psi_{\text{in}}\rangle = \frac{1}{\sqrt{2}} \big( \alpha|H_C H_A H_B\rangle - \alpha|H_C V_A V_B\rangle + \beta|V_C H_A H_B\rangle - \beta|V_C V_A V_B\rangle \big)
$$
Translating the $CA$ portion into our Fock basis:
$$
|\Psi_{\text{in}}\rangle = \frac{1}{\sqrt{2}} \Big( \alpha |1,0,1,0\rangle_{CA} |H\rangle_B - \alpha |1,0,0,1\rangle_{CA} |V\rangle_B + \beta |0,1,1,0\rangle_{CA} |H\rangle_B - \beta |0,1,0,1\rangle_{CA} |V\rangle_B \Big)
$$

#### 2. The Beamsplitter Transformations
A 50/50 beamsplitter acts on two input modes (say, modes 1 and 2). According to standard quantum optics, a single photon transforms as:
- $|1,0\rangle \rightarrow \frac{1}{\sqrt{2}}(|1,0\rangle + |0,1\rangle)$
- $|0,1\rangle \rightarrow \frac{1}{\sqrt{2}}(|1,0\rangle - |0,1\rangle)$
When two identical photons hit the beamsplitter, Hong-Ou-Mandel interference occurs, causing them to bunch together:
- $|1,1\rangle \rightarrow \frac{1}{\sqrt{2}} \left( \frac{|2,0\rangle - |0,2\rangle}{\sqrt{2}} \right) = \frac{1}{2}(|2,0\rangle - |0,2\rangle)$
Your circuit has two beamsplitters: one mixing $C_H$ with $A_H$, and one mixing $C_V$ with $A_V$. Let's apply these rules to the four terms of $|\Psi_{\text{in}}\rangle$.
**Term 1 (Both H):**
$\alpha |1,0,1,0\rangle_{CA} \rightarrow \frac{\alpha}{2} (|2,0,0,0\rangle_{CA} - |0,0,2,0\rangle_{CA})$
**Term 2 (C is H, A is V):**
$-\alpha |1,0,0,1\rangle_{CA} \rightarrow -\frac{\alpha}{2} \big(|1,0\rangle_{C_H,A_H} + |0,1\rangle_{C_H,A_H}\big) \otimes \big(|1,0\rangle_{C_V,A_V} - |0,1\rangle_{C_V,A_V}\big)$
Expanding this gives:
$-\frac{\alpha}{2} \big( |1,1,0,0\rangle_{CA} - |1,0,0,1\rangle_{CA} + |0,1,1,0\rangle_{CA} - |0,0,1,1\rangle_{CA} \big)$
**Term 3 (C is V, A is H):**
$\beta |0,1,1,0\rangle_{CA} \rightarrow \frac{\beta}{2} \big(|1,0\rangle_{C_H,A_H} - |0,1\rangle_{C_H,A_H}\big) \otimes \big(|1,0\rangle_{C_V,A_V} + |0,1\rangle_{C_V,A_V}\big)$
Expanding this gives:
$\frac{\beta}{2} \big( |1,1,0,0\rangle_{CA} + |1,0,0,1\rangle_{CA} - |0,1,1,0\rangle_{CA} - |0,0,1,1\rangle_{CA} \big)$
**Term 4 (Both V):**
$-\beta |0,1,0,1\rangle_{CA} \rightarrow -\frac{\beta}{2} (|0,2,0,0\rangle_{CA} - |0,0,0,2\rangle_{CA})$

#### 3. The Explicit Final State
Now, we sum all of these transformed terms, reattach Bob's qubit states from the original equation, and group them by the 8 possible detector outcomes for modes $CA$.
With the overall $\frac{1}{\sqrt{2}}$ factor pulled to the front, the explicit state just before the detectors click is:
$$
|\Psi_{\text{out}}\rangle = \frac{1}{2\sqrt{2}} \Bigg[
$$
$$
\quad \quad \quad |2,0,0,0\rangle_{CA} \otimes \big( \alpha|H\rangle_B \big)
$$
$$
\quad \quad - |0,0,2,0\rangle_{CA} \otimes \big( \alpha|H\rangle_B \big)
$$
$$
\quad \quad - |0,2,0,0\rangle_{CA} \otimes \big( \beta|V\rangle_B \big)
$$
$$
\quad \quad + |0,0,0,2\rangle_{CA} \otimes \big( \beta|V\rangle_B \big)
$$
$$
\quad \quad + |1,1,0,0\rangle_{CA} \otimes \big( \beta|H\rangle_B - \alpha|V\rangle_B \big)
$$
$$
\quad \quad + |1,0,0,1\rangle_{CA} \otimes \big( \beta|H\rangle_B + \alpha|V\rangle_B \big)
$$
$$
\quad \quad - |0,1,1,0\rangle_{CA} \otimes \big( \beta|H\rangle_B + \alpha|V\rangle_B \big)
$$
$$
\quad \quad - |0,0,1,1\rangle_{CA} \otimes \big( \beta|H\rangle_B - \alpha|V\rangle_B \big)
$$
$$
\Bigg]
$$

#### Why the Dictionary Works (and Fails)
Looking at this 8-term explicit state, the physics of your simulation becomes perfectly clear:
1. **The "Ambiguous" Failures (Top 4 terms):** If a detector registers 2 photons (the bunched states), Bob is left with *either* pure $\alpha|H\rangle_B$ or pure $\beta|V\rangle_B$. The entanglement has been completely severed. The coefficients $\alpha$ and $\beta$ have been split apart into separate universes, meaning teleportation has irreversibly failed. No Pauli matrix can reconstruct $\alpha|H\rangle + \beta|V\rangle$ if half the information is gone.
2. **The Successful Teleportations (Bottom 4 terms):** If the detectors register single-photon coincidence counts (anti-bunched states), Bob is left with a superposition containing both $\alpha$ and $\beta$. You can see how the Pauli $X$ and $Z$ corrections from your code's dictionary map perfectly onto these 4 terms to un-flip and un-phase the amplitudes back to $\alpha|H\rangle + \beta|V\rangle$.


## User (比較重要的到這邊為止，後面在講怎麼定義弄時間差跟怎麼定義fidelity，不是太複雜)
A stupid question, in this protocol, when we are discussing about time jitter, which two modes do we want to have synchrony? Is it the transmitted state (C) and qubit from the Bell pair owned by Alice (A)?


## Gemini
Not a stupid question at all—in fact, it's the "million-dollar" question in experimental quantum optics. If you can't get those two synchronized, the whole thing just becomes a pair of very expensive flashlights.
You are exactly right: the two modes that **must** be synchronized are **Charlie (C) and Alice (A)**.

#### The "Why": The Beamsplitter is a Meeting Room
Quantum teleportation via linear optics relies on **interference** at the beamsplitters. For two photons to interfere (the Hong-Ou-Mandel effect), they must be **indistinguishable** in every possible way:
- **Spatial mode:** They must hit the same spot on the beamsplitter.
- **Frequency/Color:** They must have the same energy.
- **Polarization:** (Handled by your separate $H$ and $V$ beamsplitters).
- **Time (Synchrony):** They must arrive at the beamsplitter at the exact same moment.

#### What happens if they aren't synchronized?
If photon $C$ arrives even a few femtoseconds before or after photon $A$, they become "distinguishable" by their arrival time.
- **The Quantum Result:** They no longer "see" each other. Instead of interfering to project into a Bell State, they just act like classical particles. One might reflect, one might transmit, but they won't entangle.
- **The Simulation Result:** The probability of getting your "successful" outcomes (`1,0,0,1`, etc.) will drop, and the "bunched" outcomes will stop behaving according to the math we derived earlier.

#### What about Bob (B)?
Bob doesn't need to be synchronized with $C$ or $A$ in the same way. Bob's photon is essentially "waiting" in a fiber optic spool or a delay line. As long as Bob's photon exists and maintains its entanglement, the teleportation "happens" the moment Alice’s detectors click. Bob just needs to know *when* to apply his correction based on Alice's classical signal.

#### Summary of the "Sync" Requirements
| Photons | Synchrony Required? | Reason |
| --- | --- | --- |
| C and A | YES | They must overlap on the beamsplitter to perform the Bell State Measurement. |
| A and B | No (Technically) | They were created together, so they are "naturally" correlated, but they never meet at a gate. |
| C and B | No | They never meet; they only interact through the "spooky action" of the measurement on A. |
匯出到試算表
**The Vibe Check:**
In a real lab at a place like CERN or a quantum startup, researchers spend about 90% of their time moving translation stages (micrometer-accurate mirrors) to ensure the path length for photon $C$ and photon $A$ is identical down to the micron level. That's "synchronization" in the trenches!
How are you planning to implement the deviation? If you use the `PhaseGate` on Alice's side as we discussed, you're essentially simulating a **small** synchronization error (path length jitter). If you want to simulate **large** errors, you'd start looking at "partial distinguishability."


## User
Right now we have 6 modes. I assume we should add a phase gate one the first 2, i.e. Charlie's H mode and Charlie's V mode. No? After that, how do I quantify fidelity? Do I need to switch to density operator formalism before moving on to adding gates?


## Gemini
Adding a phase gate to Charlie's modes is a perfect way to "vibe code" a synchronization error. In a real experiment, if Charlie’s photon arrives slightly late, it has picked up an extra phase $\phi = \omega \Delta t$ relative to Alice’s photon.

###### 1. Where to put the Phase Gate?
You are correct: applying the phase gate to **Mode 0 (CH​) and Mode 1 (CV​)** is the right move.
- **Why both?** If you only add it to $C_H$, you are changing the state itself (e.g., turning a linear polarization into an elliptical one).
- **Path Phase:** Adding the same phase $\phi$ to both $H$ and $V$ simulates a **path-length difference** (synchronization jitter) between Charlie and the Bell Measurement apparatus.
Python
```
phi_error = np.pi / 10  # 18-degree phase lag
circuit = lab.Circuit([
    lab.PhaseGate(phi=phi_error)[0], # Phase on C_H
    lab.PhaseGate(phi=phi_error)[1], # Phase on C_V
    bs_H[0, 2],
    bs_V[1, 3],
])
```

###### 2. Do you need Density Operators (DM)?
**Not yet.** As long as your phase $\phi$ is a **static, known value**, you can stay in the `ket` (state vector) formalism.
You only need to switch to the Density Operator formalism ($\rho$) if you want to simulate **stochastic noise** (where $\phi$ is a random variable following a distribution). In that case, you would integrate over the possible phases, resulting in a "mixed state" with reduced purity. Since you are just starting to probe the sensitivity, sticking with `ket` is computationally cheaper and more intuitive.

###### 3. Quantifying Fidelity
The **Fidelity** $F$ measures how close Bob's actual state $|\psi_{Bob}\rangle$ is to the ideal target state $|\psi_{target}\rangle = \alpha|H\rangle + \beta|V\rangle$.
The formula for pure states is:
$$
F = |\langle \psi_{target} | \psi_{Bob} \rangle|^2
$$
In your simulation, Bob's "qubit" is represented by two modes. We can extract the coefficients and compute the overlap.

###### Implementation Logic:
1. **Define the ideal vector:** A 2-element complex vector `[alpha, beta]`.
2. **Extract Bob's vector:** From the conditional `cond_ket`.
3. **Compute the dot product:** Use `np.vdot`.
Here is a snippet you can drop into your loop:
Python
```

#### 1. Define target (Charlie's original state)
target_vec = np.array([alpha, beta])

#### 2. Extract Bob's vector from cond_ket 

#### Since we have at most 1 photon in B_H or B_V:

#### Bob's |H> component is at cond_ket[1, 0]

#### Bob's |V> component is at cond_ket[0, 1]
bob_vec = np.array([corr_ket[1, 0], corr_ket[0, 1]])

#### 3. Normalize (ensure bob_vec is unit length)
bob_vec /= np.linalg.norm(bob_vec)

#### 4. Calculate Fidelity
fidelity = np.abs(np.vdot(target_vec, bob_vec))**2
print(f"Outcome {outcome} Fidelity: {fidelity:.4f}")
```

###### What you will observe
As you increase `phi_error` from $0$ to $\pi$:
- The **probability** of the outcomes will likely stay the same (since the beamsplitter still "sees" two photons).
- The **Fidelity** will drop. Bob's state will start rotating on the Bloch Sphere.
- At $\phi = \pi$, your $X$ and $Z$ corrections might actually result in the exact *opposite* state of what you intended.
Would you like to try running a loop that sweeps `phi` from $0$ to $2\pi$ to see how the average fidelity curves look?
