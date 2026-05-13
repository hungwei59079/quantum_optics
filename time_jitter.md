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

## Mode operators and BS transformations

To do the explicit algebra term by term we need names for the post-BS
output modes. Define
$c^\dagger_{P,k}$ to create a photon at output port $\alpha$ with
polarization $P$ and frequency $k$, and $d^\dagger_{P,k}$ likewise for
port $\beta$. (The port labels $\alpha, \beta$ here are the *spatial*
output labels and are a different role from the qubit amplitudes
$\alpha, \beta$ in $|\psi\rangle_C$ — port labels appear only as operator
subscripts, qubit amplitudes only as standalone prefactors.)

The Heisenberg-picture transformations for the BS, combined with the
delay phase $\phi_k = \omega_k\,\tau$ on every C mode:

$$
a^\dagger_{C,P,k} \;\longrightarrow\; \frac{e^{i\phi_k}}{\sqrt{2}}\,\bigl(c^\dagger_{P,k} + d^\dagger_{P,k}\bigr),
\qquad
a^\dagger_{A,P,k} \;\longrightarrow\; \frac{1}{\sqrt{2}}\,\bigl(c^\dagger_{P,k} - d^\dagger_{P,k}\bigr),
$$

applied independently for each polarization $P$ and each frequency $k$.
Bob-side operators $a^\dagger_{B,P,k}$ are untouched. With these in
hand, the recipe for each Term is: expand every $|P\rangle_X$ into its
$M = N+1$ frequency modes, substitute, then read off the output state.

## Term 1: $\alpha\,|HHH\rangle/\sqrt{2}$ — same-pol HOM at H

Expanding the wavepackets:

$$
|HHH\rangle \;=\; \frac{1}{M^{3/2}} \sum_{k_C, k_A, k_B}
a^\dagger_{C,H,k_C}\, a^\dagger_{A,H,k_A}\, a^\dagger_{B,H,k_B}\,|0\rangle.
$$

Apply delay+BS:

$$
|HHH\rangle \;\longrightarrow\;
\frac{1}{2\,M^{3/2}} \sum_{k_C, k_A, k_B} e^{i\phi_{k_C}}
\bigl(c^\dagger_{H,k_C} + d^\dagger_{H,k_C}\bigr)\bigl(c^\dagger_{H,k_A} - d^\dagger_{H,k_A}\bigr)\,a^\dagger_{B,H,k_B}\,|0\rangle.
$$

Expand the BS product:

$$
\bigl(c^\dagger_{H,k_C} + d^\dagger_{H,k_C}\bigr)\bigl(c^\dagger_{H,k_A} - d^\dagger_{H,k_A}\bigr)
\;=\;
c^\dagger_{H,k_C} c^\dagger_{H,k_A}
\;-\; c^\dagger_{H,k_C} d^\dagger_{H,k_A}
\;+\; d^\dagger_{H,k_C} c^\dagger_{H,k_A}
\;-\; d^\dagger_{H,k_C} d^\dagger_{H,k_A}.
$$

Four output configurations: two coincidence terms ($c^\dagger d^\dagger$
and $d^\dagger c^\dagger$, one photon per port), and two bunching terms
($c^\dagger c^\dagger$ at $\alpha$, $-d^\dagger d^\dagger$ at $\beta$).

**The HOM cancellation.** Both photons are H, so they are
indistinguishable in their polarization mode — once they leave the BS,
no photon carries a label "I came from C" or "I came from A". The
operator pair

$$
(k_C = k_c,\,k_A = k_d)\,:\;\; -c^\dagger_{H,k_c} d^\dagger_{H,k_d},
\qquad
(k_C = k_d,\,k_A = k_c)\,:\;\; +d^\dagger_{H,k_d} c^\dagger_{H,k_c}
= +c^\dagger_{H,k_c} d^\dagger_{H,k_d}
$$

