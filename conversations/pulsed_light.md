## User
Mathematically, how do you describe a pulsed coherent state? If possible, write down such state and evaluate $\langle E(r,t) \rangle$, the expectation value of E field, to show that it is indeed a pulsed coherent state.


## Gemini
A single-mode coherent state represents a continuous-wave (CW) laser with a perfectly defined frequency. However, to describe a **pulsed coherent state**, we must move to a **multimode** description, as a pulse is essentially a superposition of many frequency modes (a wave packet).

#### 1. The Mathematical State
A pulsed coherent state $|\psi_{pulse}\rangle$ is defined as a product of coherent states for every possible mode $k$:
$$
|\psi_{pulse}\rangle = \bigotimes_k |\alpha_k\rangle
$$
This can be written more elegantly using the multimode displacement operator acting on the vacuum state $|0\rangle$:
$$
|\psi_{pulse}\rangle = \exp\left( \sum_k (\alpha_k \hat{a}_k^\dagger - \alpha_k^* \hat{a}_k) \right) |0\rangle
$$
In this expression:
- $\hat{a}_k^\dagger$ and $\hat{a}_k$ are the creation and annihilation operators for the mode with wavevector $k$ and frequency $\omega_k$.
- $\alpha_k$ is the complex amplitude of the coherent state in mode $k$. To form a pulse, these amplitudes $\alpha_k$ are not random; they follow a spectral distribution (like a Gaussian) centered around a carrier frequency $\omega_0$.

#### 2. The Electric Field Operator
The quantized electric field operator $\hat{E}(\mathbf{r}, t)$ is the sum of its positive and negative frequency components:
$$
\hat{E}(\mathbf{r}, t) = \hat{E}^{(+)}(\mathbf{r}, t) + \hat{E}^{(-)}(\mathbf{r}, t)
$$
For a 1D field traveling along the $z$-axis, the positive frequency component is:
$$
\hat{E}^{(+)}(z, t) = i \sum_k \sqrt{\frac{\hbar \omega_k}{2 \epsilon_0 V}} \hat{a}_k e^{i(k z - \omega_k t)}
$$

#### 3. Evaluating the Expectation Value ⟨E(z,t)⟩
To show this represents a pulse, we calculate the expectation value of the field. Since $|\psi_{pulse}\rangle$ is an eigenstate of the annihilation operator $\hat{a}_k$ (i.e., $\hat{a}_k |\alpha_k\rangle = \alpha_k |\alpha_k\rangle$), we find:
$$
\langle \hat{E}^{(+)}(z, t) \rangle = \langle \psi_{pulse} | \hat{E}^{(+)}(z, t) | \psi_{pulse} \rangle = i \sum_k \sqrt{\frac{\hbar \omega_k}{2 \epsilon_0 V}} \alpha_k e^{i(k z - \omega_k t)}
$$
The total field expectation value is:
$$
\langle \hat{E}(z, t) \rangle = 2 \text{Re} \left[ i \sum_k \mathcal{E}_k \alpha_k e^{i(k z - \omega_k t)} \right]
$$
where $\mathcal{E}_k = \sqrt{\frac{\hbar \omega_k}{2 \epsilon_0 V}}$ is the "field per photon" for mode $k$.

#### 4. Why this is a "Pulse"
To see the pulse shape, assume the amplitudes $\alpha_k$ follow a Gaussian distribution centered at $k_0$ with width $\Delta k$:
$$
\alpha_k \propto e^{-\frac{(k - k_0)^2}{4 (\Delta k)^2}}
$$
When you perform the summation (or integral in the limit of a large volume), the result is a product of a **carrier wave** and an **envelope**:
$$
\langle E(z, t) \rangle \approx E_0 \underbrace{e^{-(\Delta k)^2 (z - v_g t)^2}}_{\text{Pulse Envelope}} \cos(k_0 z - \omega_0 t + \phi)
$$

#### Conclusion
The evaluation shows that:
1. **Coherent Nature:** The expectation value $\langle E \rangle$ is non-zero and oscillates, behaving like a classical field (unlike a Fock state $|n\rangle$ where $\langle E \rangle = 0$).
2. **Pulsed Nature:** Because it is multimode, the field is localized in space and time. The envelope moves at the group velocity $v_g$, ensuring that photons arrive in a synchronized "coincidence" window rather than randomly over time.

## User (註：這對話不是很重要但你還是可以看一下，實際上不是用coherent，你可以跳到下一個)
Is it possible to simulate the output of two pulsed coherent light hitting a beam splitter? I think we could let the input state be, as you mentioned, $\sum_k \ket{\alpha}_k$ and the other one similarly, too. Just not sure how to pose a distance difference, but through this we could change the distribution of $\alpha$ easily. By changing the distribution of $\alpha$, perhaps through $\delta k$, we could simulate the effect of how pulse width affect coincidence. 
 If Mrmustard is not good at this, using qutip or other packages is fine too. What do you think?


## Gemini
It is absolutely possible to simulate this. Since you are dealing with coherent states, you have a major computational advantage: coherent states are **Gaussian states**. This means you can avoid the "curse of dimensionality" found in Fock-space simulations (like those typically done in QuTiP) and use phase-space methods instead.

