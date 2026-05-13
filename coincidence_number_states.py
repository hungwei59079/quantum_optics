"""
Single 50/50 beam splitter with two single-photon pulsed inputs (HOM dip).

Each beam carries one photon distributed coherently across the same M
frequency modes used in the coherent script:
    |ψ⟩_beam = Σ_k c_k a†_k |0⟩,    c_k = 1/√M,  k = −(M−1)/2..+(M−1)/2 .
The temporal wavepacket has the same Dirichlet-kernel envelope as the
coherent pulse train; the photon is just delocalized inside that envelope.

A 50/50 BS couples each frequency pair (signal-k, reference-k); one beam
carries delay τ, applied as a per-mode phase exp(i ω_k τ) via lab.Rgate.
Working through the BS algebra for two single-photon wavepackets gives a
clean Hong-Ou-Mandel result that depends only on the pulse-overlap term:
    P_coinc(τ) = (1/2) · [1 − D_M(Δω τ)² / M²]
where D_M(x) = sin(M x/2) / sin(x/2) is the Dirichlet kernel.  In
contrast to the coherent case, the carrier ω₀ drops out — there are no
fringes.  P_coinc = 0 at τ = 0 (perfect bunching, the HOM dip) and rises
to the asymptote 1/2 as the pulses stop overlapping.

We cross-check this analytic prediction against an mrmustard simulation
that builds the explicit 2M-mode two-photon Fock-superposition input
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
def single_beam_pulse_ket(M, mode_cutoff):
    """One-photon wavepacket  |ψ⟩ = Σ_k (1/√M) a†_k |0⟩  on M modes.

    Sized at the *output* cutoff (≥ 3, never just 2): the input only fills
    the n=1 slots, but the BS can bunch both photons into one mode (n=2)
    and those slots must already exist in the Fock space the state is
    defined on — otherwise mrmustard silently truncates that mass and the
    coincidence rate comes out inflated by 1/M.
    """
    c = 1.0 / np.sqrt(M)
    ket = np.zeros((mode_cutoff,) * M, dtype=complex)
    for k in range(M):
        idx = [0] * M
        idx[k] = 1
        ket[tuple(idx)] = c
    return ket


def two_beam_input_ket(M, mode_cutoff):
    """Tensor product of two identical one-photon wavepackets."""
    psi = single_beam_pulse_ket(M, mode_cutoff)
    return np.tensordot(psi, psi, axes=0)


# --------------------------------------------------------------------
# Analytic HOM dip
# --------------------------------------------------------------------
def coincidence_analytic(tau, M):
    """P_coinc(τ) = ½ [1 − D_M(Δω τ)²/M²].   No carrier dependence."""
    D = dirichlet_kernel(DELTA_OMEGA * tau, M)
    return 0.5 * (1.0 - (D / M) ** 2)


# --------------------------------------------------------------------
# Mr Mustard simulation (explicit Fock-state propagation)
# --------------------------------------------------------------------
def coincidence_mrmustard(tau, M, cutoff=3):
    """Coincidence probability via direct Fock-space evaluation.

    Builds the 2M-mode two-photon ket, applies a per-mode delay phase
    on the second beam (Rgate), then a 50/50 BS for each (signal-k,
    reference-k) frequency pair, and reads joint photon-number probabilities
    at the requested cutoff.  Output modes can hold up to 2 photons (HOM
    bunching when both photons share a frequency), so cutoff ≥ 3.
    """
    omegas = mode_frequencies(M)
    total_modes = 2 * M

    state = lab.State(ket=two_beam_input_ket(M, mode_cutoff=cutoff))

    ops = []
    # Delay on the reference beam
    for k in range(M):
        ops.append(lab.Rgate(angle=float(omegas[k] * tau))[M + k])
    # 50/50 BS coupling each frequency pair
    for k in range(M):
        ops.append(lab.BSgate(theta=np.pi / 4)[k, M + k])

    out = state >> lab.Circuit(ops)
    probs = np.asarray(out.fock_probabilities(cutoffs=[cutoff] * total_modes))

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
demo_M = 5
print(f"== HOM-dip snapshot (M = {demo_M} modes per beam) ==")
print(f"{'τ':>12} {'P_coinc':>10}   asymptote = 1/2")
for tau in [0.0, T_CAR / 2, T_CAR, T_REP / 16, T_REP / 8, T_REP / 4, T_REP / 2, T_REP]:
    P = coincidence_analytic(tau, demo_M)
    print(f"{tau:+12.4f} {P:10.4f}")
print()

# --- mrmustard cross-check at several M ------------------------------
# 3^(2M) Fock-tensor size limits M: M=3 → 729, M=5 → 59 049, M=7 → 4.78 M.
mm_cutoff = 3
mm_M_values = [3, 5, 7]
mm_taus = np.linspace(-0.6 * T_REP, 0.6 * T_REP, 31)
mm_results = {}

for mm_M in mm_M_values:
    print(f"== mrmustard cross-check (M = {mm_M} modes/beam, Fock cutoff = {mm_cutoff}) ==")
    print(f"{'τ':>12} {'analytic':>12} {'mrmustard':>12} {'Δ':>12}")
    P_arr = np.empty_like(mm_taus)
    for i, tau in enumerate(mm_taus):
        P_mm = coincidence_mrmustard(tau, mm_M, cutoff=mm_cutoff)
        P_an = coincidence_analytic(tau, mm_M)
        P_arr[i] = P_mm
        print(f"{tau:+12.4f} {P_an:12.6f} {P_mm:12.6f} {P_mm-P_an:+12.2e}")
    mm_results[mm_M] = P_arr
    print()

# --- plots ------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(15, 4.4))


# (a) HOM dip vs delay for several M, plus mrmustard markers (color-matched)
ax = axes[0]
tau_grid = np.linspace(-0.6 * T_REP, 0.6 * T_REP, 4001)
M_curves = [3, 5, 7, 15]
M_to_color = dict(zip(M_curves, plt.cm.viridis(np.linspace(0.15, 0.85, len(M_curves)))))
for M in M_curves:
    ax.plot(tau_grid, [coincidence_analytic(t, M) for t in tau_grid],
            color=M_to_color[M], lw=1.4, label=f"M = {M}")
mm_markers = {3: "o", 5: "s", 7: "^"}
for mm_M in mm_M_values:
    ax.plot(mm_taus, mm_results[mm_M], mm_markers[mm_M],
            color=M_to_color[mm_M], markersize=7,
            markeredgecolor="black", markeredgewidth=0.8,
            linestyle="none", label=f"mm M = {mm_M}")
ax.axhline(0.5, color="gray", linestyle="--", linewidth=0.8)
for k in [-1, 0, 1]:
    ax.axvline(k * T_REP, color="gray", linestyle=":", linewidth=0.7)
ax.set_xlabel(r"delay  $\tau$")
ax.set_ylabel(r"$P_\mathrm{coinc}$")
ax.set_title(f"(a) HOM dip vs delay   (mrmustard cutoff = {mm_cutoff})")
ax.set_ylim(-0.02, 0.6)
ax.legend(fontsize=8, loc="lower right", ncol=2)
ax.grid(alpha=0.3)

# (b) rescaled overlay: dips collapse when we scale τ by M
ax = axes[1]
u_grid = np.linspace(-3.0, 3.0, 4001)
for M, c in zip(M_curves, plt.cm.viridis(np.linspace(0.15, 0.85, len(M_curves)))):
    # rescale: u = M Δω τ / (2π)  →  τ = 2π u / (M Δω)
    tau_resc = 2 * np.pi * u_grid / (M * DELTA_OMEGA)
    ax.plot(u_grid, [coincidence_analytic(t, M) for t in tau_resc],
            color=c, lw=1.4, label=f"M = {M}")
ax.axhline(0.5, color="gray", linestyle="--", linewidth=0.8)
ax.set_xlabel(r"rescaled delay  $u = M\,\Delta\omega\,\tau / 2\pi$")
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