both contribute to the *same* output Fock state
$|1_{H,k_c}\rangle_\alpha\,|1_{H,k_d}\rangle_\beta$ — and they
interfere. (The BS operators commute since they act on different modes
and ports.) Collecting the two contributions and relabeling dummy
indices in the second:

$$
\sum_{k_C, k_A} e^{i\phi_{k_C}}\bigl(-c^\dagger_{H,k_C} d^\dagger_{H,k_A} + c^\dagger_{H,k_A} d^\dagger_{H,k_C}\bigr)
\;=\;
\sum_{k_c, k_d}\,\bigl(e^{i\phi_{k_d}} - e^{i\phi_{k_c}}\bigr)\,c^\dagger_{H,k_c} d^\dagger_{H,k_d}.
$$

This is exactly the multi-mode HOM-dip structure (compare lines 222–238
of [fock_space_HOM_dip_Gemini.md](fock_space_HOM_dip_Gemini.md)). With
Term 1's prefactor $\alpha/\sqrt{2}$ included, and the trivial B-side
sum over $k_B$ kept explicit, the coincidence part of Term 1 in the
post-BS state is

$$
|\Psi^{(1)}_{\text{coinc}}\rangle
\;=\;
\frac{\alpha}{2\sqrt{2}\,M^{3/2}}\sum_{k_c, k_d, k_B}
\bigl(e^{i\phi_{k_d}} - e^{i\phi_{k_c}}\bigr)\,
c^\dagger_{H,k_c} d^\dagger_{H,k_d}\,a^\dagger_{B,H,k_B}\,|0\rangle.
$$

The bunching part is the other two operator terms:
$+c^\dagger_{H,k_C} c^\dagger_{H,k_A}$ (both H at $\alpha$) and
$-d^\dagger_{H,k_C} d^\dagger_{H,k_A}$ (both H at $\beta$) — same
polarization, one arm.

## Term 4: $-\beta\,|VVV\rangle/\sqrt{2}$ — same-pol HOM at V

Identical to Term 1 with $H \to V$ and prefactor $-\beta/\sqrt{2}$:

$$
|\Psi^{(4)}_{\text{coinc}}\rangle
\;=\;
-\frac{\beta}{2\sqrt{2}\,M^{3/2}}\sum_{k_c, k_d, k_B}
\bigl(e^{i\phi_{k_d}} - e^{i\phi_{k_c}}\bigr)\,
c^\dagger_{V,k_c} d^\dagger_{V,k_d}\,a^\dagger_{B,V,k_B}\,|0\rangle.
$$

The bunching part puts both V photons at the same port — same
polarization, one arm.

## Term 2: $-\alpha\,|HVV\rangle/\sqrt{2}$ — different polarization sectors

Now the C photon is H and the A photon is V — they sit in different
polarization sectors and go through independent BSs that share no
operators:

$$
|HVV\rangle \;=\; \frac{1}{M^{3/2}} \sum_{k_C, k_A, k_B}
a^\dagger_{C,H,k_C}\, a^\dagger_{A,V,k_A}\, a^\dagger_{B,V,k_B}\,|0\rangle,
$$

$$
|HVV\rangle \;\longrightarrow\;
\frac{1}{2\,M^{3/2}}\sum_{k_C, k_A, k_B} e^{i\phi_{k_C}}
\bigl(c^\dagger_{H,k_C} + d^\dagger_{H,k_C}\bigr)\bigl(c^\dagger_{V,k_A} - d^\dagger_{V,k_A}\bigr)\,a^\dagger_{B,V,k_B}\,|0\rangle.
$$

Expand the BS product:

$$
\bigl(c^\dagger_{H,k_C} + d^\dagger_{H,k_C}\bigr)\bigl(c^\dagger_{V,k_A} - d^\dagger_{V,k_A}\bigr)
=
c^\dagger_{H,k_C} c^\dagger_{V,k_A}
- c^\dagger_{H,k_C} d^\dagger_{V,k_A}
+ d^\dagger_{H,k_C} c^\dagger_{V,k_A}
- d^\dagger_{H,k_C} d^\dagger_{V,k_A}.
$$