###### 1. Modeling the "Distance Difference"
In a pulsed system, a distance difference $\Delta z$ (or temporal delay $\Delta t = \Delta z / c$) is mathematically equivalent to a frequency-dependent phase shift.
If your pulse $A$ has amplitudes $\alpha_k$, then Pulse $B$ with a delay $\Delta z$ will have amplitudes:
$$
\beta_k(\Delta z) = \beta_k(0) e^{i k \Delta z}
$$
Alternatively, in the time domain, if $f(t)$ is your pulse envelope, the delayed pulse is $f(t - \Delta t)$. When you perform the simulation, you define your modes $k$ and shift the complex amplitudes $\alpha_k$ according to the Fourier transform of the delayed envelope.

###### 2. Choosing the Tool: MrMustard vs. QuTiP
| Feature | MrMustard | QuTiP |
| --- | --- | --- |
| Logic | Phase Space (Gaussian) | Hilbert Space (Fock) |
| Scaling | Excellent. Handles hundreds of modes easily. | Poor. 10 modes with a cutoff of 10 photons is 1010 dimensions. |
| Pulsed States | Native support for multimode Gaussian optics. | Requires manual tensor product management. |
| Complexity | High-level (easy to define beam splitters). | Low-level (you build the operators). |
匯出到試算表
**Verdict:** For simulating pulsed coherent light, **MrMustard** is significantly better. It represents the state using a mean vector $\bar{r}$ and a covariance matrix $\mathbf{V}$, which makes simulating a 50-mode pulse as fast as a 1-mode pulse.

###### 3. Simulation Strategy (MrMustard Logic)
To simulate how pulse width ($\delta k$) affects coincidence, you can follow this workflow:

###### A. Define the Spectral Modes
Instead of a single mode, you define a vector of modes $k_1, k_2, \dots, k_n$.
- Set $\alpha_k$ for Source 1 as a Gaussian distribution centered at $k_0$.
- Set $\alpha_k$ for Source 2 as the same distribution, but multiply by $e^{ik \Delta z}$.

###### B. The Beam Splitter Transformation
In MrMustard, a Beam Splitter acts on the modes. Since you have a multimode pulse, the Beam Splitter must act on *pairs* of corresponding modes: $(\text{Mode } k_{1,A}, \text{Mode } k_{1,B})$, $(\text{Mode } k_{2,A}, \text{Mode } k_{2,B})$, etc.

###### C. Measure Coincidence
To find the coincidence, you calculate the photon number expectation value at the output ports. For pulsed coherent states, the mean photon number in the output modes is:
$$
\langle n_{out} \rangle = \sum_k |\alpha_{out, k}|^2
$$

###### 4. Sketch of the Python Logic
If you were to implement this using a Gaussian approach (which is what MrMustard does under the hood), the core logic would look like this:
Python
```
import numpy as np
def simulate_pulse_interference(delta_z, delta_k, k0=100, num_modes=100):
    #### 1. Define k-space
    ks = np.linspace(k0 - 5*delta_k, k0 + 5*delta_k, num_modes)
    #### 2. Define Spectral Amplitudes (Gaussian Envelopes)
    #### Source A (at origin)
    alpha_A = np.exp(-(ks - k0)**2 / (4 * delta_k**2))
    #### Source B (shifted by delta_z)
    alpha_B = np.exp(-(ks - k0)**2 / (4 * delta_k**2)) * np.exp(1j * ks * delta_z)
    #### 3. Apply Beam Splitter (50/50) to each mode k
    #### Output Port 1: (A + B) / sqrt(2)
    #### Output Port 2: (A - B) / sqrt(2)
    out1 = (alpha_A + alpha_B) / np.sqrt(2)
    out2 = (alpha_A - alpha_B) / np.sqrt(2)
    #### 4. Total Intensity (Proportional to Detectable Photons)
    intensity1 = np.sum(np.abs(out1)**2)
    intensity2 = np.sum(np.abs(out2)**2)
    return intensity1, intensity2
```

###### Why this works for your Goal
By varying `delta_z` in the loop above, you will see the **interference fringes**.
- If `delta_k` is small (long pulse in time), the interference fringes will persist over a long `delta_z`.
- If `delta_k` is large (short pulse in time), the interference will vanish quickly as `delta_z` increases, because the pulses no longer overlap in the time domain.
This perfectly simulates the temporal "coincidence window" you were asking about. Would you like to see how to translate this into a specific MrMustard `Circuit` or `State` object?


## User
I just realized, if we input a pair of coherent states into a beam splitter, the output state is also a separable pair of coherent states with different displacement values. This simulation is actually trivial.  
 This gets me concerned. So we're not allowed to use coherent states (for the teleported qubit. Instead of $\alpha \ket{H} + \beta \ket{V}$, use a coherent version of this) in quantum teleportation? If that's the case, let's say the state to be teleported is $\ket{H}$. How do we generate a pulsed number state of ${H}$? Is it even doable experimentally?


