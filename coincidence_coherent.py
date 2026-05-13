"""
Single 50/50 beam splitter with two pulsed coherent inputs (mode-locked).

Each beam is a comb of M frequency modes  ω_k = ω₀ + k·Δω,
k = −(M−1)/2..+(M−1)/2  (M odd), every mode prepared in the same coherent
state |α⟩.  Two scales appear:
    pulse repetition  T_rep = 2π/Δω,    envelope (slow) scale
    carrier period    T_car = 2π/ω₀,    fringe   (fast) scale.
For real pulsed lasers the ratio ω₀/Δω is >~ 10³ — we keep it moderate in
this script so the carrier fringes stay visible against the envelope, but
the qualitative picture is the same.

A 50/50 BS acts on each frequency pair independently.  One beam carries
delay τ, applied as a per-mode phase  exp(i ω_k τ)  via lab.Rgate, which
sends |α⟩ → |α e^{i φ}⟩.  Coherent in / coherent out, so per-port amplitudes
are
    α_X,k = α (1 ± e^{i ω_k τ}) / √2 ,
giving mean photon counts
    n̄_A(τ) = α² M + α² · cos(ω₀ τ) · D_M(Δω τ),
    n̄_B(τ) = α² M − α² · cos(ω₀ τ) · D_M(Δω τ),
where D_M(x) = sin(M x/2) / sin(x/2) is the Dirichlet kernel — the slow
envelope set by pulse overlap.  Frequency modes are independent Poissons on
each port, so the coincidence rate is
    P_coinc(τ) = (1 − e^{−n̄_A}) · (1 − e^{−n̄_B}).

We cross-check this against an mrmustard simulation that propagates the
2M-mode coherent state through the circuit, with a Fock cutoff to
truncate the (infinite) coherent series.
"""

import numpy as np
import matplotlib.pyplot as plt

from mrmustard import math as mm_math

mm_math.change_backend("tensorflow")  # PNR / Fock probs need the TF backend

import mrmustard.lab as lab

from coincidence_utils import (
    DELTA_OMEGA, OMEGA_0, T_REP, T_CAR,
    mode_frequencies, pulse_envelope,
)


ALPHA = 0.7  # coherent amplitude per mode (real)


# --------------------------------------------------------------------
# Analytic outputs (coherent in / coherent out)
# --------------------------------------------------------------------
def output_means(tau, M, alpha=ALPHA):
    """Mean photon counts on the two output ports."""
    omegas = mode_frequencies(M)
    phase = np.exp(1j * omegas * tau)
    nA = float(np.sum(np.abs(alpha * (1 + phase) / np.sqrt(2)) ** 2))
    nB = float(np.sum(np.abs(alpha * (1 - phase) / np.sqrt(2)) ** 2))
    return nA, nB


def coincidence(tau, M, alpha=ALPHA):
    nA, nB = output_means(tau, M, alpha)
    return (1.0 - np.exp(-nA)) * (1.0 - np.exp(-nB))


# --------------------------------------------------------------------
# mrmustard simulation (explicit Fock-cutoff truncation of the coherent series)
# --------------------------------------------------------------------
def coincidence_mrmustard(tau, M, alpha=ALPHA, cutoff=5):
    """Coincidence probability via direct Fock-space evaluation.

    Builds a 2M-mode state — modes 0..M-1 are the signal beam, modes
    M..2M-1 the reference — applies the per-mode delay phase to the
    reference, then a 50/50 BS on each frequency pair, and reads the
    joint photon-number probability with the requested cutoff.
    """
    omegas = mode_frequencies(M)
    total_modes = 2 * M

    ops = []
    # |α⟩ on every mode  (Dgate on vacuum: x = Re α, y = Im α; ⟨n⟩ = x² + y²)
    for k in range(total_modes):
        ops.append(lab.Dgate(x=alpha, y=0.0)[k])
    # delay on the reference beam
    for k in range(M):
        ops.append(lab.Rgate(angle=float(omegas[k] * tau))[M + k])
    # 50/50 BS coupling each (signal-k, reference-k) frequency pair
    for k in range(M):
        ops.append(lab.BSgate(theta=np.pi / 4)[k, M + k])

    state = lab.Vacuum(num_modes=total_modes) >> lab.Circuit(ops)
    probs = np.asarray(state.fock_probabilities(cutoffs=[cutoff] * total_modes))

    # Total photons on each port via the photon-count index arrays
    idx = np.indices(probs.shape)
    nA_total = idx[:M].sum(axis=0)
    nB_total = idx[M:].sum(axis=0)

    # Inclusion–exclusion: P(coinc) = 1 − P(no A) − P(no B) + P(no anywhere)
    P_no_A  = float(probs[nA_total == 0].sum())
    P_no_B  = float(probs[nB_total == 0].sum())
    P_no_AB = float(probs[(nA_total == 0) & (nB_total == 0)].sum())
    return 1.0 - P_no_A - P_no_B + P_no_AB


