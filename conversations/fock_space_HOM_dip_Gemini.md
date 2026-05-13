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