## Gemini
You are absolutely correct. One of the "hidden" hurdles in learning quantum optics is realizing that while coherent states look like classical waves, they are "too classical" for standard Bell State Measurements (BSM).
If you use two coherent states $|\alpha\rangle$ and $|\beta\rangle$ at a 50/50 beam splitter, the output is indeed the separable state $|\frac{\alpha+\beta}{\sqrt{2}}\rangle \otimes |\frac{\alpha-\beta}{\sqrt{2}}\rangle$. There is no entanglement created, and no "projection" occurs that can facilitate teleportation. To teleport a qubit, you generally need **non-Gaussian** states, specifically single-photon (Fock) states.

#### 1. Why Coherent States Fail Teleportation
As shown in your reference **1000000972.jpg**, coherent light is "random" and has a second-order coherence of $g^{(2)}(0) = 1$.
- **The Poissonian Problem:** A coherent state $|\alpha\rangle$ is a superposition of all possible photon numbers $|0\rangle, |1\rangle, |2\rangle, \dots$.
- **Indistinguishability:** In a BSM, you need to know that exactly *one* photon came from each port to identify the Bell state. With coherent states, you might have zero photons, or three, or five, making it impossible to perform a clean projection onto an entangled basis.
- **Antibunching Requirement:** For a successful Hong-Ou-Mandel interference (the heart of BSM), you need the "Antibunched" behavior where $g^{(2)}(0) < 1$.

#### 2. Generating a Pulsed Number State ∣1⟩
Generating a pure single-photon state (a Fock state $|1\rangle$) is one of the most common tasks in an experimental quantum optics lab. It is very much doable, and the standard method is **Heralded Single-Photon Generation** via **Spontaneous Parametric Down-Conversion (SPDC)**.

##### The Experimental Recipe:
1. **The Pump:** Use a pulsed laser (like a Ti:Sapphire) to send high-energy "pump" photons into a non-linear crystal (like BBO or KTP).
2. **The Pair:** Occasionally, a pump photon splits into two lower-energy photons, called the **Signal** and the **Idler**.
3. **The Herald:** Because they are created in pairs, detecting the "Idler" photon at a detector acts as a "herald." It tells you with 100% certainty that there is exactly one "Signal" photon currently traveling down the other path.
4. **The Pulse:** Since the pump laser was pulsed, the resulting single photon is also "contained" within that same temporal pulse window.

#### 3. Representing the State for your Simulation
If you are teleporting a polarization qubit, your "pulsed number state" is not a coherent $\alpha$, but rather a single excitation shared across two modes (Horizontal and Vertical):
$$
|\psi\rangle_{qubit} = c_H \hat{a}_H^\dagger |0\rangle + c_V \hat{a}_V^\dagger |0\rangle = c_H |1,0\rangle + c_V |0,1\rangle
$$
In **QuTiP**, you would represent this using a Fock basis with a small dimensions (e.g., `fock(2, 1)`). In **MrMustard**, because a single photon is a non-Gaussian state, you would define it using the `Fock` state class rather than the `Coherent` state class.

#### 4. Is it Trivial in Simulation?
Unlike coherent states, the simulation of single photons at a beam splitter is **not** trivial.
- When two $|1\rangle$ photons hit a beam splitter, they undergo the **Hong-Ou-Mandel effect**.
- Instead of splitting up, they "bunch" and both exit through the *same* port together (either $|2,0\rangle$ or $|0,2\rangle$).
- They never exit separately ($|1,1\rangle$ is suppressed).
This "suppression of the $|1,1\rangle$ state" is exactly the physical mechanism that allows a Bell State Measurement to work. If you try to simulate this in MrMustard using `Fock(1)` states, you will see the coincidence counts drop to zero at the output, which is the signature you need for your teleportation project.
Since you're looking at pulse widths and $g^{(2)}$, would you like to see how the mathematical form of the SPDC state differs from the coherent pulse we discussed earlier?


## User
I know a single photon state looks like that, but how do we mathematically describe a "pulsed" number state? Is that possible? Would sum over different modes work? I hope that we could modify something like the displacement phase of the coherent state to account for the time delay of one of the pulse and then I could simulate the relation between the output (coincident counts?) vs. the time delay.


## Gemini
Yes, it is absolutely possible to describe a "pulsed" number state mathematically, and your intuition about using a sum over modes is spot on. However, the structure of this state is fundamentally different from the pulsed coherent state we discussed earlier.

#### 1. The Pulsed Single-Photon State
For a coherent pulse, we had a **product** of coherent states across all modes. For a pulsed single-photon state (a Fock state $|1\rangle$), we have a **superposition** where exactly one excitation is shared across all spectral modes.
We define a **wave packet creation operator** $\hat{A}^\dagger$:
$$
\hat{A}^\dagger = \sum_k f(k) \hat{a}_k^\dagger
$$
Where $f(k)$ is the spectral amplitude (the "shape" of your pulse in frequency space), normalized such that $\sum_k |f(k)|^2 = 1$.
The pulsed single-photon state is then:
$$
|\psi_{pulse}\rangle = \hat{A}^\dagger |0\rangle = \sum_k f(k) |1\rangle_k \bigotimes_{j \neq k} |0\rangle_j
$$
In this state, there is exactly one photon in the entire pulse. If you measure the energy, you find one photon; however, that photon is "smeared" across a range of frequencies, which is what gives the pulse its shape and duration in time.

