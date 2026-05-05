"""
Single 50/50 beam splitter with two single-photon pulsed inputs (HOM dip).

Each beam carries one photon distributed coherently across the same N+1
frequency modes used in the coherent script:
    |ψ⟩_beam = Σ_k c_k a†_k |0⟩,    c_k = 1/√(N+1),  k = −N/2..+N/2 .
The temporal wavepacket has the same Dirichlet-kernel envelope as the
coherent pulse train; the photon is just delocalized inside that envelope.

A 50/50 BS couples each frequency pair (signal-k, reference-k); one beam
carries delay τ, applied as a per-mode phase exp(i ω_k τ) via lab.Rgate.
Working through the BS algebra for two single-photon wavepackets gives a
clean Hong-Ou-Mandel result that depends only on the pulse-overlap term:
    P_coinc(τ) = (1/2) · [1 − D_N(Δω τ)² / (N+1)²]
where D_N(x) = sin((N+1)x/2) / sin(x/2) is the Dirichlet kernel.  In
contrast to the coherent case, the carrier ω₀ drops out — there are no
fringes.  P_coinc = 0 at τ = 0 (perfect bunching, the HOM dip) and rises
to the asymptote 1/2 as the pulses stop overlapping.

We cross-check this analytic prediction against an mrmustard simulation
that builds the explicit 2(N+1)-mode two-photon Fock-superposition input
and reads the joint photon-number distribution at the BS output.
"""

import numpy as np
import matplotlib.pyplot as plt

from mrmustard import math as mm_math

mm_math.change_backend("tensorflow")  # PNR / Fock probs need the TF backend

import mrmustard.lab as lab

from coincidence_utils import (
    DELTA_OMEGA, OMEGA_0, T_REP, T_CAR,
    mode_frequencies, dirichlet_kernel, pulse_envelope,
)