# ====================================================================
# Numbers + plots
# ====================================================================
print(f"Per-mode coherent amplitude  α  = {ALPHA}   (⟨n⟩/mode = {ALPHA**2:.3f})")
print(f"Mode spacing                 Δω = {DELTA_OMEGA}   (T_rep = 2π/Δω = {T_REP:.4f})")
print(f"Carrier                      ω₀ = {OMEGA_0}   (T_car = 2π/ω₀ = {T_CAR:.4f},  ω₀/Δω = {OMEGA_0/DELTA_OMEGA:.0f})")
print()

# --- snapshot at a few representative delays --------------------------
demo_M = 5
print(f"== Output snapshot (M = {demo_M} modes per beam, α = {ALPHA}) ==")
print(f"{'τ':>12} {'⟨n_A⟩':>10} {'⟨n_B⟩':>10} {'P_coinc':>10}")
for tau in [0.0, 0.5 * T_CAR, T_CAR, T_REP / 8, T_REP / 4, T_REP / 2, T_REP]:
    nA, nB = output_means(tau, demo_M)
    P = coincidence(tau, demo_M)
    print(f"{tau:+12.4f} {nA:10.4f} {nB:10.4f} {P:10.4f}")
print()

# --- mrmustard cross-check at a handful of delays ---------------------
mm_M, mm_cutoff = 3, 5
mm_taus = np.linspace(-0.5 * T_REP, 0.5 * T_REP, 5)
print(f"== mrmustard cross-check (M = {mm_M} modes/beam, Fock cutoff = {mm_cutoff}) ==")
print(f"{'τ':>12} {'analytic':>12} {'mrmustard':>12} {'Δ':>12}")
mm_P = np.empty_like(mm_taus)
for i, tau in enumerate(mm_taus):
    P_mm = coincidence_mrmustard(tau, mm_M, cutoff=mm_cutoff)
    P_an = coincidence(tau, mm_M)
    mm_P[i] = P_mm
    print(f"{tau:+12.4f} {P_an:12.6f} {P_mm:12.6f} {P_mm-P_an:+12.2e}")
print()

# --- plots ------------------------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(15, 4.4))

# (a) single-beam pulse train: envelope only (the carrier drops out of |E|²)
ax = axes[0]
t_grid = np.linspace(-0.5 * T_REP, 1.5 * T_REP, 4000)
for M in [3, 7, 15]:
    ax.plot(t_grid, pulse_envelope(t_grid, M), label=f"M = {M}")
for k in range(2):
    ax.axvline(k * T_REP, color="gray", linestyle=":", linewidth=0.7)
ax.set_xlabel(r"time  $t$")
ax.set_ylabel("intensity (peak-normalized)")
ax.set_title("(a) single-beam pulse train")
ax.legend(fontsize=9)
ax.grid(alpha=0.3)

# (b) coincidence vs τ over one envelope period — fringes visible underneath
ax = axes[1]
tau_grid = np.linspace(-0.6 * T_REP, 0.6 * T_REP, 8001)
M_curves = [5, 9, 15]
for M, c in zip(M_curves, plt.cm.viridis(np.linspace(0.15, 0.85, len(M_curves)))):
    ax.plot(tau_grid, [coincidence(t, M) for t in tau_grid],
            color=c, lw=0.6, label=f"M = {M}")
ax.plot(mm_taus, mm_P, "kx", markersize=8, mew=2,
        label=f"mrmustard (M = {mm_M}, cutoff = {mm_cutoff})")
for k in [-1, 0, 1]:
    ax.axvline(k * T_REP, color="gray", linestyle=":", linewidth=0.7)
ax.set_xlabel(r"delay  $\tau$")
ax.set_ylabel(r"$P_\mathrm{coinc}$")
ax.set_title(rf"(b) coincidence vs delay   (ω₀/Δω = {OMEGA_0/DELTA_OMEGA:.0f})")
ax.set_ylim(-0.02, 1.02)
ax.legend(fontsize=8, loc="lower center")
ax.grid(alpha=0.3)

# (c) zoom to a few carrier periods near τ = 0 — clean fringe pattern
ax = axes[2]
zoom_window = 5 * T_CAR
tau_zoom = np.linspace(-zoom_window, zoom_window, 2001)
zoom_M = 9
ax.plot(tau_zoom, [coincidence(t, zoom_M) for t in tau_zoom],
        color="C2", lw=1.4, label=f"M = {zoom_M}")
for k in range(-5, 6):
    ax.axvline(k * T_CAR, color="gray", linestyle=":", linewidth=0.5)
ax.set_xlabel(r"delay  $\tau$")
ax.set_ylabel(r"$P_\mathrm{coinc}$")
ax.set_title(rf"(c) carrier fringes (zoom: ±5 T_car ≈ ±{zoom_window:.3f})")
ax.set_ylim(-0.02, 1.02)
ax.legend(fontsize=9)
ax.grid(alpha=0.3)

plt.suptitle(rf"50/50 BS with two mode-locked coherent pulse trains  "
             rf"($\alpha={ALPHA}$, $\omega_0/\Delta\omega={OMEGA_0/DELTA_OMEGA:.0f}$)")
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("coincidence.png", dpi=150)
plt.show()
print("Plot saved to coincidence.png")