#### 2. Posing a Distance/Time Delay
Just as you suspected, you can account for a time delay $\Delta t$ (or distance $\Delta z = c \Delta t$) by applying a frequency-dependent phase to the spectral distribution.
If the original pulse has the shape $f(k)$, the delayed pulse creation operator $\hat{B}^\dagger$ is:
$$
\hat{B}^\dagger(\Delta z) = \sum_k f(k) e^{i k \Delta z} \hat{a}_k^\dagger
$$

#### 3. Simulating Coincidence vs. Delay (The HOM Dip)
When you let these two pulsed number states hit a beam splitter, you are simulating the **Hong-Ou-Mandel (HOM) effect**. This is the core of the Bell State Measurement you need for your quantum teleportation project.
- **At Δz=0 (Perfect Overlap):** The two photons are perfectly indistinguishable. Because they are bosons, they undergo destructive interference in the "coincidence" channel. They "bunch" and exit the beam splitter together. Your coincident count rate will drop to **zero**.
- **At large Δz (No Overlap):** The photons arrive at different times. The beam splitter can "distinguish" them by their arrival time. They act as independent particles, and you will see a non-zero coincident count rate (the baseline).

#### 4. Implementation in MrMustard or QuTiP
Since you are working with **MrMustard** and **QuTiP** for your final project, here is how to approach the simulation:
- **MrMustard:** You can define a `State` with a single photon excitation using the `Fock` state class. To make it pulsed, you assign this excitation to a "mode" that is actually a collective wave-packet mode. MrMustard is particularly good at this because it can handle the transformation of these wave-packet modes through optical elements like beam splitters quite efficiently.
- **Manual Mode Sum:** If you want to see the "gory details," you can write a loop in Python (similar to the one we discussed for coherent states) but instead of calculating the classical intensity, you calculate the quantum coincidence probability:
  $$
  P_{coinc}(\Delta z) = \langle \psi_{in} | \hat{n}_1 \hat{n}_2 | \psi_{in} \rangle
  $$
where $|\psi_{in}\rangle = \hat{A}^\dagger \hat{B}^\dagger(\Delta z) |0\rangle$.

#### Summary of the Simulation Logic
To see how the **pulse width** affects coincidence, you simply change the width of your spectral distribution $f(k)$:
1. **Narrow f(k) (Wide Pulse):** The HOM dip will be very wide. You need a large $\Delta z$ before the photons stop interfering.
2. **Wide f(k) (Ultrafast Pulse):** The HOM dip will be extremely sharp. This reflects the "Antibunched" nature shown in your notes, where the timing must be precise for the quantum effects to manifest.
This approach allows you to directly plot the "HOM Dip" visibility as a function of the delay $\Delta z$, which is likely a key requirement for your teleportation simulation.


## User
It sounds straightforward and appealing to use mode superposition to represent mode number state. This is my guess too, but could we prove that this is indeed pulsed number state? We are not able to just calculate expectation value of E like coherent state superposition since it's just 0.


## Gemini
You’ve hit on one of the most profound differences between classical and quantum fields. You are absolutely right: for any state with a fixed number of photons (a Fock state), the expectation value of the electric field is zero, $\langle \hat{E} \rangle = 0$. This is because the electric field operator $\hat{a} + \hat{a}^\dagger$ changes the photon number, and states with different photon numbers are orthogonal.
To "see" the pulse in a single-photon state, we don't look at the field itself, but at the **detection probability density** (which classically corresponds to the intensity).

#### 1. The Observable: Intensity/Probability
To prove that $|\psi\rangle = \sum_k f(k) \hat{a}_k^\dagger |0\rangle$ is a pulse, we must evaluate the expectation value of the intensity operator, which is proportional to $\hat{E}^{(-)} \hat{E}^{(+)}$. This represents the probability of detecting a photon at position $z$ and time $t$.
The positive frequency field operator is:
$$
\hat{E}^{(+)}(z, t) = \sum_q \mathcal{E}_q \hat{a}_q e^{i(k_q z - \omega_q t)}
$$
*(Where Eq​ is the field strength per photon for mode q)*.