The four output configurations are now labeled by *polarization-port pairs*:

- $+c^\dagger_{H,k_C} c^\dagger_{V,k_A}$ — HV at $\alpha$, frequencies $(k_C, k_A)$ — *1-arm, diff pol*
- $-c^\dagger_{H,k_C} d^\dagger_{V,k_A}$ — H at $\alpha$ freq $k_C$, V at $\beta$ freq $k_A$ — *coinc, diff pol*
- $+d^\dagger_{H,k_C} c^\dagger_{V,k_A}$ — H at $\beta$ freq $k_C$, V at $\alpha$ freq $k_A$ — *coinc, diff pol*
- $-d^\dagger_{H,k_C} d^\dagger_{V,k_A}$ — HV at $\beta$, frequencies $(k_C, k_A)$ — *1-arm, diff pol*

**No HOM cancellation.** Unlike Term 1, the two photons are now
distinguishable by polarization — one is always the H photon (from C,
carrying the delay phase), the other always the V photon (from A, no
phase). Each $(k_C, k_A)$ pair therefore lands in its *own* output Fock
state, and **different $(k_C, k_A)$ pairs do not interfere**.

The immediate consequence: the delay phase $e^{i\phi_{k_C}}$ rides on
each amplitude as a per-Fock-state global phase and **disappears
entirely when we take $|\cdot|^2$**. Term 2 (and by symmetry Term 3)
will give *$\tau$-independent* probabilities for every detection event.

## Term 3: $\beta\,|VHH\rangle/\sqrt{2}$ — symmetric to Term 2

C is V (with delay), A is H. Same structure:

$$
|VHH\rangle \;\longrightarrow\;
\frac{1}{2\,M^{3/2}}\sum_{k_C, k_A, k_B} e^{i\phi_{k_C}}
\bigl(c^\dagger_{V,k_C} + d^\dagger_{V,k_C}\bigr)\bigl(c^\dagger_{H,k_A} - d^\dagger_{H,k_A}\bigr)\,a^\dagger_{B,H,k_B}\,|0\rangle.
$$

Same four output configurations as Term 2 (HV coincidences and HV
bunching), all diff-pol, all $\tau$-independent in probability.

## Why the four Terms don't interfere

Reading off the post-BS Fock supports from the four derivations above:

| Term | $\vert\psi\rangle_{\text{in}}$ | $\alpha\beta$ side after BS | B side |
|------|---------------------------|---------------------------|--------|
| 1 | $\alpha\,\vert HHH\rangle$  | two H photons         | one H photon |
| 2 | $-\alpha\,\vert HVV\rangle$ | one H + one V photon  | one V photon |
| 3 | $\beta\,\vert VHH\rangle$   | one H + one V photon  | one H photon |
| 4 | $-\beta\,\vert VVV\rangle$  | two V photons         | one V photon |

Any pair of Terms differs either on the B side polarization or on the
$\alpha\beta$-port polarization composition. The BS preserves
polarization-mode photon number (the H and V sectors evolve completely
independently), so the four post-BS supports are **pairwise orthogonal
in Fock space**. There is no cross-Term interference, and totals add
classically across the four contributions.

## $P_{\text{coinc, same}}(\tau) = \mathrm{HOM}(\tau)/2$

Only Terms 1 and 4 contribute (the same-polarization sectors at
$\alpha\beta$). Take Term 1. The amplitude for each output Fock state
$|1_{H,k_c}\rangle_\alpha\,|1_{H,k_d}\rangle_\beta\,|1_{H,k_B}\rangle_B$
is

$$
\text{amp}^{(1)}_{k_c, k_d, k_B}
\;=\;
\frac{\alpha}{2\sqrt{2}\,M^{3/2}}\,\bigl(e^{i\phi_{k_d}} - e^{i\phi_{k_c}}\bigr).
$$