# --------------------------------------------------------------------
# Single-photon wavepacket builders
# --------------------------------------------------------------------
def single_beam_pulse_ket(N, mode_cutoff):
    """One-photon wavepacket  |ψ⟩ = Σ_k (1/√M) a†_k |0⟩  on M = N+1 modes.

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


# --------------------------------------------------------------------
# Analytic HOM dip
# --------------------------------------------------------------------
def coincidence_analytic(tau, N):
    """P_coinc(τ) = ½ [1 − D_N(Δω τ)²/(N+1)²].   No carrier dependence."""
    D = dirichlet_kernel(DELTA_OMEGA * tau, N)
    return 0.5 * (1.0 - (D / (N + 1)) ** 2)


# --------------------------------------------------------------------
# Mr Mustard simulation (explicit Fock-state propagation)
# --------------------------------------------------------------------
def coincidence_mrmustard(tau, N, cutoff=3):
    """Coincidence probability via direct Fock-space evaluation.

    Builds the 2(N+1)-mode two-photon ket, applies a per-mode delay phase
    on the second beam (Rgate), then a 50/50 BS for each (signal-k,
    reference-k) frequency pair, and reads joint photon-number probabilities
    at the requested cutoff.  Output modes can hold up to 2 photons (HOM
    bunching when both photons share a frequency), so cutoff ≥ 3.
    """
    omegas = mode_frequencies(N)
    M = len(omegas)             # N+1 modes per beam
    N_total = 2 * M

    state = lab.State(ket=two_beam_input_ket(N, mode_cutoff=cutoff))

    ops = []
    # Delay on the reference beam
    for k in range(M):
        ops.append(lab.Rgate(angle=float(omegas[k] * tau))[M + k])
    # 50/50 BS coupling each frequency pair
    for k in range(M):
        ops.append(lab.BSgate(theta=np.pi / 4)[k, M + k])

    out = state >> lab.Circuit(ops)
    probs = np.asarray(out.fock_probabilities(cutoffs=[cutoff] * N_total))

    # Total photons = 2 (BS conserves number), so
    #   P_coinc = 1 − P(both photons at A) − P(both at B)
    #          = 1 − P(n_B_total = 0) − P(n_A_total = 0)
    idx = np.indices(probs.shape)
    nA_total = idx[:M].sum(axis=0)
    nB_total = idx[M:].sum(axis=0)
    P_no_A = float(probs[nA_total == 0].sum())
    P_no_B = float(probs[nB_total == 0].sum())
    return 1.0 - P_no_A - P_no_B


# ====================================================================
# Numbers + plots
# ====================================================================
print(f"Mode spacing  Δω = {DELTA_OMEGA}   (T_rep = 2π/Δω = {T_REP:.4f})")
print(f"Carrier       ω₀ = {OMEGA_0}    (T_car = 2π/ω₀ = {T_CAR:.4f},  ω₀/Δω = {OMEGA_0/DELTA_OMEGA:.0f})")
print()

# --- snapshot at a few representative delays --------------------------
demo_N = 4
print(f"== HOM-dip snapshot (N = {demo_N} → {demo_N + 1} modes per beam) ==")
print(f"{'τ':>12} {'P_coinc':>10}   asymptote = 1/2")
for tau in [0.0, T_CAR / 2, T_CAR, T_REP / 16, T_REP / 8, T_REP / 4, T_REP / 2, T_REP]:
    P = coincidence_analytic(tau, demo_N)
    print(f"{tau:+12.4f} {P:10.4f}")
print()

# --- mrmustard cross-check at several N ------------------------------
mm_cutoff = 3
mm_N_values = [2, 4, 6]
mm_taus = np.linspace(-0.6 * T_REP, 0.6 * T_REP, 31)
mm_results = {}

for mm_N in mm_N_values:
    print(f"== mrmustard cross-check (N = {mm_N} → {mm_N+1} modes/beam, Fock cutoff = {mm_cutoff}) ==")
    print(f"{'τ':>12} {'analytic':>12} {'mrmustard':>12} {'Δ':>12}")
    P_arr = np.empty_like(mm_taus)
    for i, tau in enumerate(mm_taus):
        P_mm = coincidence_mrmustard(tau, mm_N, cutoff=mm_cutoff)
        P_an = coincidence_analytic(tau, mm_N)
        P_arr[i] = P_mm
        print(f"{tau:+12.4f} {P_an:12.6f} {P_mm:12.6f} {P_mm-P_an:+12.2e}")
    mm_results[mm_N] = P_arr
    print()

# --- plots ------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(15, 4.4))


# (b) HOM dip vs delay for several N, plus mrmustard markers (color-matched)
ax = axes[0]
tau_grid = np.linspace(-0.6 * T_REP, 0.6 * T_REP, 4001)
N_curves = [2, 4, 6, 14]
N_to_color = dict(zip(N_curves, plt.cm.viridis(np.linspace(0.15, 0.85, len(N_curves)))))
for N in N_curves:
    ax.plot(tau_grid, [coincidence_analytic(t, N) for t in tau_grid],
            color=N_to_color[N], lw=1.4, label=f"N = {N}")
mm_markers = {2: "o", 4: "s", 6: "^"}
for mm_N in mm_N_values:
    ax.plot(mm_taus, mm_results[mm_N], mm_markers[mm_N],
            color=N_to_color[mm_N], markersize=7,
            markeredgecolor="black", markeredgewidth=0.8,
            linestyle="none", label=f"mm N = {mm_N}")
ax.axhline(0.5, color="gray", linestyle="--", linewidth=0.8)
for k in [-1, 0, 1]:
    ax.axvline(k * T_REP, color="gray", linestyle=":", linewidth=0.7)
ax.set_xlabel(r"delay  $\tau$")
ax.set_ylabel(r"$P_\mathrm{coinc}$")
ax.set_title(f"(a) HOM dip vs delay   (mrmustard cutoff = {mm_cutoff})")
ax.set_ylim(-0.02, 0.6)
ax.legend(fontsize=8, loc="lower right", ncol=2)
ax.grid(alpha=0.3)

# (c) rescaled overlay: dips collapse when we scale τ by (N+1)
ax = axes[1]
u_grid = np.linspace(-3.0, 3.0, 4001)
for N, c in zip(N_curves, plt.cm.viridis(np.linspace(0.15, 0.85, len(N_curves)))):
    # rescale: u = (N+1) Δω τ / (2π)  →  τ = 2π u / ((N+1) Δω)
    tau_resc = 2 * np.pi * u_grid / ((N + 1) * DELTA_OMEGA)
    ax.plot(u_grid, [coincidence_analytic(t, N) for t in tau_resc],
            color=c, lw=1.4, label=f"N = {N}")
ax.axhline(0.5, color="gray", linestyle="--", linewidth=0.8)
ax.set_xlabel(r"rescaled delay  $u = (N+1)\,\Delta\omega\,\tau / 2\pi$")
ax.set_ylabel(r"$P_\mathrm{coinc}$")
ax.set_title(r"(b) dips collapse onto a universal shape")
ax.set_ylim(-0.02, 0.6)
ax.legend(fontsize=8, loc="lower right")
ax.grid(alpha=0.3)

plt.suptitle(rf"50/50 BS with two single-photon pulsed inputs  "
             rf"($\omega_0/\Delta\omega = {OMEGA_0/DELTA_OMEGA:.0f}$)")
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("coincidence_number_states.png", dpi=150)
plt.show()
print("Plot saved to coincidence_number_states.png")
