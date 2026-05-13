# FockSpace_HOM_Dip_Explained

**Source:** [https://gemini.google.com/share/0f3cd1e4dcb7](https://gemini.google.com/share/0f3cd1e4dcb7)
**Created:** 發布時間：2026年5月13日 上午09:52

---


## User
I asked Claude to simulate the HOM dip for pulsed number states, and he even evaluated the analytic form for me: 
 def coincidence_analytic(tau, N): 
     """P_coinc(τ) = ½ [1 − D_N(Δω τ)²/(N+1)²].   No carrier dependence.""" 
     D = dirichlet_kernel(DELTA_OMEGA * tau, N) 
     return 0.5 * (1.0 - (D / (N + 1)) ** 2) 
 #### -------------------------------------------------------------------- 
 #### Mr Mustard simulation (explicit Fock-state propagation) 
 #### -------------------------------------------------------------------- 
 def coincidence_mrmustard(tau, N, cutoff=3): 
     """Coincidence probability via direct Fock-space evaluation. 
     Builds the 2(N+1)-mode two-photon ket, applies a per-mode delay phase 
     on the second beam (Rgate), then a 50/50 BS for each (signal-k, 
     reference-k) frequency pair, and reads joint photon-number probabilities 
     at the requested cutoff.  Output modes can hold up to 2 photons (HOM 
     bunching when both photons share a frequency), so cutoff ≥ 3. 
     """ 
     omegas = mode_frequencies(N) 
     M = len(omegas)             # N+1 modes per beam 
     N_total = 2 * M 
     state = lab.State(ket=two_beam_input_ket(N, mode_cutoff=cutoff)) 
     ops = [] 
     #### Delay on the reference beam 
     for k in range(M): 
         ops.append(lab.Rgate(angle=float(omegas[k] * tau))[M + k]) 
     #### 50/50 BS coupling each frequency pair 
     for k in range(M): 
         ops.append(lab.BSgate(theta=np.pi / 4)[k, M + k]) 
     out = state >> lab.Circuit(ops) 
     probs = np.asarray(out.fock_probabilities(cutoffs=[cutoff] * N_total)) 
     #### Total photons = 2 (BS conserves number), so 
     ####   P_coinc = 1 − P(both photons at A) − P(both at B) 
     ####          = 1 − P(n_B_total = 0) − P(n_A_total = 0) 
     idx = np.indices(probs.shape) 
     nA_total = idx[:M].sum(axis=0) 
     nB_total = idx[M:].sum(axis=0) 
     P_no_A = float(probs[nA_total == 0].sum()) 
     P_no_B = float(probs[nB_total == 0].sum()) 
     return 1.0 - P_no_A - P_no_B 
 (The second function is the actual simulation. It then created plots to show that they're the same) 
 Could you explain why the analytic for looks like that? We didn't use Gaussian amplitude, but evenly spaced modes, as you could see in the definition of `two_beam_input_ket`: 
 def single_beam_pulse_ket(N, mode_cutoff): 
     """One-photon wavepacket  |ψ⟩ = Σ_k (1/√M) a†_k |0⟩  on M = N+1 modes. 
     Sized at the *output* cutoff (≥ 3, never just 2): the input only fills 
     the n=1 slots, but the BS can bunch both photons into one mode (n=2) 
     and those slots must already exist in the Fock space the state is 
     defined on — otherwise mrmustard silently truncates that mass and the 
     coincidence rate comes out inflated by 1/(N+1). 
     """ 
     M = N + 1 
     c = 1.0 / np.sqrt(M) 
     ket = np.zeros((mode_cutoff,) * M, dtype=complex) 
     for k in range(M): 
         idx = [0] * M 
         idx[k] = 1 
         ket[tuple(idx)] = c 
     return ket 
 def two_beam_input_ket(N, mode_cutoff): 
     """Tensor product of two identical one-photon wavepackets.""" 
     psi = single_beam_pulse_ket(N, mode_cutoff) 
     return np.tensordot(psi, psi, axes=0)


## Gemini
That is a brilliant approach to explicitly simulating the Hong-Ou-Mandel (HOM) effect in Fock space!
To understand why the analytic form uses the **Dirichlet kernel** instead of the standard Gaussian dip, we have to look at the mathematical relationship between a photon's spectral amplitude and the HOM coincidence probability.
Here is the step-by-step breakdown of exactly where that equation comes from.

#### 1. The General HOM Formula
For two identical photons entering a 50:50 beam splitter, the probability of them leaving out of different ports (a coincidence) is determined by the absolute square of their wavefunction overlap.
If we delay one photon by a time $\tau$, the coincidence probability is given by the standard formula:
$$
P_{\text{coinc}}(\tau) = \frac{1}{2} \left( 1 - |\gamma(\tau)|^2 \right)
$$
where $\gamma(\tau)$ is the inner product (the overlap integral) of the two single-photon wavepackets.

#### 2. Defining the "Boxcar" Frequency Comb
In your `single_beam_pulse_ket` function, you aren't using a continuous Gaussian amplitude. Instead, you are placing the photon in an equal superposition of $M = N + 1$ discrete, evenly spaced frequency modes.
Mathematically, the creation operator for your single-photon wavepacket is:
$$
A^\dagger = \frac{1}{\sqrt{N+1}} \sum_{k=0}^{N} a_k^\dagger
$$
The frequencies of these modes are evenly spaced by $\Delta\omega$, so the frequency of the $k$-th mode is $\omega_k = \omega_0 + k\Delta\omega$.

#### 3. Applying the Time Delay
When you apply the delay `tau` to the reference beam (via the `Rgate` in your simulation), each frequency mode picks up a phase shift proportional to its frequency. The delayed photon's creation operator becomes:
$$
B^\dagger(\tau) = \frac{1}{\sqrt{N+1}} \sum_{k=0}^{N} e^{i \omega_k \tau} b_k^\dagger
$$

#### 4. Evaluating the Overlap (Where the Dirichlet Kernel Appears)
Now, we calculate the overlap $\gamma(\tau)$ between the unshifted photon and the delayed photon. Because the modes are discrete and orthogonal, the overlap is just the sum of the products of their probability amplitudes:
$$
\gamma(\tau) = \sum_{k=0}^{N} \left( \frac{1}{\sqrt{N+1}} \right)^* \left( \frac{1}{\sqrt{N+1}} e^{i \omega_k \tau} \right)
$$
$$
\gamma(\tau) = \frac{1}{N+1} \sum_{k=0}^{N} e^{i (\omega_0 + k\Delta\omega) \tau}
$$
We can factor out the global phase from the base frequency $\omega_0$:
$$
\gamma(\tau) = \frac{e^{i \omega_0 \tau}}{N+1} \sum_{k=0}^{N} \left( e^{i \Delta\omega \tau} \right)^k
$$
The sum inside this equation is a standard geometric series of the form $\sum r^k$. Evaluating this geometric series yields:
$$
\sum_{k=0}^{N} \left( e^{i \Delta\omega \tau} \right)^k = \frac{1 - e^{i (N+1) \Delta\omega \tau}}{1 - e^{i \Delta\omega \tau}}
$$
By factoring out half-phases from the numerator and denominator, this beautifully simplifies into a ratio of sine functions:
$$
\gamma(\tau) = \frac{e^{i \omega_0 \tau}}{N+1} e^{i N \Delta\omega \tau / 2} \frac{\sin\left((N+1) \frac{\Delta\omega \tau}{2}\right)}{\sin\left(\frac{\Delta\omega \tau}{2}\right)}
$$

#### 5. Bringing It Together
Remember that the HOM dip depends on the *absolute square* of this overlap:
$$
|\gamma(\tau)|^2 = \frac{1}{(N+1)^2} \left[ \frac{\sin\left((N+1) \frac{\Delta\omega \tau}{2}\right)}{\sin\left(\frac{\Delta\omega \tau}{2}\right)} \right]^2
$$
The function inside the brackets—$\frac{\sin((N+1)x/2)}{\sin(x/2)}$—is known in signal processing and Fourier analysis as the **Dirichlet kernel** (often denoted $D_N(x)$) or the discrete sinc function.
Substituting this back into the general HOM formula gives you the exact analytic expression you saw:
$$
P_{\text{coinc}}(\tau) = \frac{1}{2} \left[ 1 - \frac{D_N(\Delta\omega \tau)^2}{(N+1)^2} \right]
$$

#### Summary: Boxcar vs. Gaussian
In short, the analytic form looks like this because the HOM dip shape is essentially the squared Fourier transform of the photon's power spectrum.
- A **continuous Gaussian** spectrum Fourier-transforms into a **Gaussian** dip.
- A **continuous square** (boxcar) spectrum Fourier-transforms into a **sinc-squared** dip.
- A **discrete, evenly spaced** (comb) spectrum—which is what your code builds—Fourier-transforms into a **Dirichlet-squared** dip (which is simply the periodic, discrete equivalent of a sinc function).


## User
Can you first show me how the coincidence probability for one single photon mode, when one of the input beam has a phase delay?


## Gemini
To understand how the pulse simulation works, it helps to look at the simplest possible case: two photons in a **single, identical frequency mode**, where one has a phase delay $\phi$.

#### 1. The Input State
We start with one photon in mode $a$ and one photon in mode $b$.
$$
|\psi_{\text{in}}\rangle = a^\dagger b^\dagger |0,0\rangle
$$
When we apply a phase delay (like the `Rgate` in your code) to beam $b$, the creation operator transforms as $b^\dagger \to e^{i\phi} b^\dagger$. The state becomes:
$$
|\psi_{\text{delayed}}\rangle = e^{i\phi} a^\dagger b^\dagger |0,0\rangle
$$

#### 2. The Beam Splitter Transformation
A 50/50 beam splitter (BS) mixes the input modes $a$ and $b$ to produce output modes $c$ and $d$. Following the convention used in your simulation:
- $a^\dagger \to \frac{1}{\sqrt{2}}(c^\dagger + d^\dagger)$
- $b^\dagger \to \frac{1}{\sqrt{2}}(-c^\dagger + d^\dagger)$

#### 3. Expanding the Output State
Substituting these into our delayed state, we get:
$$
|\psi_{\text{out}}\rangle = \frac{e^{i\phi}}{2} (c^\dagger + d^\dagger)(-c^\dagger + d^\dagger) |0,0\rangle
$$
Expanding the product of the operators:
$$
|\psi_{\text{out}}\rangle = \frac{e^{i\phi}}{2} \left[ -c^\dagger c^\dagger + c^\dagger d^\dagger - d^\dagger c^\dagger + d^\dagger d^\dagger \right] |0,0\rangle
$$

#### 4. The "Magic" of Destructive Interference
In quantum mechanics, the order of these creation operators doesn't matter for different modes ($c^\dagger d^\dagger = d^\dagger c^\dagger$). This leads to a perfect cancellation of the coincidence terms:
- The term $(c^\dagger d^\dagger)$ represents one photon in each port.
- The term $(- d^\dagger c^\dagger)$ represents the other way to get one photon in each port.
Because they have opposite signs, they sum to zero. The state simplifies to:
$$
|\psi_{\text{out}}\rangle = \frac{e^{i\phi}}{2} \left[ -(c^\dagger)^2 + (d^\dagger)^2 \right] |0,0\rangle
$$
Converting back to state notation:
$$
|\psi_{\text{out}}\rangle = \frac{e^{i\phi}}{\sqrt{2}} \left[ -|2,0\rangle + |0,2\rangle \right]
$$

#### 5. The Coincidence Probability
The probability of measuring one photon in each output ($P_{\text{coinc}}$) is the overlap with the $|1,1\rangle$ state:
$$
P_{\text{coinc}} = |\langle 1,1 | \psi_{\text{out}} \rangle|^2 = 0
$$

#### Key Insight
For a **single mode**, the phase delay $\phi$ is just a global phase. As long as the photons remain in the same spectral mode, they are perfectly **indistinguishable**, and the coincidence probability is always zero.
The "dip" you see in your multi-mode simulation only appears because the delay $\tau$ is applied to a **pulse**. In the pulse case, the phase shift is frequency-dependent ($\phi_k = \omega_k \tau$). This causes the different frequency components to get "out of sync," effectively making the two photons **distinguishable** in time. When they are distinguishable, the destructive interference described above fails, and $P_{\text{coinc}}$ rises from 0 back toward $0.5$.


## User
Can you then consider two single photon mode and evaluate the coincidence probability again when one beam is delayed? Please explicitly do the calculation by transforming the creation operators.


## Gemini
Let's get our hands dirty with the algebra. This is where we see the "dip" actually emerge from the interference of cross-terms between different frequencies.

#### 1. The Setup
We have two frequency modes per beam, $\omega_1$ and $\omega_2$ (where $\omega_2 = \omega_1 + \Delta\omega$).
Following your `single_beam_pulse_ket` logic for $N=1$ ($M=2$ modes), the input states for beams $A$ and $B$ are:
$$
|\psi\rangle_A = \frac{1}{\sqrt{2}}(a_1^\dagger + a_2^\dagger)|0\rangle, \quad |\psi\rangle_B = \frac{1}{\sqrt{2}}(b_1^\dagger + b_2^\dagger)|0\rangle
$$
The total input state is the tensor product:
$$
|\Psi_{\text{in}}\rangle = \frac{1}{2}(a_1^\dagger + a_2^\dagger)(b_1^\dagger + b_2^\dagger)|0\rangle
$$

#### 2. The Delay and Beam Splitter Transformations
We apply the delay $\tau$ to beam $B$. Each mode picks up a phase $e^{i\omega_k \tau}$:
$$
b_1^\dagger \to e^{i\omega_1 \tau} b_1^\dagger, \quad b_2^\dagger \to e^{i\omega_2 \tau} b_2^\dagger
$$
Then, the 50/50 beam splitter couples each frequency pair $(a_k, b_k)$ to output modes $(c_k, d_k)$:
$$
a_k^\dagger \to \frac{1}{\sqrt{2}}(c_k^\dagger + d_k^\dagger), \quad b_k^\dagger \to \frac{1}{\sqrt{2}}(-c_k^\dagger + d_k^\dagger)
$$

#### 3. Transforming the Total State
Substitute these into the input state. To keep it clean, let's factor out a $\frac{1}{\sqrt{2}}$ from every operator:
$$
|\Psi_{\text{out}}\rangle = \frac{1}{4} \underbrace{\left[ (c_1^\dagger + d_1^\dagger) + (c_2^\dagger + d_2^\dagger) \right]}_{\text{Beam A}} \cdot \underbrace{\left[ e^{i\omega_1 \tau}(-c_1^\dagger + d_1^\dagger) + e^{i\omega_2 \tau}(-c_2^\dagger + d_2^\dagger) \right]}_{\text{Beam B}} |0\rangle
$$
Now we expand the product. We are only interested in **coincidence terms** (terms that have exactly one $c$ photon and one $d$ photon).
- **Same-frequency pairs (c1​,d1​) and (c2​,d2​):**
Just like the single-mode case, these cancel out exactly:
$e^{i\omega_1 \tau}(c_1^\dagger d_1^\dagger - d_1^\dagger c_1^\dagger) = 0$
$e^{i\omega_2 \tau}(c_2^\dagger d_2^\dagger - d_2^\dagger c_2^\dagger) = 0$
- **Cross-frequency pairs (c1​,d2​) and (c2​,d1​):**
These do **not** cancel! Let's collect them:
$|\Psi_{\text{coinc}}\rangle = \frac{1}{4} \left[ e^{i\omega_2 \tau} c_1^\dagger d_2^\dagger - e^{i\omega_1 \tau} d_2^\dagger c_1^\dagger + e^{i\omega_1 \tau} c_2^\dagger d_1^\dagger - e^{i\omega_2 \tau} d_1^\dagger c_2^\dagger \right] |0\rangle$
Grouping by the output states $|1_1, 1_2\rangle_{cd}$ (one photon of freq 1 in port $c$, one of freq 2 in port $d$):
$$
|\Psi_{\text{coinc}}\rangle = \frac{1}{4} \left[ (e^{i\omega_2 \tau} - e^{i\omega_1 \tau}) c_1^\dagger d_2^\dagger + (e^{i\omega_1 \tau} - e^{i\omega_2 \tau}) c_2^\dagger d_1^\dagger \right] |0\rangle
$$

#### 4. Calculating the Probability
The probability $P_{\text{coinc}}$ is the sum of the squared magnitudes of these coefficients:
$$
P_{\text{coinc}} = \frac{1}{16} \left( |e^{i\omega_2 \tau} - e^{i\omega_1 \tau}|^2 + |e^{i\omega_1 \tau} - e^{i\omega_2 \tau}|^2 \right)
$$
Focusing on one term:
$$
|e^{i\omega_2 \tau} - e^{i\omega_1 \tau}|^2 = |e^{i\omega_1 \tau}(e^{i\Delta\omega \tau} - 1)|^2 = |e^{i\Delta\omega \tau} - 1|^2
$$
Using the identity $|e^{ix} - 1|^2 = 2 - 2\cos(x)$, we get:
$$
P_{\text{coinc}} = \frac{1}{16} \left( [2 - 2\cos(\Delta\omega \tau)] + [2 - 2\cos(\Delta\omega \tau)] \right)
$$
$$
P_{\text{coinc}}(\tau) = \frac{1}{4} (1 - \cos(\Delta\omega \tau))
$$

#### 5. Verification with the Dirichlet Form
Does this match the general formula $P_{\text{coinc}} = \frac{1}{2} [ 1 - (\frac{D_N}{N+1})^2 ]$?
For $N=1$ ($M=2$ modes), the Dirichlet kernel is $D_1(x) = \frac{\sin(x)}{\sin(x/2)} = 2\cos(x/2)$.
Plugging this in:
$$
P_{\text{coinc}} = \frac{1}{2} \left[ 1 - \left(\frac{2\cos(\Delta\omega \tau / 2)}{2}\right)^2 \right] = \frac{1}{2} [ 1 - \cos^2(\Delta\omega \tau / 2) ]
$$
Using the double-angle identity $\cos^2(\theta) = \frac{1 + \cos(2\theta)}{2}$:
$$
P_{\text{coinc}} = \frac{1}{2} \left[ 1 - \frac{1 + \cos(\Delta\omega \tau)}{2} \right] = \frac{1}{2} \left[ \frac{2 - 1 - \cos(\Delta\omega \tau)}{2} \right] = \frac{1}{4} (1 - \cos(\Delta\omega \tau))
$$
It's a perfect match. The "dip" is essentially the result of the two frequency modes beating against each other as you change the delay.
Would you like to see how this evolves as we add more modes, or are you curious about how the "width" of this dip scales with $N$?