Squaring, using $|e^{ix} - e^{iy}|^2 = 2 - 2\cos(x - y)$, and noting
that $\phi_{k_d} - \phi_{k_c} = (k_d - k_c)\,\Delta\omega\,\tau$ (the
carrier $\omega_0$ cancels in the difference):

$$
\bigl|\text{amp}^{(1)}\bigr|^2
\;=\;
\frac{|\alpha|^2}{8\,M^3}\,\bigl(2 - 2\cos((k_d - k_c)\Delta\omega\,\tau)\bigr).
$$

Different Fock states are orthogonal, so the total Term-1 coincidence
probability is the straight sum over $(k_c, k_d, k_B)$, each running
over $M$ values:

$$
P^{(1)}_{\text{coinc, same}}
\;=\;
\sum_{k_c, k_d, k_B}\frac{|\alpha|^2}{8\,M^3}\,\bigl(2 - 2\cos((k_d - k_c)\Delta\omega\,\tau)\bigr)
\;=\;
\frac{|\alpha|^2}{4\,M^2}\,\Bigl(M^2 - \sum_{k_c, k_d}\cos((k_d - k_c)\Delta\omega\,\tau)\Bigr).
$$

The double cosine sum collapses to a Dirichlet kernel squared:

$$
\sum_{k_c, k_d}\cos\bigl((k_d - k_c)\Delta\omega\,\tau\bigr)
\;=\;
\Re\Bigl[\Bigl(\sum_{k_d} e^{i k_d \Delta\omega\tau}\Bigr)\Bigl(\sum_{k_c} e^{-i k_c \Delta\omega\tau}\Bigr)\Bigr]
\;=\;
\Bigl|\sum_k e^{i k \Delta\omega\,\tau}\Bigr|^2
\;=\;
D_N(\Delta\omega\,\tau)^2.
$$

So

$$
P^{(1)}_{\text{coinc, same}}
\;=\;
\frac{|\alpha|^2}{4}\,\Bigl(1 - \frac{D_N^2}{M^2}\Bigr)
\;=\;
\frac{|\alpha|^2}{2}\,\mathrm{HOM}(\tau).
$$

By the H↔V symmetry between Terms 1 and 4, $P^{(4)}_{\text{coinc, same}} = |\beta|^2\,\mathrm{HOM}(\tau)/2$.
The Fock supports of Terms 1 and 4 are orthogonal (H photons vs V
photons at $\alpha\beta$), so total adds:

$$
P_{\text{coinc, same}}(\tau)
\;=\;
\frac{(|\alpha|^2 + |\beta|^2)\,\mathrm{HOM}(\tau)}{2}
\;=\;
\frac{\mathrm{HOM}(\tau)}{2}.
$$

The $|\alpha|^2 + |\beta|^2 = 1$ collapse is what makes the answer
independent of the input qubit's amplitudes. At $\tau = 0$ this is zero
(perfect HOM bunching, every event ends up at one port); at full
distinguishability $\mathrm{HOM} = 1/2$ it saturates at $1/4$.

## $P_{\text{coinc, diff}}(\tau) = 1/4$

Only Terms 2 and 3 contribute. Take Term 2. Its two coincidence
configurations contribute amplitudes (each with a per-Fock-state global
delay phase that vanishes in the squared modulus)

$$
\text{amp}^{(2)}_{\text{H@}\alpha,\text{V@}\beta}
\;=\;
-\,\frac{\alpha\,e^{i\phi_{k_C}}}{2\sqrt{2}\,M^{3/2}},
\qquad
\text{amp}^{(2)}_{\text{H@}\beta,\text{V@}\alpha}
\;=\;
+\,\frac{\alpha\,e^{i\phi_{k_C}}}{2\sqrt{2}\,M^{3/2}},
$$

each multiplied by Bob's $a^\dagger_{B,V,k_B}\,|0\rangle$. Each triple
$(k_C, k_A, k_B)$ labels a distinct output Fock state, and the two
configurations (H@α,V@β) vs (H@β,V@α) also produce different Fock
states — so **there is no interference**, and

