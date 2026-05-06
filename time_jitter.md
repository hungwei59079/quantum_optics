# Time-jitter analytics: derivations

This note explains the closed-form results that appear in
[teleportation_time_jitter.py](teleportation_time_jitter.py) and
[teleportation_time_jitter_fidelity.py](teleportation_time_jitter_fidelity.py).
Everything follows from one structural observation: **the four polarization
terms in the input state's expansion live in disjoint post-BS Fock
subspaces, so they don't interfere.** Once you accept that, each term can
be analyzed independently and the outcome probabilities just add up
classically (weighted by $|\alpha|^2$ and $|\beta|^2$).

## Setup and notation

Each polarization mode of each qubit is a single-photon wavepacket
spread coherently across $M = N+1$ frequency modes
$\omega_k = \omega_0 + k\,\Delta\omega$, $k = -N/2, \dots, +N/2$, all with
the same per-mode amplitude $1/\sqrt{M}$:

$$
|H\rangle_X \;=\; \frac{1}{\sqrt{M}} \sum_k a^\dagger_{X,H,k}\, |0\rangle,
\qquad
|V\rangle_X \;=\; \frac{1}{\sqrt{M}} \sum_k a^\dagger_{X,V,k}\, |0\rangle,
\qquad X \in \{C, A, B\}.
$$

The input state is
$|\psi\rangle_C = \alpha|H\rangle_C + \beta|V\rangle_C$;
the resource is
$|\Phi^{-}\rangle_{AB} = (|HH\rangle_{AB} - |VV\rangle_{AB})/\sqrt{2}$.
The full input is

$$
|\Psi\rangle_\text{in} \;=\; |\psi\rangle_C \otimes |\Phi^{-}\rangle_{AB}.
$$

The Bell-measurement BS couples the C and A modes per-frequency, per
polarization. A delay $\tau$ on the C qubit applies a per-mode phase
$e^{i\omega_k\tau}$ to *all* C modes (both polarizations together — the
qubit is delayed as one). With the convention

$$
a^\dagger_{C,P,k} \;\to\; \frac{1}{\sqrt{2}}\bigl(a^\dagger_{\alpha,P,k} + a^\dagger_{\beta,P,k}\bigr),
\qquad
a^\dagger_{A,P,k} \;\to\; \frac{1}{\sqrt{2}}\bigl(a^\dagger_{\alpha,P,k} - a^\dagger_{\beta,P,k}\bigr),
$$

the labels $\alpha$ and $\beta$ index the two output spatial ports, and
each polarization $P \in \{H, V\}$ is mixed independently per frequency.

## The HOM-dip building block

Two indistinguishable single-photon wavepackets meeting at a 50/50 BS
give the standard Hong–Ou–Mandel coincidence rate

$$
\mathrm{HOM}(\tau) \;=\; \frac{1}{2}\Bigl(1 - \frac{D_N(\Delta\omega\,\tau)^2}{(N+1)^2}\Bigr),
$$

where $D_N(x) = \sin\bigl((N+1)x/2\bigr)/\sin(x/2)$ is the Dirichlet
kernel (derived in
[coincidence_number_states.py](coincidence_number_states.py)). This is
the *only* place $\tau$ enters the teleportation analysis — every
$\tau$-dependent quantity below is expressed in terms of
$\mathrm{HOM}(\tau)$.

The carrier $\omega_0$ does *not* appear — sums over the symmetric mode
comb factor as $e^{i\omega_0\tau}\,D_N(\Delta\omega\tau)$, and the
carrier piece always cancels in $|\cdot|^2$.

## The four-term decomposition

Expand the input on the H/V basis of all three qubits:

$$
|\Psi\rangle_\text{in} \;=\; \frac{1}{\sqrt{2}} \Bigl[
\underbrace{\alpha\,|HHH\rangle}_{\text{Term 1}}
\;-\; \underbrace{\alpha\,|HVV\rangle}_{\text{Term 2}}
\;+\; \underbrace{\beta\,|VHH\rangle}_{\text{Term 3}}
\;-\; \underbrace{\beta\,|VVV\rangle}_{\text{Term 4}}
\Bigr]
$$