#### 2. The Proof
We want to calculate $I(z, t) = \langle \psi | \hat{E}^{(-)}(z, t) \hat{E}^{(+)}(z, t) | \psi \rangle$.
**Step 1: Apply E^(+) to the state.**
$$
\hat{E}^{(+)}(z, t) |\psi\rangle = \left( \sum_q \mathcal{E}_q \hat{a}_q e^{i(k_q z - \omega_q t)} \right) \left( \sum_k f(k) \hat{a}_k^\dagger |0\rangle \right)
$$
Using the commutation relation $[\hat{a}_q, \hat{a}_k^\dagger] = \delta_{qk}$, we get:
$$
\hat{E}^{(+)}(z, t) |\psi\rangle = \sum_k \mathcal{E}_k f(k) e^{i(k z - \omega_k t)} |0\rangle
$$
**Step 2: Calculate the Inner Product.**
Now we multiply by the conjugate (the "bra" side):
$$
\langle \psi | \hat{E}^{(-)} \hat{E}^{(+)} | \psi \rangle = \left( \sum_{k'} \mathcal{E}_{k'} f^*(k') e^{-i(k' z - \omega_{k'} t)} \langle 0 | \right) \left( \sum_k \mathcal{E}_k f(k) e^{i(k z - \omega_k t)} |0\rangle \right)
$$
Since $\langle 0 | 0 \rangle = 1$, this collapses into a single absolute square:
$$
I(z, t) \propto \left| \sum_k \mathcal{E}_k f(k) e^{i(k z - \omega_k t)} \right|^2
$$

#### 3. Physical Interpretation
The term inside the absolute square is exactly the **Fourier Transform** of the spectral distribution $f(k)$ (scaled by $\mathcal{E}_k$).
If we assume a narrow-band pulse (where $\mathcal{E}_k$ is roughly constant and $\omega_k \approx \omega_0 + v_g(k - k_0)$), the sum becomes:
$$
I(z, t) \propto | \Psi(z, t) |^2
$$
where $\Psi(z, t)$ is the **spatio-temporal wave packet**:
$$
\Psi(z, t) \approx e^{i(k_0 z - \omega_0 t)} \int f(k) e^{i(k-k_0)(z - v_g t)} dk
$$

#### Why this proves it’s a "Pulse":
1. **Localization:** If $f(k)$ is a Gaussian with width $\Delta k$, then $I(z, t)$ is a Gaussian in space/time with width $\Delta z \sim 1/\Delta k$. It is not spread across all space like a plane wave; it is localized.
2. **Propagation:** The peak of the probability distribution moves at the group velocity $v_g$.
3. **Photon Number:** If you integrate $I(z, t)$ over all space, you get exactly **1**. This confirms it is a single-photon state, but one that is "shaped" into a pulse.

#### Summary
While the **field** expectation $\langle E \rangle$ is zero (meaning there is no well-defined classical phase), the **probability of finding the photon** $\langle \hat{E}^{(-)} \hat{E}^{(+)} \rangle$ follows a localized pulse shape.
This is the mathematical "green light" for your simulation: you can shift the pulse in time by applying $e^{ik \Delta z}$ to $f(k)$, and even though $\langle E \rangle$ stays zero, the **overlap** of these probability envelopes at the beam splitter will correctly produce the Hong-Ou-Mandel dip.
In your code, you won't be tracking fields; you'll be tracking the overlap of these mode-functions $\Psi(z, t)$. Does this clarify why the "sum over modes" approach is physically rigorous for a Fock state?


## User
I know that in classical optics, we could use mode-locking technique to create pulsed laser and from what I have read, we usually assume that the modes are equally spaced (in frequency domain) and have equal amplitudes. For coherent states it's fine to assume that all coherent states $\ket{\alpha}_k$ just have equal $\alpha$, but I'm not sure if it's the same for number states. Could I assume that $f(k)$ is constant over a small interval?


## Gemini
Mathematically, you **can** assume $f(k)$ is constant over a small interval, but it leads to a specific physical pulse shape that differs from the typical Gaussian pulses used in many quantum optics simulations.
In classical mode-locking, assuming equal amplitudes and phases across $N$ modes results in a pulse whose temporal width is inversely proportional to the total bandwidth. For a single-photon state, the same mathematical principles apply to the probability envelope.

#### 1. The "Top-Hat" Distribution
If you assume $f(k)$ is constant over a finite interval centered at $k_0$ with width $\Delta k$:
$$
f(k) = \begin{cases} \frac{1}{\sqrt{\Delta k}} & \text{if } |k - k_0| \le \frac{\Delta k}{2} \\ 0 & \text{otherwise} \end{cases}
$$
This satisfies the normalization condition $\int |f(k)|^2 dk = 1$, ensuring you have exactly one photon in the pulse.

#### 2. Resulting Pulse Shape: The Sinc Pulse
As established in Fourier analysis, the transform of a rectangular (top-hat) function is a **sinc function**. The spatial/temporal profile of the detection probability will be:
$$
I(z, t) \propto \left| \text{sinc}\left( \frac{\Delta k (z - v_g t)}{2} \right) \right|^2
$$
While this is a valid "pulsed" state, it has a few characteristics that might affect your simulation of the Hong-Ou-Mandel (HOM) dip:
- **Side Lobes:** Sinc pulses have "ringing" or side lobes. In a coincidence experiment, this could cause small secondary oscillations in your $g^{(2)}(\tau)$ or coincidence-vs-delay plots.
- **Non-Physicality:** Real-world heralded single-photon sources (like SPDC) typically produce Gaussian spectral profiles due to the pump laser shape and crystal phase-matching conditions.

#### 3. Comparison of Spectral Distributions
If you are simulating this in a package like **MrMustard** or **QuTiP**, it is often more robust to use a Gaussian distribution even for a number state, as it more closely mirrors the "Coherent (random)" or "Antibunched" sources often cited in text.
| Spectral Distribution f(k) | Temporal Shape I(t) | Pros/Cons for Simulation |
| --- | --- | --- |
| Constant (Top-Hat) | Sinc-squared | Easy to define; produces side lobes that may complicate the HOM dip. |
| Gaussian | Gaussian | Most realistic for SPDC sources; smooth decay of coincidences with delay. |
| Lorentzian | Exponential | Represents decay from a single atom; very sharp peak. |
匯出到試算表

#### Summary for your Simulation
You can certainly assume $f(k)$ is constant for your simulation to observe how $\Delta k$ affects the coincidence window. It will show that as you increase the interval (the bandwidth), the coincidence window (the HOM dip) becomes narrower. However, for a high-fidelity quantum teleportation simulation, transitioning to a Gaussian $f(k)$ will likely yield cleaner results that match experimental literature more closely.
Does the prospect of "sinc-shaped" interference patterns change how you want to structure your coincidence detection logic?


## User
I think through our simulation of pulsed single photon states we have a pretty clear basis of how to address the time delay of a beam. Now I want to go back to the quantum teleportation setup. 
 In that setup, a slightly different thing is that instead of two single photon beams, we have one single photon beam with arbitrary polarization (teleported qubit) and a Bell state. I think we could use 2 * (N+1) modes with MrMustard to represent the teleported qubit (each with amplitude $\alpha/\sqrt{N+1}$ or $\beta/\sqrt{N+1}$, but how do we describe a pulsed Bell state? We don't have to address the SPDC conversion part yet, so do you have any ideas?


## Gemini
To move from single-photon interference to a full quantum teleportation simulation, we need to transition from single-excitation wave packets to a two-photon entangled state distributed across multiple modes.
As you noted, a coherent state simulation would be trivial because the states remain separable. For teleportation, we must maintain the "Antibunched" nature of the photons. Using $2(N+1)$ modes for each spatial path is a mathematically sound way to discretize the frequency/temporal window of your pulses.

###### 1. The Mathematical Structure of a Pulsed Bell State
A Bell state is a two-photon state entangled in polarization and spatial path. In a pulsed, multimode framework, this entanglement must also account for the spectral wave packet.
If we choose the $|\Psi^-\rangle$ state (the "singlet" state), the pulsed version is defined by the creator operators for the two photons in paths **2** and **3**:
$$
|\Psi^-\rangle_{pulsed} = \frac{1}{\sqrt{2}} \left( \hat{A}_{2,H}^\dagger \hat{A}_{3,V}^\dagger - \hat{A}_{2,V}^\dagger \hat{A}_{3,H}^\dagger \right) |0\rangle
$$
Expanding this into your discrete modes (where $g(k)$ is your spectral distribution):
$$
|\Psi^-\rangle_{pulsed} = \frac{1}{\sqrt{2}} \sum_{k, q} g(k)g(q) \left( \hat{a}_{2,H,k}^\dagger \hat{a}_{3,V,q}^\dagger - \hat{a}_{2,V,k}^\dagger \hat{a}_{3,H,q}^\dagger \right) |0\rangle
$$
- **Normalization:** For a top-hat distribution where $g(k) = 1/\sqrt{N+1}$, the normalization of the two-photon state is preserved because the double sum over $k$ and $q$ ensures the total probability is $1$.
- **Separability:** Unlike the coherent state, this cannot be factored into two independent pulses. The photons are tied together such that their spectral properties (frequency/arrival time) are correlated alongside their polarization.

###### 2. Mode Mapping in MrMustard
In **MrMustard**, managing these $2(N+1)$ modes per path requires careful indexing. For a three-path teleportation setup (Qubit path 1, Bell-Port 2, Bell-Port 3), you would have a total of $6(N+1)$ modes.
| Path & Polarization | Mode Indices | Description |
| --- | --- | --- |
| Path 1 (H / V) | 0…N / N+1…2N+1 | The pulsed teleported qubit. |
| Path 2 (H / V) | 2N+2…3N+2 / 3N+3…4N+3 | First half of the pulsed Bell pair. |
| Path 3 (H / V) | 4N+4…5N+4 / 5N+5…6N+5 | Second half of the pulsed Bell pair. |
匯出到試算表

###### 3. Defining the Pulsed Bell State for Simulation
Since MrMustard's `State` object can take a `ket` (vector) or `dm` (density matrix), you can construct the Bell state by populating the indices of a high-dimensional tensor.
- **For the teleported qubit (α∣H⟩+β∣V⟩):**
You populate the modes in Path 1. If you use a constant $f(k) = 1/\sqrt{N+1}$, each $H$-mode $k$ gets a value of $\alpha/\sqrt{N+1}$, and each $V$-mode gets $\beta/\sqrt{N+1}$.
- **For the Bell Pair:**
You populate the two-photon sector. Every combination of mode $(k \in \text{Path 2}, q \in \text{Path 3})$ will have a non-zero value. Specifically, the component $(\text{Mode } 2H_k, \text{Mode } 3V_q)$ and $(\text{Mode } 2V_k, \text{Mode } 3H_q)$ will have opposite signs.

###### 4. Addressing Time Delay and Coincidence
To simulate the effect of a time delay on the teleportation fidelity:
1. Apply the phase shift $e^{ik \Delta z}$ to the modes of the **teleported qubit (Path 1)**.
2. The **Bell State Measurement (BSM)** is performed by a 50/50 beam splitter acting on Path 1 and Path 2.
3. **Coincidence Projection:** You measure Path 1 and Path 2 with single-photon detectors. Teleportation is "successful" only when you detect exactly one photon in Path 1 and one in Path 2 (the coincidence window).
Because your Bell state is pulsed, the "overlap" at the BSM beam splitter will naturally depend on $\Delta z$. If the qubit pulse and the Bell pulse are offset, the photons become distinguishable by arrival time, and the BSM will fail to project them into an entangled state. This will result in a decrease in the fidelity of the teleported state at Path 3.

###### Conceptual Logic for your MrMustard Script
In your research code, you can define a helper function to build these "wavepacket" states:
Python
```
def create_pulsed_bell_state(N, spectral_dist):
    #### spectral_dist is a vector of length N+1 (e.g. ones/sqrt(N+1))
    #### Define a zero tensor for the Fock space (limited to 2 photons total)
    #### Populate indices corresponding to Path 2 and Path 3
    #### Apply Psi-minus logic: 1/sqrt(2) * (H2_V3 - V2_H3)
    pass
```
By looping over different `spectral_dist` widths (like the $\delta k$ we discussed earlier), you can directly observe how a shorter pulse makes the teleportation more sensitive to timing jitter. Given your work with **Heisenberg models** and **stochastic series expansion**, this type of discrete mode discretization should feel very familiar to the lattice structures you use in many-body physics.
Do you want to focus on the specific detector projection logic (how to "herald" the success on Path 3) next?


## User
Claude built the input state (including both teleported qubit and Bell pair) based on our conversation. Let's do a cross check. Also, while giving explanation to this, could you write down the mathematical form of the tensor product state explicitly with derivation, so that I could follow the code more easily? Thanks a lot! 
 def _mode_idx(qubit, polarization, freq, M): 
     """Global mode index for (qubit ∈ {C,A,B}, pol ∈ {H,V}, freq ∈ 0..M-1).""" 
     qubit_offset = {"C": 0, "A": 2 * M, "B": 4 * M}[qubit] 
     pol_offset = {"H": 0, "V": M}[polarization] 
     return qubit_offset + pol_offset + freq 
 #### ---------------------------------------------------------------------- 
 #### Input ket builder 
 #### ---------------------------------------------------------------------- 
 def build_input_ket(alpha, beta, N, ca_cutoff=3, b_cutoff=2): 
     """ 
     Build  |Ψ⟩_in = (α|H⟩_C + β|V⟩_C) ⊗ (|HH⟩_AB − |VV⟩_AB) / √2. 
     Mixed cutoffs: C/A modes at ca_cutoff (≥ 3 — BS can bunch both photons 
     into one mode); B modes at b_cutoff (≥ 2 — never modified).  Returns a 
     numpy array of shape (ca_cutoff,)*(4M) + (b_cutoff,)*(2M). 
     """ 
     M = N + 1 
     n_modes = 6 * M 
     shape = (ca_cutoff,) * (4 * M) + (b_cutoff,) * (2 * M) 
     ket = np.zeros(shape, dtype=complex) 
     c_amp = 1.0 / np.sqrt(M) 
     bell_sign = {"H": +1.0, "V": -1.0} 
     base = c_amp ** 3 / np.sqrt(2) 
     for P_C, amp_C in [("H", alpha), ("V", beta)]: 
         for P_AB in ["H", "V"]: 
             sign = bell_sign[P_AB] 
             for k_C in range(M): 
                 for k_A in range(M): 
                     for k_B in range(M): 
                         idx = [0] * n_modes 
                         idx[_mode_idx("C", P_C, k_C, M)] = 1 
                         idx[_mode_idx("A", P_AB, k_A, M)] = 1 
                         idx[_mode_idx("B", P_AB, k_B, M)] = 1 
                         ket[tuple(idx)] = amp_C * sign * base 
     return ket


## Gemini
Claude has built a solid foundation here. The code correctly implements a **multimode discrete Fock state** representation. It treats each frequency and polarization as a distinct spatial mode in the simulation "grid," which is exactly how MrMustard or a high-dimensional QuTiP tensor would process it.
Here is the cross-check of the logic and the formal mathematical derivation.

#### 1. Mathematical Derivation of the Input Ket
To follow the code, we define a **wavepacket creation operator** $\hat{A}^\dagger_{P}$ for a photon in path $A$ with polarization $P \in \{H, V\}$. Since the code assumes a "top-hat" (constant) spectral distribution across $M$ modes, the operator is:
$$
\hat{A}^\dagger_{P} = \sum_{k=0}^{M-1} \frac{1}{\sqrt{M}} \hat{a}^\dagger_{P,k}
$$
Where $\hat{a}^\dagger_{P,k}$ creates a photon in the $k$-th frequency mode of path $A$ with polarization $P$.

##### Step A: The Teleported Qubit (Path C)
The state to be teleported is a single-photon pulse in path $C$ with an arbitrary polarization:
$$
|\psi\rangle_C = \left( \alpha \hat{C}^\dagger_{H} + \beta \hat{C}^\dagger_{V} \right) |0\rangle = \sum_{k_C=0}^{M-1} \frac{1}{\sqrt{M}} \left( \alpha \hat{c}^\dagger_{H,k_C} + \beta \hat{c}^\dagger_{V,k_C} \right) |0\rangle
$$

##### Step B: The Pulsed Bell State (Paths A and B)
The code implements the $|\Phi^-\rangle$ Bell state ($|HH\rangle - |VV\rangle$). In the pulsed multimode framework, this is:
$$
|\Phi^-\rangle_{AB} = \frac{1}{\sqrt{2}} \left( \hat{A}^\dagger_{H}\hat{B}^\dagger_{H} - \hat{A}^\dagger_{V}\hat{B}^\dagger_{V} \right) |0\rangle
$$
Substituting the summations for the operators:
$$
|\Phi^-\rangle_{AB} = \frac{1}{\sqrt{2}} \sum_{k_A=0}^{M-1} \sum_{k_B=0}^{M-1} \frac{1}{M} \left( \hat{a}^\dagger_{H,k_A} \hat{b}^\dagger_{H,k_B} - \hat{a}^\dagger_{V,k_A} \hat{b}^\dagger_{V,k_B} \right) |0\rangle
$$

##### Step C: The Full Tensor Product ∣Ψ⟩in​
The total input state is $|\psi\rangle_C \otimes |\Phi^-\rangle_{AB}$. By combining the sums, we get:
$$
|\Psi\rangle_{in} = \sum_{k_C, k_A, k_B} \frac{1}{\sqrt{2} M^{3/2}} \left( \alpha \hat{c}^\dagger_{H,k_C} + \beta \hat{c}^\dagger_{V,k_C} \right) \left( \hat{a}^\dagger_{H,k_A} \hat{b}^\dagger_{H,k_B} - \hat{a}^\dagger_{V,k_A} \hat{b}^\dagger_{V,k_B} \right) |0\rangle
$$
This expands into four main terms (two for $\alpha$ and two for $\beta$), which is exactly what the nested loops in `build_input_ket` are doing.

#### 2. Code Cross-Check & Verification
The code's logic is a bit like packing a very organized suitcase—making sure every photon lands in its specific frequency "pocket."
- **Normalization Check:**
The code sets the amplitude to `base = (1/\sqrt{M})^3 / \sqrt{2}`.
For a fixed set of polarizations, there are $M^3$ possible frequency combinations.
The sum of the squares for one polarization branch is: $M^3 \times \left| \frac{1}{\sqrt{2}M^{3/2}} \right|^2 = \frac{M^3}{2M^3} = 1/2$.
Since the Bell state has two branches ($HH$ and $VV$), the total norm is $1/2 + 1/2 = 1$. **Status: Passed.**
- **Mode Indexing:**
The `_mode_idx` function correctly segments the 1D array into six blocks (3 paths $\times$ 2 polarizations). This is critical for MrMustard to know which modes to apply the Beam Splitter to later.
| Qubit Path | Offset | H-Modes | V-Modes |
| --- | --- | --- | --- |
| C (Qubit) | 0 | 0…M−1 | M…2M−1 |
| A (Bell 1) | 2M | 2M…3M−1 | 3M…4M−1 |
| B (Bell 2) | 4M | 4M…5M−1 | 5M…6M−1 |
匯出到試算表
- **Mixed Cutoffs:**
Using `ca_cutoff=3` is a clever move. In the next step (the Bell State Measurement), photons from $C$ and $A$ will hit a beam splitter. They might **bunch** into the same mode, meaning a mode might need to represent a state of $|2\rangle$. A cutoff of 3 allows for $0, 1, \text{ and } 2$ photons safely.

#### 3. Key Observations for Your Simulation
1. **Which Bell State?** Note that the code produces $|\Phi^-\rangle = \frac{1}{\sqrt{2}}(|HH\rangle - |VV\rangle)$. If your reference material expects $|\Psi^-\rangle = \frac{1}{\sqrt{2}}(|HV\rangle - |VH\rangle)$, you would just change the `idx` logic in the `P_AB` loop so that A and B have opposite polarizations.
2. **Addressing the Time Delay:** To simulate the timing jitter we discussed, you should modify the loop for `k_C`. Instead of a flat `amp_C`, you would multiply it by the phase factor $e^{i k_C \Delta z}$. This "tilts" the phase of the qubit pulse relative to the Bell pulse.
3. **Performance Tip:** For large $N$, the quadruple nested loop might get sluggish in Python. Since the amplitudes are mostly uniform, you could eventually move to NumPy slicing to populate the `ket`, but for a cross-check and initial validation, this explicit loop is much easier to debug.
This structure is perfectly poised for the next step: applying the 50/50 Beam Splitter between path $C$ and path $A$ to perform the BSM.
How do you plan to handle the measurement projection on the $C$ and $A$ modes to herald the success?