$$
\bigl|\text{amp}^{(2)}\bigr|^2 \;=\; \frac{|\alpha|^2}{8\,M^3}.
$$

The two configurations contribute $M^3$ Fock states each (one per
$(k_C, k_A, k_B)$ value), giving

$$
P^{(2)}_{\text{coinc, diff}}
\;=\;
2 \cdot M^3 \cdot \frac{|\alpha|^2}{8\,M^3}
\;=\;
\frac{|\alpha|^2}{4}.
$$

By H↔V symmetry between Terms 2 and 3, $P^{(3)}_{\text{coinc, diff}} = |\beta|^2/4$.
Terms 2 and 3 are orthogonal in the output Fock space (Term 2 has Bob
in a V wavepacket, Term 3 has Bob in H), so the probabilities add:

$$
P_{\text{coinc, diff}}(\tau)
\;=\;
\frac{|\alpha|^2 + |\beta|^2}{4}
\;=\;
\frac{1}{4}.
$$

**Independent of $\tau$**: with H and V photons distinguishable, the
delay phase has no interfering partner to play against, and timing
jitter leaves these outcomes alone.

## $P_{\text{1-arm, same}}(\tau) = (1 - \mathrm{HOM}(\tau))/2$

This is the complementary part of Terms 1 and 4 — both photons at the
same output port with the same polarization (both H@α, both H@β, both
V@α, or both V@β). Photon-number conservation gives the answer without
having to rewrite the bunching algebra: Term 1's total weight in the
post-BS state equals its weight in the input, $|\alpha|^2/2$, and its
coincidence part is $|\alpha|^2\,\mathrm{HOM}(\tau)/2$, so

$$
P^{(1)}_{\text{1-arm, same}}
\;=\;
\frac{|\alpha|^2}{2} - \frac{|\alpha|^2\,\mathrm{HOM}(\tau)}{2}
\;=\;
\frac{|\alpha|^2\,(1 - \mathrm{HOM}(\tau))}{2}.
$$

Term 4 likewise gives $|\beta|^2 (1 - \mathrm{HOM})/2$. Adding:

$$
P_{\text{1-arm, same}}(\tau)
\;=\;
\frac{(|\alpha|^2 + |\beta|^2)\,(1 - \mathrm{HOM}(\tau))}{2}
\;=\;
\frac{1 - \mathrm{HOM}(\tau)}{2}.
$$

At $\tau = 0$ this is $1/2$ (perfect HOM bunching: every same-pol event
ends up at one port); at full distinguishability it falls to $1/4$,
matching the diff-pol channels.

## $P_{\text{1-arm, diff}}(\tau) = 1/4$

Same logic as $P_{\text{coinc, diff}}$ applied to the bunching part of
Terms 2 and 3. Term 2's two bunching configurations
($+c^\dagger_{H} c^\dagger_{V}$ at $\alpha$, $-d^\dagger_{H} d^\dagger_{V}$ at $\beta$)
each contribute $M^3$ Fock states with
$|\text{amp}|^2 = |\alpha|^2/(8\,M^3)$ and no interference. Summed,
$P^{(2)}_{\text{1-arm, diff}} = |\alpha|^2/4$, and Term 3 gives
$|\beta|^2/4$, so

$$
P_{\text{1-arm, diff}}(\tau)
\;=\;
\frac{|\alpha|^2 + |\beta|^2}{4}
\;=\;
\frac{1}{4}.
$$

$\tau$-independent for the same reason as $P_{\text{coinc, diff}}$.

**Sanity check.** Sum of the four categories at every $\tau$:
$\mathrm{HOM}/2 + 1/4 + (1 - \mathrm{HOM})/2 + 1/4 = 1$. ✓ All the
$\tau$-dependence lives in the same-polarization channels (Terms 1 and
4, with their HOM cancellation), and these are exactly the channels the
BS Bell-measurement uses to distinguish $\Psi^{\pm}$ from $\Phi^{\pm}$.

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