with $|P_C P_A P_B\rangle = |P\rangle_C |P\rangle_A |P\rangle_B$. Each term has
weight $|\alpha|^2/2$ or $|\beta|^2/2$ in the probability budget, and
together they sum to 1.

**Why the four terms don't interfere.** After the BS, classify each
term's output Fock support by two labels: (i) the polarization of the
B-side photon, (ii) the polarization composition at the $\alpha\beta$
ports.

| Term | $|\psi\rangle_{\text{in}}$ | $\alpha\beta$ side after BS | B side |
|------|---------------------------|---------------------------|--------|
| 1 | $\alpha\,|HHH\rangle$  | two H photons              | one H |
| 2 | $-\alpha\,|HVV\rangle$ | one H + one V photon       | one V |
| 3 | $\beta\,|VHH\rangle$   | one H + one V photon       | one H |
| 4 | $-\beta\,|VVV\rangle$  | two V photons              | one V |

Pairwise: any two terms differ either on the B side (terms 2 vs 3, 1 vs
2, etc.) or on the $\alpha\beta$ polarization composition (terms 1 vs
3, 1 vs 4, 2 vs 4). Since polarization-mode photon-number is preserved
by the BS, the four output sectors are **mutually orthogonal in Fock
space**. There is no interference between them, and probabilities of
detection events add classically with weights
$|\alpha|^2/2$, $|\alpha|^2/2$, $|\beta|^2/2$, $|\beta|^2/2$.

This decoupling is the master idea — every "constant 1/4" or "$\mathrm{HOM}/2$"
below comes from summing four independent contributions.

**Each term's BS analysis** (for the *gross* probabilities — frequency
phases will matter only when we get to fidelity):

- **Term 1 (HHH).** Two H photons interfere via HOM in the H sector;
  the V sector is empty. Coincidence (one H at $\alpha$, one H at $\beta$)
  occurs with probability $\mathrm{HOM}(\tau)$; bunching (both H at one port)
  with probability $1-\mathrm{HOM}(\tau)$. Polarization is *same* (both H)
  in either case.

- **Term 4 (VVV).** Symmetric to Term 1 with V instead of H. Same
  probabilities; polarization is *same* (both V).

- **Term 2 (HVV).** The C photon is H, the A photon is V; they sit in
  different polarization sectors and **don't interfere**. Each photon
  goes 50/50 between $\alpha$ and $\beta$, independently. The four
  outcomes (H@$\alpha$,V@$\alpha$), (H@$\alpha$,V@$\beta$), (H@$\beta$,
  V@$\alpha$), (H@$\beta$,V@$\beta$) each have probability $1/4$.
  So conditional probabilities are: coincidence $1/2$, bunching $1/2$;
  polarization is always *different* (one H, one V).

- **Term 3 (VHH).** Symmetric to Term 2 with the roles of $H$ and $V$
  swapped between C and A. Same conditional probabilities; always *diff*
  polarization.

The four detection categories now follow by mixing.

## $P_\text{coinc, same}(\tau) = \mathrm{HOM}(\tau)/2$

Only Terms 1 and 4 contribute (only they have same polarization at
$\alpha\beta$), and each contributes its HOM coincidence rate:

$$
P_\text{coinc, same}(\tau)
= \frac{|\alpha|^2}{2}\cdot \mathrm{HOM}(\tau)
+ \frac{|\beta|^2}{2}\cdot \mathrm{HOM}(\tau)
= \frac{\mathrm{HOM}(\tau)}{2}.
$$

The $|\alpha|^2 + |\beta|^2 = 1$ collapse means the result is independent
of which qubit was input. Physically: timing jitter degrades the HOM
interference for the same-polarization sectors, leaking probability mass
that would otherwise have bunched. At $\tau = 0$ this is zero (perfect
HOM bunching); at full distinguishability ($\mathrm{HOM} = 1/2$) it
saturates at $1/4$.

## $P_\text{coinc, diff}(\tau) = 1/4$

Only Terms 2 and 3 contribute (they have $1H+1V$ at $\alpha\beta$),
and each contributes its $1/2$ "two independent photons split between
two ports" probability:

$$
P_\text{coinc, diff}(\tau)
= \frac{|\alpha|^2}{2}\cdot \frac{1}{2}
+ \frac{|\beta|^2}{2}\cdot \frac{1}{2}
= \frac{1}{4}.
$$

This is constant in $\tau$ — Terms 2 and 3 have *no HOM interference*
because the C and A photons are in orthogonal polarization sectors and
go through independent BSs. Timing jitter has nothing to interfere with,
so it leaves these outcomes alone.

## $P_\text{1-arm, same}(\tau) = (1 - \mathrm{HOM}(\tau))/2$

The complement of $P_\text{coinc, same}$ within the same-polarization
sectors of Terms 1 and 4 (since Terms 2, 3 contribute nothing to "same
polarization"):

$$
P_\text{1-arm, same}(\tau)
= \frac{|\alpha|^2}{2}\cdot (1 - \mathrm{HOM}(\tau))
+ \frac{|\beta|^2}{2}\cdot (1 - \mathrm{HOM}(\tau))
= \frac{1 - \mathrm{HOM}(\tau)}{2}.
$$

This is the HOM-bunching peak: at $\tau = 0$ it equals $1/2$ (every
HHH/VVV event produces bunching at one port); it falls to $1/4$ at full
distinguishability.

## $P_\text{1-arm, diff}(\tau) = 1/4$

Symmetric to $P_\text{coinc, diff}$ — only Terms 2, 3 contribute, each
with conditional bunching probability $1/2$:

$$
P_\text{1-arm, diff}(\tau)
= \frac{|\alpha|^2}{2}\cdot \frac{1}{2}
+ \frac{|\beta|^2}{2}\cdot \frac{1}{2}
= \frac{1}{4}.
$$

Same logic as $P_\text{coinc, diff}$: no HOM interference is available
to these terms, so the rate is $\tau$-independent.

The four detection categories sum to 1 for any $\tau$:
$\mathrm{HOM}/2 + 1/4 + (1-\mathrm{HOM})/2 + 1/4 = 1$. ✓

## $F(\tau) = 1 - 4\,|\alpha|^2|\beta|^2 \cdot \mathrm{HOM}(\tau)$

The fidelity calculation post-selects on the four "diff pol" detection
outcomes (whose Bell-state assignment is unambiguous in a BS-only Bell
measurement):

| outcome $(n_{\alpha H},\, n_{\alpha V},\, n_{\beta H},\, n_{\beta V})$ | Bell projection | correction |
|---------------|-------------|---------------|
| $(1, 0, 0, 1)$ | $\Psi^{-}$ | $X$ |
| $(0, 1, 1, 0)$ | $\Psi^{-}$ | $X$ |
| $(1, 1, 0, 0)$ | $\Psi^{+}$ | $X$ then $Z$ |
| $(0, 0, 1, 1)$ | $\Psi^{+}$ | $Z$ then $X$ |

These correspond to $P_\text{coinc, diff}$ and $P_\text{1-arm, diff}$,
with total post-selection probability $1/4 + 1/4 = 1/2$ — independent of
$\tau$. The HH/VV bunched outcomes (constant $\Phi^{-}$ rate plus a
$\tau$-dependent coincidence-same component) are dropped because $\Phi^+$
and $\Phi^-$ produce identical detection patterns in BS-only Bell
measurement and so have no unique correction.

**Why only Terms 2 and 3 contribute to post-selected outcomes.** Each
post-selected macro-outcome has exactly one H photon and one V photon at
the $\alpha\beta$ ports; only Terms 2 and 3 produce this $H+V$
composition. So the conditional Bob ket is a coherent sum of
contributions from Terms 2 and 3, with their $\alpha$ and $\beta$ weights
playing back against each other.

**Conditional Bob state.** Take macro-outcome $(1, 0, 0, 1)$: 1 H photon
at $\alpha$ in some frequency $k_\alpha$, 1 V photon at $\beta$ in some
frequency $l_\beta$. Tracking the BS amplitudes carefully:

- **Term 2** has the C-side H photon (with delay phase $e^{i\omega_{k_\alpha}\tau}$)
  going to $\alpha$ and the A-side V photon going to $\beta$. The B-side
  photon is V (Bell pair was $|VV\rangle$). Net contribution:

$$
\frac{\alpha\, e^{i\omega_{k_\alpha}\tau}}{2\sqrt{2}\,M}\, |V\rangle_B.
$$

- **Term 3** has the C-side V photon (delay phase
  $e^{i\omega_{l_\beta}\tau}$) at $\beta$ and the A-side H photon at
  $\alpha$. The B-side photon is H (Bell pair was $|HH\rangle$). Net
  contribution:

$$
\frac{\beta\, e^{i\omega_{l_\beta}\tau}}{2\sqrt{2}\,M}\, |H\rangle_B.
$$

Both contribute coherently to the *same* αβ Fock outcome (because the
αβ-side polarization composition matches), even though they put the B
photon in orthogonal polarization wavepackets. The unnormalized Bob ket
is

$$
|B\rangle^{(k_\alpha, l_\beta)}_\text{unnorm}
= \frac{1}{2\sqrt{2}\,M}\Bigl[
  \alpha\, e^{i\omega_{k_\alpha}\tau}\, |V\rangle_B
+ \beta\,  e^{i\omega_{l_\beta}\tau}\, |H\rangle_B
\Bigr].
$$

Note the polarization "swap": $\alpha$ multiplies $|V\rangle_B$ and
$\beta$ multiplies $|H\rangle_B$ — exactly what an $X$ correction will
fix.

**Apply the correction and compute the fidelity contribution.** With
$X$ on Bob's polarization, $X|H\rangle_B = |V\rangle_B$ and vice versa,
so the corrected Bob state has $\alpha$ on $|H\rangle_B$ and $\beta$ on
$|V\rangle_B$ — matching the target $|\psi\rangle_B = \alpha|H\rangle_B + \beta|V\rangle_B$.
Equivalently, work with the uncorrected target
$|\psi_\text{eff}\rangle = X|\psi\rangle = \beta|H\rangle_B + \alpha|V\rangle_B$
and take the inner product:

$$
\langle\psi_\text{eff}\,|\,B\rangle^{(k_\alpha, l_\beta)}_\text{unnorm}
= \frac{1}{2\sqrt{2}\,M}\Bigl[
  |\alpha|^2\, e^{i\omega_{k_\alpha}\tau}
+ |\beta|^2\, e^{i\omega_{l_\beta}\tau}
\Bigr].
$$

The cross-terms $\alpha^*\beta\,\langle V|H\rangle$ and $\beta^*\alpha\,\langle H|V\rangle$
vanish, and what survives is real-positive in the magnitudes
$|\alpha|^2, |\beta|^2$ — the phase of $\alpha\beta$ never enters, which
is why the formula depends on $|\alpha|^2|\beta|^2$ alone.

**Squaring and summing over frequencies.** The inner-product magnitude
squared expands to

$$
\bigl|\langle\psi_\text{eff}\,|\,B\rangle^{(k_\alpha, l_\beta)}_\text{unnorm}\bigr|^2
= \frac{1}{8M^2}\Bigl[
|\alpha|^4 + |\beta|^4 + 2\,|\alpha|^2|\beta|^2\,\cos\bigl((k_\alpha - l_\beta)\Delta\omega\,\tau\bigr)
\Bigr],
$$

with the carrier $\omega_0$ canceling out of the cosine (only the
*difference* $\omega_{k_\alpha} - \omega_{l_\beta} = (k_\alpha - l_\beta)\Delta\omega$ remains).
Summing over the $M^2$ frequency pairs gives

$$
\sum_{k_\alpha, l_\beta} \cos\bigl((k_\alpha - l_\beta)\Delta\omega\,\tau\bigr)
= \Bigl|\sum_k e^{ik\Delta\omega\,\tau}\Bigr|^2
= D_N(\Delta\omega\,\tau)^2,
$$

so

$$
\sum_{k_\alpha, l_\beta} |\langle\psi_\text{eff}\,|\,B\rangle_\text{unnorm}|^2
= \frac{|\alpha|^4 + |\beta|^4}{8} + \frac{|\alpha|^2|\beta|^2 \, D_N^2}{4M^2}.
$$

**The other three macros give the same.** By the H↔V swap symmetry,
macro $(0, 1, 1, 0)$ (also corrected by $X$) has identical structure to
$(1, 0, 0, 1)$. By the $\alpha \leftrightarrow \beta$ port symmetry,
macros $(1, 1, 0, 0)$ and $(0, 0, 1, 1)$ — corrected by $ZX$ and $XZ$
respectively — produce conditional Bob kets with rearranged signs, but
the fidelity contribution after correction is *the same closed form*.
(Pauli matrices being self-adjoint, $|\langle\psi|U|\phi\rangle|^2 = |\langle U^\dagger\psi|\phi\rangle|^2$
is invariant under $U \leftrightarrow U^\dagger$, and the two-Pauli
compositions $ZX$ vs $XZ$ differ only by a global sign.)

So each macro contributes an equal share to numerator and denominator:

$$
\text{numerator} = 4 \cdot \Bigl[\frac{|\alpha|^4 + |\beta|^4}{8} + \frac{|\alpha|^2|\beta|^2 \, D_N^2}{4M^2}\Bigr]
= \frac{|\alpha|^4 + |\beta|^4}{2} + \frac{|\alpha|^2|\beta|^2 \, D_N^2}{M^2},
$$

$$
\text{denominator} \;=\; P_\text{post-sel} \;=\; \tfrac{1}{2}.
$$

**Final formula.** Dividing,

$$
F(\tau) = (|\alpha|^4 + |\beta|^4) + \frac{2|\alpha|^2|\beta|^2 \, D_N^2}{M^2}.
$$

Use $|\alpha|^4 + |\beta|^4 = 1 - 2|\alpha|^2|\beta|^2$ (from
$|\alpha|^2 + |\beta|^2 = 1$) and the $\mathrm{HOM}$ definition
$\mathrm{HOM}(\tau) = (1/2)(1 - D_N^2/M^2)$ to rewrite as

$$
\boxed{\;F(\tau) \;=\; 1 \;-\; 4\,|\alpha|^2|\beta|^2 \cdot \mathrm{HOM}(\tau)\;}
$$

**Reading the formula.** The fidelity loss is the HOM dip *modulated by
the coherence content* $|\alpha|^2|\beta|^2$ of the input on the H/V
basis:

- $|\psi\rangle = |H\rangle$ or $|V\rangle$: $|\alpha|^2|\beta|^2 = 0$,
  so $F(\tau) = 1$ for all $\tau$. Computational-basis states are
  immune — the Bell measurement preserves the bit even when BS
  interference is destroyed, because the C and A photons are simply
  routed (no HOM interference is needed).
- Equator states $(|H\rangle + e^{i\varphi}|V\rangle)/\sqrt{2}$:
  $|\alpha|^2|\beta|^2 = 1/4$, so $F(\tau) = 1 - \mathrm{HOM}(\tau)$,
  reaching $F = 1/2$ at full distinguishability — the worst-case drop
  for any input qubit. The phase $\varphi$ never enters, so $|+\rangle$,
  $|-\rangle$, $|+i\rangle$, $|-i\rangle$ all behave identically.
- Asymmetric states like $0.6|H\rangle + 0.8|V\rangle$ have
  $|\alpha|^2|\beta|^2 = 0.36 \cdot 0.64 = 0.2304$, so the dip depth is
  $4 \cdot 0.2304 \cdot \mathrm{HOM}_{\max} = 4 \cdot 0.2304 \cdot 0.5 \approx 0.461$,
  giving $F_\text{min} \approx 0.539$ at full distinguishability.

The carrier $\omega_0$ doesn't appear anywhere in the final formula —
just like the basic HOM dip, only the *spectral spread* $\Delta\omega$
controls the timescale of the fidelity drop. This is the same physics
as `coincidence_number_states.py`, just dressed up with polarization
labels and a Bell-state correction.
