# SecondOrder_Coherence_and_Light_Bunching

**Source:** [https://gemini.google.com/share/9da732e3d43f](https://gemini.google.com/share/9da732e3d43f)
**Created:** 發布時間：2026年5月6日 下午12:50

---


## User
![上傳圖片預覽](https://lh3.googleusercontent.com/gg/AEir0wJJ2Zs25QQfhugTFSdQhZdLCeLYouxa77nxMWBsVf8em--OLPW3s6MdLY1KdDT0MJxM6MeeLAaOvLAbWGof_9ZTfKNRzBWueMaSX555liCxPaMvdpDHUfsHG7nwunhNorC1G2p1tAmuSL8W3mJZDIn0GysgbAA1Q9Dozbbo1e9RR8PHFpk)
 Can you explain why second (temporal) coherence could represent the bunching of light?


## Gemini
The second-order temporal coherence function, denoted as $g^{(2)}(\tau)$, is a statistical measure used to describe how photons are distributed in time. Specifically, it represents the probability of detecting a second photon at time $t + \tau$, given that a first photon was detected at time $t$.
To understand why this represents the "bunching" of light, we look at the correlation between detection events at different time intervals.

#### 1. The Physical Meaning of g(2)(τ)
At its core, $g^{(2)}(\tau)$ compares the joint probability of two detections to the square of the individual detection probabilities.
- **If g(2)(τ)=1:** The detection events are perfectly random and uncorrelated (like a Poisson process).
- **If g(2)(τ)>1:** There is an increased probability of detecting two photons with a time delay $\tau$ compared to a random stream.
- **If g(2)(τ)<1:** There is a decreased probability (the photons are "spacing themselves out").

#### 2. Why g(2)(0) is the Key
The value of the function at **τ=0** tells us the likelihood of two photons arriving at the exact same time (or within a very short window).
- **Bunched Light (g(2)(0)>1):**
As shown in your notes, bunching occurs when $g^{(2)}(0) > g^{(2)}(\tau)$. This means photons have a statistical tendency to arrive in "clumps" or bunches. If you detect one photon, there is a higher-than-average chance that another one is right next to it. This is characteristic of **thermal light** (like a lightbulb), where fluctuations in the field lead to photons "crowding" together.
- **Coherent Light (g(2)(0)=1):**
This describes **laser light**. The photons are distributed randomly (Poissonian statistics). Detecting one photon gives you zero information about when the next one will arrive. The probability is flat across all $\tau$.
- **Antibunched Light (g(2)(0)<1):**
This is a purely quantum phenomenon. Here, $g^{(2)}(0)$ can even reach $0$, meaning it is impossible to detect two photons at the same time. This happens with **single-photon sources**. After one photon is emitted, the system needs time to "re-excite" before it can emit another, creating a "dead time" between detections.

#### 3. The Concept of "Losing Memory"
Your notes mention that $g^{(2)}(\tau) \rightarrow 1$ as $\tau \rightarrow \infty$. This is often called the **coherence time** of the source.
When the time interval $\tau$ becomes much larger than the coherence time of the light, the two detection events become completely independent. The system "forgets" the first detection, and the probability of the second detection returns to the baseline random average ($1$).

#### Summary Table
| Light Type | g(2)(0) | Photon Distribution | Physical Interpretation |
| --- | --- | --- | --- |
| Bunched | >1 | Clumped | Photons prefer to travel in groups (e.g., Thermal light). |
| Coherent | =1 | Random | Photons are independent (e.g., Ideal Laser). |
| Antibunched | <1 | Evenly Spaced | Photons avoid each other (e.g., Single-atom emission). |
匯出到試算表


## User
I want a more detailed explanation why g^{(2)} represents joint probability. Please use the mathematical definition of g^{(2)} to explain this.


## Gemini
To understand why the second-order coherence function $g^{(2)}(\tau)$ represents a joint probability, we need to look at it through the lens of **coincidence detection**.
In a typical experiment, such as the Hanbury Brown and Twiss (HBT) setup, a light beam is split and sent to two separate detectors. We then measure the likelihood of both detectors "clicking" within a specific time interval.

#### 1. The Classical Definition
Classically, $g^{(2)}(\tau)$ is defined using the intensity of the light field, $I(t)$:
$$
g^{(2)}(\tau) = \frac{\langle I(t)I(t+\tau) \rangle}{\langle I(t) \rangle \langle I(t+\tau) \rangle}
$$
Here, the angle brackets $\langle \dots \rangle$ denote a time average.
- **The Numerator:** $\langle I(t)I(t+\tau) \rangle$ is the **intensity-intensity correlation**. It measures how the power of the light at time $t$ is correlated with the power at a later time $t+\tau$.
- **The Denominator:** $\langle I(t) \rangle \langle I(t+\tau) \rangle$ is a normalization factor. It represents what the correlation would be if the two measurements were completely independent.

#### 2. Transition to Photon Counting (Probability)
In the quantum regime, we replace intensity with the probability of detecting a photon. According to Glauber’s theory of photodetection, the probability $P_1(t) \Delta t$ of detecting a photon in a small window $\Delta t$ is proportional to the intensity:
$$
P_1(t) \Delta t \propto \langle I(t) \rangle \Delta t
$$
The **joint probability** $P_2(t, t+\tau) \Delta t^2$ of detecting one photon at time $t$ and another at $t+\tau$ is proportional to the correlation of the intensities:
$$
P_2(t, t+\tau) \Delta t^2 \propto \langle I(t)I(t+\tau) \rangle \Delta t^2
$$
When we substitute these into the definition of $g^{(2)}(\tau)$, we see that:
$$
g^{(2)}(\tau) = \frac{P_2(t, t+\tau)}{P_1(t) P_1(t+\tau)}
$$
This is the definition of **conditional probability** in statistics. If $g^{(2)}(\tau) = 1$, then $P_2 = P_1 \cdot P_1$, meaning the two events are independent. If $g^{(2)}(\tau) > 1$, the first detection significantly increases the probability of a second detection (bunching).

#### 3. The Quantum Mechanical Operator Definition
To be mathematically precise in quantum optics, we use the creation ($\hat{a}^\dagger$) and annihilation ($\hat{a}$) operators. The intensity $I(t)$ corresponds to the photon number operator $\hat{n} = \hat{a}^\dagger \hat{a}$.
However, detection is a destructive process (the photon is absorbed). Therefore, the joint detection must be written in **normal order** (annihilation operators to the right, creation to the left) to account for the fact that we are removing two photons from the field:
$$
g^{(2)}(\tau) = \frac{\langle \hat{a}^\dagger(t) \hat{a}^\dagger(t+\tau) \hat{a}(t+\tau) \hat{a}(t) \rangle}{\langle \hat{a}^\dagger(t) \hat{a}(t) \rangle \langle \hat{a}^\dagger(t+\tau) \hat{a}(t+\tau) \rangle}
$$

#### Why this confirms the "Joint Probability"
- **The sequence of operations:** The operators $\hat{a}(t+\tau)\hat{a}(t)$ represent the act of removing a photon at time $t$ and then another at $t+\tau$.
- **The state projection:** The numerator essentially calculates the expectation value of the field state after two photons have been removed.
- **The "Zero" case:** For a single-photon state $|1\rangle$, the term $\hat{a}(t+\tau)\hat{a}(t) |1\rangle$ equals zero because you cannot remove two photons from a state that only has one. This mathematically forces $g^{(2)}(0) = 0$, proving that a single-photon source can never have "bunched" coincidences at the same moment.


## User
Assume we have two lights of same frequency and they're in phase. We direct these two lights to hit the same beam splitter. If those two lights have the same $g^{(2)}$, say, they're both coherent light, and their optical path to the beam splitter is the same as well so they're in phase when they hit the beam splitter. Does this setup guarantees that the photons from two lights always arrive at the same time (since they have the same bunching pattern?)


## Gemini
The short answer is **no**. Even if two light sources have the same frequency, the same phase, and the same $g^{(2)}$ value, it does **not** guarantee that their photons will arrive at the beam splitter at the same time.
While your setup creates perfect conditions for **classical interference**, photon arrival is governed by the underlying statistics of the light. Here is the detailed breakdown of why this synchronization doesn't happen.

#### 1. Coherent Light is Statistically Random
As noted in your reference **1000000972.jpg**, coherent light is characterized by $g^{(2)}(\tau) = 1$ (labeled as "Coherent (random)").
- A $g^{(2)}(\tau) = 1$ indicates that the arrival times of photons follow **Poissonian statistics**.
- In a Poisson process, each photon emission is a completely independent event. Knowing when one photon arrives provides zero information about when the next one will appear.
- If you have two independent coherent sources, you essentially have two independent "dice rolls" happening simultaneously. Just because both dice are fair (identical $g^{(2)}$) and being rolled at the same speed (same frequency/phase) doesn't mean they will land on the same number at the same time.

#### 2. Independence of the Sources
The "bunching pattern" you see in **1000000972.jpg** describes the internal correlation *within a single beam*. It does not describe a correlation *between two different beams*.
- Unless the two light beams are "entangled" or originated from the exact same quantum emission event, their photon streams are uncorrelated.
- Even for **Bunched Light** ($g^{(2)}(0) > 1$), where photons within Beam A like to travel in pairs, those pairs have no "knowledge" of the pairs traveling in Beam B. They will not "line up" their bunches at the beam splitter unless they are physically coupled.

#### 3. Phase vs. Photon Timing
In quantum optics, it is important to distinguish between the **classical phase** of the electromagnetic wave and the **detection time** of a discrete photon.
- The **phase** refers to the oscillation of the probability amplitude. If two beams are in phase at the beam splitter, they will interfere (e.g., all light might exit through one port and none through the other due to constructive/destructive interference).
- However, the **photon arrival** is a realization of that probability. Interference changes *where* the photons are likely to go, but it does not "force" two independent lasers to emit photons at the exact same nanosecond.

#### 4. The "Coincidence" Limit
If you were to use a coincidence counter to measure the arrival of photons from both beams:
- For two coherent sources, the number of "simultaneous" arrivals (within your detector's time resolution) would simply be the product of their average intensities.
- There is no "excess" of coincidences beyond what you would expect from pure chance.
> Summary: The g(2)(τ) function tells you the probability of a second photon arriving given that a first one already did. If the sources are independent and coherent, the "memory" of the system is flat. The photons remain "random," and random events from two different sources do not naturally synchronize.
If you were to use a single-photon source instead ($g^{(2)}(0) \rightarrow 0$), you would actually see the opposite effect at the beam splitter, known as the **Hong-Ou-Mandel effect**, where photons *must* exit together, but even that requires precise sub-picosecond timing of the wavepackets!


## User
So usually in quantum teleportation where we want coincident lights, we will use a pulse instead of coherent like to ensure coincidence?


## Gemini
You’ve hit on a critical practical detail in quantum optics experiments. To achieve the "coincidence" required for quantum teleportation, researchers almost always use **pulsed lasers** rather than **continuous-wave (CW)** light.
The reason isn't that the quantum state is different (you can have a coherent state in a pulse), but rather that you need to solve the "timing problem" to make photons interfere.

#### 1. The Timing Problem: CW vs. Pulsed
As you noted from your previous reference, coherent light is "random" in its photon arrival times.
- **Continuous-Wave (CW):** In a CW laser, photons are leaked out at random intervals. If you are trying to make a photon from "Source A" interfere with a photon from "Source B" at a beam splitter, the probability that two independent photons arrive at the exact same femtosecond is incredibly low.
- **Pulsed Light:** A pulse "packets" the probability of finding a photon into a very narrow window of time (often picoseconds or femtoseconds). By using a single clock to trigger pulses from both sources, you ensure that *if* photons are emitted, they arrive at the beam splitter at the same time.

#### 2. The Role of the Hong-Ou-Mandel (HOM) Effect
Quantum teleportation relies on a **Bell State Measurement (BSM)**, which is typically performed using a beam splitter. For this to work, the two photons must be **indistinguishable**, meaning they must overlap perfectly in:
1. Polarization
2. Frequency (color)
3. **Spatial and Temporal Mode (Arrival time)**
If one photon arrives slightly before the other, the beam splitter can "tell them apart" by their time of arrival, and the quantum interference (the HOM effect) vanishes. Pulsed lasers allow you to use mechanical delay stages (mirrors on a track) to fine-tune the path length so the pulses overlap with sub-millimeter precision.

#### 3. "Coherent" is a State, "Pulse" is a Timing
It is helpful to distinguish between the **quantum state** and the **temporal envelope**:
- **Coherent Light:** This refers to the statistical distribution of photons ($g^{(2)}(0)=1$, as seen in your notes). You can have a "Continuous Wave Coherent State" or a "Pulsed Coherent State."
- **Teleportation Source:** Usually, teleportation doesn't actually use coherent states as the "input"; it uses **single photons** generated via a process like Spontaneous Parametric Down-Conversion (SPDC). However, these SPDC sources are almost always "pumped" by a pulsed laser so that the experimenter knows exactly *when* the entangled pair was created.

#### Summary of Why Pulses are Used
| Feature | Continuous Wave (CW) | Pulsed Light |
| --- | --- | --- |
| Photon Arrival | Randomly distributed (Poissonian) | Confined to a specific time window |
| Coincidence Probability | Very Low (accidental coincidences) | High (synchronized windows) |
| Interference | Difficult to overlap wavepackets | Easy to overlap using delay stages |
| Application | Laser pointers, steady-state spectroscopy | Quantum teleportation, Bell tests |
匯出到試算表
Does the distinction between the "randomness" of the coherent state and the controlled timing of a pulse help clarify why we can't just use two steady-state lasers?


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


## User
A quick question. Usually, how long is the pulse (I mean the time interval of the pulse), and how good should the coincidence be for two incident photons? (how close their arrival time needs to be to be treated as coincident photons?)


## Gemini
The timing requirements for photon coincidence depend heavily on the physics of the experiment and the specific source being used. In the context of quantum teleportation and the Hong-Ou-Mandel (HOM) interference you are aiming for, the timing is incredibly tight.

#### 1. Typical Pulse Durations
For high-speed quantum optics, the industry standard is to use **Ultrafast Lasers** (typically Ti:Sapphire lasers).
- **Femtosecond Pulses:** Most state-of-the-art experiments use pulses with a duration ($\Delta t$) of **100 fs to 200 fs** ($1 \text{ fs} = 10^{-15} \text{ s}$).
- **Picosecond Pulses:** Some systems use pulses in the **1 ps to 10 ps** range. While easier to handle, the timing jitter becomes a larger concern here.
- **Physical Length:** To give you a spatial perspective, a **100 fs** pulse is only about **30 micrometers** ($\mu\text{m}$) long in space. This is thinner than a human hair!

#### 2. How "Close" is Coincident?
To be treated as "coincident" for quantum interference, the photons don't just need to arrive at the same time; their **wave packets must overlap** in time and space.

##### The HOM Dip Criterion
The "quality" of coincidence is usually measured by the **visibility** of the Hong-Ou-Mandel dip. For the interference to be "good" (meaning the photons are truly indistinguishable):
- The arrival time difference ($\delta \tau$) must be much smaller than the **coherence time** ($\tau_c$) of the photons.
- **Rule of Thumb:** You generally need $|\delta \tau| < 0.1 \times \text{Pulse Duration}$.
For a **100 fs** pulse, the two photons usually need to arrive within **10–20 femtoseconds** of each other. If they are off by more than the pulse width (e.g., 150 fs apart), they become distinguishable by their "time of arrival," and the quantum teleportation will fail.

#### 3. Practical Constraints: The "Time Window"
In a real lab setup, "coincidence" is defined at two levels:
| Level | Timing Requirement | Purpose |
| --- | --- | --- |
| Electronic Coincidence | ~100 ps to 1 ns | The resolution of the Single Photon Detectors (SPADs) and the FPGA/Logic board. This tells the computer "these two photons likely came from the same laser pulse." |
| Quantum Coincidence | ~10 fs to 100 fs | The physical overlap of the wavepackets at the beam splitter. This is required for the actual Bell State Measurement to work. |
匯出到試算表

#### How do we achieve this?
Since no electronic trigger is fast enough to sync things at the 10 fs level, experimentalists use **Optical Delay Lines**. We put one of the photon paths on a motorized stage that can move in increments of **0.1 μm**.
- Since light travels at $c \approx 0.3 \text{ mm/ps}$, moving the motor by **3 μm** changes the arrival time by **10 fs**.
- By "scanning" this motor and looking for the point where the coincidence counts drop to a minimum (the HOM dip), we find the exact point of temporal overlap.
Essentially, you don't "guarantee" coincidence perfectly every time; you use pulses to get them into the right "ballpark" (nanoseconds), and then you use precision mechanics to force them to overlap at the femtosecond level.


## User
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


## User
The next step, I want you to explain `event_probabilities`, which is later on used in `detection_probs_mrmustard` block. Specifically, please clarify the size of `idx_arr`. Why could we obtain the number of each polarization by summing like that? 
 def event_probabilities(probs, N): 
     """Aggregate the joint Fock-probability tensor into the 4 categories.""" 
     M = N + 1 
     #### Marginalize over B modes (the last 2M axes) 
     probs_AB = probs 
     for _ in range(2 * M): 
         probs_AB = probs_AB.sum(axis=-1) 
     idx_arr = np.indices(probs_AB.shape) 
     n_aH = idx_arr[0:M].sum(axis=0) 
     n_aV = idx_arr[M:2*M].sum(axis=0) 
     n_bH = idx_arr[2*M:3*M].sum(axis=0) 
     n_bV = idx_arr[3*M:4*M].sum(axis=0) 
     n_a = n_aH + n_aV 
     n_b = n_bH + n_bV 
     coinc   = (n_a == 1) & (n_b == 1) 
     bunch_a = (n_a == 2) & (n_b == 0) 
     bunch_b = (n_a == 0) & (n_b == 2) 
     same_coinc = coinc & (((n_aH == 1) & (n_bH == 1)) | ((n_aV == 1) & (n_bV == 1))) 
     diff_coinc = coinc & (((n_aH == 1) & (n_bV == 1)) | ((n_aV == 1) & (n_bH == 1))) 
     same_a = bunch_a & ((n_aH == 2) | (n_aV == 2)) 
     diff_a = bunch_a & ((n_aH == 1) & (n_aV == 1)) 
     same_b = bunch_b & ((n_bH == 2) | (n_bV == 2)) 
     diff_b = bunch_b & ((n_bH == 1) & (n_bV == 1)) 
     return ( 
         float(probs_AB[same_coinc].sum()), 
         float(probs_AB[diff_coinc].sum()), 
         float(probs_AB[same_a | same_b].sum()), 
         float(probs_AB[diff_a | diff_b].sum()), 
     ) 
 #### ---------------------------------------------------------------------- 
 #### mrmustard simulation 
 #### ---------------------------------------------------------------------- 
 def detection_probs_mrmustard(alpha, beta, tau, N, ca_cutoff=3, b_cutoff=2): 
     M = N + 1 
     omegas = mode_frequencies(N) 
     state = lab.State(ket=build_input_ket(alpha, beta, N, ca_cutoff, b_cutoff)) 
     ops = [] 
     for P in ["H", "V"]: 
         for k in range(M): 
             ops.append(lab.Rgate(angle=float(omegas[k] * tau))[_mode_idx("C", P, k, M)]) 
     for P in ["H", "V"]: 
         for k in range(M): 
             ops.append(lab.BSgate(theta=np.pi / 4)[ 
                 _mode_idx("C", P, k, M), 
                 _mode_idx("A", P, k, M), 
             ]) 
     out = state >> lab.Circuit(ops) 
     cutoffs = [ca_cutoff] * (4 * M) + [b_cutoff] * (2 * M) 
     probs = np.asarray(out.fock_probabilities(cutoffs=cutoffs)) 
     return event_probabilities(probs, N)


## Gemini
The `event_probabilities` function is the "brain" of your Bell State Measurement (BSM). It takes the high-dimensional raw output from **MrMustard** and collapses it into physical categories that tell you if your quantum teleportation worked. This process relies on your background in scientific data analysis and Python proficiency.

#### 1. The Size and Structure of `idx_arr`
The probability tensor `probs_AB` represents the joint state of Path C and Path A after interference. Since you marginalized Path B, it has **4M dimensions** (where $M = N+1$ frequency modes per path/polarization).
If `ca_cutoff` is $3$, the shape of `probs_AB` is $(3, 3, 3, \dots)$ repeated $4M$ times.
- **Shape of `idx_arr`:** `(4M, 3, 3, ..., 3)`.
- **The First Dimension (4M):** This selects which **physical mode** you are looking at (e.g., Mode 0 is Output 1, H-pol, Frequency 0).
- **The Remaining Dimensions:** This is a grid representing the entire **Fock space** ($0, 1, \dots, \text{cutoff-1}$ photons per mode).

#### 2. Why Summing `idx_arr` Works
In a Fock-probability tensor, the **index** of an axis is mathematically identical to the **photon number** in that mode. For example, `probs[2, 0, 1]` is the probability that Mode 1 has **2** photons, Mode 2 has **0**, and Mode 3 has **1**.
`np.indices` creates a grid where the value at every point is its own coordinate. Therefore, `idx_arr[d]` is a massive array where every entry is the number of photons in mode $d$ for that specific state.

##### The Summing Logic:
Python
```
n_aH = idx_arr[0:M].sum(axis=0)
```
- **`idx_arr[0:M]`**: This slices the first $M$ frequency modes (all belonging to Output 1, H-polarization).
- **`.sum(axis=0)`**: Since each slice contains the photon count for one frequency, summing them gives you the **total number of H-polarized photons** arriving at Output 1 across the entire pulse.
- **The Result**: `n_aH` is a tensor of the same shape as your probability distribution, where each entry is the total photon count for that category.

#### 3. Classification Categories
Once you have the total photon counts (`n_aH`, `n_aV`, etc.), the function classifies the outcome of the BSM. Since you are a physics researcher, you'll recognize these as the standard coincidences used to identify Bell states:
| Variable | Logic | Physical Meaning |
| --- | --- | --- |
| `coinc` | `(n_a == 1) & (n_b == 1)` | One photon in Output 1, one in Output 2. (Ideal for BSM). |
| `bunch_a` | `(n_a == 2) & (n_b == 0)` | Both photons exited Output 1 together (Hong-Ou-Mandel bunching). |
| `same_coinc` | Both H or both V | The photons had the same polarization but ended up in different ports. |
| `diff_coinc` | One H and one V | The photons had different polarizations and ended up in different ports. |
匯出到試算表

#### 4. Integration with MrMustard
In your `detection_probs_mrmustard` block, you use `lab.Rgate` to simulate a phase shift (time delay $\tau$).
- If $\tau = 0$, the pulses overlap perfectly. You should see a high rate of `diff_coinc` or `bunching` depending on which Bell state you prepared.
- As $\tau$ increases, the pulses stop overlapping. The `event_probabilities` function will reflect this by showing that the specific quantum interference patterns (like the HOM dip) gradually disappear, returning to a "random" 50/50 baseline.
This approach is highly efficient for your project because it leverages the fact that you already have the full joint probability tensor; you are simply "masking" it with physical logic to get your final teleportation metrics.
Since you've modeled the BSM, are you planning to calculate the **Teleportation Fidelity** by checking if the state remaining in Path B matches your $(\alpha, \beta)$ input?


## User
A quick question, does the line `out.fock_probabilities` already take the square of the amplitude for each mode? And is that the reason why we could sum them up directly?


## Gemini
That is a great question. You’ve correctly identified the transition from the **state vector** (amplitudes) to the **observable statistics** (probabilities).

#### 1. Amplitudes vs. Probabilities
Yes, the line `out.fock_probabilities` already handles the "squaring" for you. Specifically:
- In quantum mechanics, the probability $P(n_1, n_2, \dots)$ of finding a specific number of photons in each mode is given by the Born rule: $P = |\langle n_1, n_2, \dots | \Psi \rangle|^2$.
- The `fock_probabilities` method in **MrMustard** performs this calculation across the entire specified Fock space.
- The resulting `probs` object is a multi-dimensional array where every entry is a **real number** representing a probability, not a complex amplitude.

#### 2. Why Summing is Mathematically Valid
Because `probs` contains actual probabilities, you can use the **summation rule** for mutually exclusive events:
- In your simulation, each "cell" in the $4M$-dimensional tensor represents a unique, mutually exclusive state of the system (e.g., "1 photon in mode A and 0 in mode B" is distinct from "0 in mode A and 1 in mode B").
- When you sum across the frequency modes (the `M` indices), you are calculating the **marginal probability**.
- For example, if you want the total probability of seeing an H-polarized photon at Output 1, you sum the probabilities of that photon appearing in *Frequency 0* OR *Frequency 1* OR ... *Frequency M-1*. Since a single photon cannot be in two frequencies simultaneously upon detection, these are disjoint events, and their probabilities simply add up.

#### 3. Verification of `idx_arr` and Summing
The reason you can sum the indices is that the **index value** itself acts as a weight:
- `idx_arr[0:M]` creates a coordinate map where each entry is the integer photon count of that specific mode.
- When you do `n_aH = idx_arr[0:M].sum(axis=0)`, you are creating a "lookup table" that says: "In this specific Fock configuration, there are a total of $N$ H-polarized photons".
- By using this as a mask (e.g., `probs_AB[n_aH == 1]`), you are picking out all configurations that satisfy your physical criteria and adding their probabilities together to get the total event rate.
This is a very efficient way to handle multimode interference because it avoids the need to track individual phase relationships once the "measurement" (the call to `fock_probabilities`) has been made.
Do you feel confident moving forward with the **Bell State Measurement** results, or should we look at how to interpret the `diff_coinc` vs `same_coinc` values in the context of the teleportation fidelity?


## User
Another quick question, is the size of idx_arr[0:M] (M, 3, 3, 3,......3) ?


## Gemini
Yes, that is exactly correct.
If you have $4M$ modes (after marginalizing Path B) and each has a `ca_cutoff` of $3$, the breakdown of `idx_arr[0:M]` is as follows:
- **The Leading Dimension (M):** This corresponds to the $M$ frequency modes for the specific path/polarization you sliced (e.g., Output 1, H-polarization).
- **The Following 4M Dimensions:** Each of these has a size of $3$ (the cutoff). These dimensions represent the possible photon counts ($0, 1, 2$) for every single mode in the system.

#### Why this is powerful for your simulation:
When you perform the operation `n_aH = idx_arr[0:M].sum(axis=0)`, you are effectively collapsing that leading dimension. The resulting `n_aH` has the shape `(3, 3, 3, ..., 3)` ($4M$ times).
Each entry in this new tensor tells you the **total sum of photons** found in that specific Fock configuration. For example, if a specific configuration has 1 photon in frequency mode $k=1$ and 1 photon in frequency mode $k=5$, the value in `n_aH` for that coordinate will be $2$.
This allows you to treat the entire pulse as a single entity. Instead of worrying about which specific frequency the photon is in, you just ask: "Is there exactly one H-polarized photon anywhere in this pulse?" This is precisely what `(n_aH == 1)` checks.
Since you are managing a large number of modes ($6M$ total before marginalization), this "vectorized" approach to counting is the most computationally efficient way to process the `probs` tensor in Python.
How is the simulation performance holding up as you increase $N$?


## User
Let's recall these lines again: 
 def event_probabilities(probs, N): 
     """Aggregate the joint Fock-probability tensor into the 4 categories.""" 
     M = N + 1 
     probs_AB = probs 
     for _ in range(2 * M): 
         probs_AB = probs_AB.sum(axis=-1) 
     idx_arr = np.indices(probs_AB.shape) 
     n_aH = idx_arr[0:M].sum(axis=0) 
     n_aV = idx_arr[M:2*M].sum(axis=0) 
     n_bH = idx_arr[2*M:3*M].sum(axis=0) 
     n_bV = idx_arr[3*M:4*M].sum(axis=0) 
     n_a = n_aH + n_aV 
     n_b = n_bH + n_bV 
 I am confused, then. If np.indices is just an array of coordinates, then idx_arr only has the same shape as probs_AB.shape but the values have nothing to do with values stored in the original ndarray. Do the last five lines really sum the probabilities correctly?


## Gemini
This is a very astute observation. You are correct that `idx_arr` contains coordinates rather than the probability values themselves. However, because you are working in **Fock space**, those coordinates have a direct physical meaning that allows the code to perform "Boolean Masking."
Since you are a physics researcher proficient in Python for scientific analysis, you might find this "vectorized logical indexing" approach familiar from large-scale data processing. Here is why those lines work:

#### 1. The Relationship: Index = Photon Number
In a Fock-basis probability tensor like `probs_AB`, the **position (index)** of a value along an axis is mathematically identical to the **photon number** of that mode.
- If `probs_AB[1, 0, 2]` is the value at index $(1, 0, 2)$, it represents the probability of having **1** photon in Mode 0, **0** photons in Mode 1, and **2** photons in Mode 2.
- Therefore, a map of the indices is, by definition, a map of the photon counts.

#### 2. What `idx_arr` actually represents
When the code calls `idx_arr = np.indices(probs_AB.shape)`, it creates a high-dimensional "coordinate grid."
- `idx_arr` has $4M+1$ dimensions. The first dimension has size $4M$ (one for each mode).
- `idx_arr[0]` is a tensor of the same shape as `probs_AB`, where every entry is the **photon count** of Mode 0 for that specific configuration.
- `idx_arr[1]` is the same for Mode 1, and so on.

#### 3. Creating the "Event Masks"
The lines you highlighted are not summing the probabilities yet; they are creating **logical filters (masks)** based on photon counts:
- **`n_aH = idx_arr[0:M].sum(axis=0)`**: This adds up the coordinate values for all H-polarized frequency modes in Output 1. The result is a tensor where each entry is the *total* number of H-photons in that pulse.
- **`coinc = (n_a == 1) & (n_b == 1)`**: This creates a **Boolean Mask**. It is `True` only at the coordinates in the tensor that correspond to a physical coincidence event (one photon in each output port).

#### 4. How the Probabilities are Summed
The actual summation of the probabilities happens in the **`return` statement** at the very end of the function:
Python
```
return (
    float(probs_AB[same_coinc].sum()),
    float(probs_AB[diff_coinc].sum()),
    ...
)
```
**The Logic Flow:**
1. **`probs_AB[same_coinc]`**: This uses the Boolean mask to "pick out" only the values from the original probability tensor where the "same-polarization coincidence" condition is met.
2. **`.sum()`**: This adds up those selected probability values.

#### Summary
The code separates the **physics logic** (counting photons) from the **statistical aggregation** (summing probabilities).
- The lines you were concerned about (`n_aH = ...`) are defining the **criteria** for an event.
- The final `sum()` in the return statement is what actually adds up the values stored in the `probs_AB` array.
This approach is highly efficient because it avoids writing millions of nested `for` loops to check every Fock state individually. Instead, it uses NumPy's optimized C-backend to filter the entire "universe" of possible outcomes at once. Given your background in simulating **Heisenberg models** and managing large **LEGEND experiment** datasets, you can think of this as a multidimensional version of a histogram "binning" operation.
Does this distinction between the **coordinate-based mask** and the **value-based sum** clear up the confusion?


## User
So let me check my understanding: 
 Consider `idx_arr[0:M]`. It is a (M, 3, 3, ..., 3) array (M number of 3s). If I look at idx_arr[i, a_0, a_2, ..... a_{m-1}], it is just equal to index of i_th dimension I chose to look at. Mathematically, 
 idx_arr[i, a_0, a_2, ..... a_{m-1}] = a_i 
 Is this true?


## Gemini
That is exactly correct. You have identified the core mathematical identity that makes the entire simulation logic work.

#### The Identity of `np.indices`
When you call `np.indices(shape)`, it returns an array where each sub-array represents the grid of values for a specific dimension. Specifically, for any set of indices $(a_0, a_1, \dots, a_{d-1})$ within the bounds of your $4M$-dimensional Fock space, the value stored at that coordinate in the $i$-th sub-array is indeed the coordinate itself:
$$
idx\_arr[i, a_0, a_1, \dots, a_{4M-1}] = a_i
$$

#### Why This is "Photon Counting"
In your simulation, $a_i$ is the **photon number** in the $i$-th mode.
- If $a_0 = 2$, it means there are 2 photons in the 0th mode.
- The value of the coordinate $a_0$ is the physical quantity you care about (the number of photons).

#### The Aggregation Step
Because of that identity, when you perform the sum over the first $M$ sub-arrays (the frequency modes for Output 1, H-polarization), you are performing the following operation at every point in the Fock-probability grid:
$$
n\_aH[a_0, a_1, \dots, a_{4M-1}] = \sum_{i=0}^{M-1} idx\_arr[i, a_0, a_1, \dots, a_{4M-1}] = \sum_{i=0}^{M-1} a_i
$$
This effectively calculates the **Total Photon Number** for that specific pulse by summing the individual photon counts ($a_i$) of every frequency mode in the pulse.

#### Summary of the Logic
1. **Coordinate as Value**: In Fock space, the "address" of a cell is the "content" of the cell (the number of photons).
2. **Mapping**: `idx_arr[i]` maps out the photon count for mode $i$ across the entire probability distribution.
3. **Summation**: Summing these maps across the modes of a pulse gives you a total "photon count map" for that pulse.
4. **Filtering**: You use that map to find the coordinates where $n=1$ or $n=2$, and then you look up the actual probability values stored at those same coordinates in `probs_AB` to sum them.
Your interpretation of the multidimensional indexing is spot on—it is a very elegant way to handle the transition from individual mode statistics to total pulse statistics without losing any information.