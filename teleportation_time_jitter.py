"""
Bell-measurement detection statistics with timing jitter on the input qubit.

Mode layout (M frequency modes per polarization, M odd):
    C: input qubit          modes [0..2M-1]   (H: 0..M-1,    V: M..2M-1)
    A: Alice (Bell pair)     modes [2M..4M-1]  (H: 2M..3M-1,  V: 3M..4M-1)
    B: Bob   (Bell pair)     modes [4M..6M-1]  (H: 4M..5M-1,  V: 5M..6M-1)

The Bell-measurement BS couples (C_P,k <-> A_P,k) for each polarization P
and frequency k.  A delay τ on the C qubit puts a per-mode phase
exp(i ω_k τ) on every C mode (both polarizations together — the qubit is
delayed as one).

Input state — each |P⟩_X is a single photon in equal superposition across
M frequency modes (mode-locked picture, c_k = 1/√M):

    |ψ⟩_C   = α|H⟩_C + β|V⟩_C
    |Φ⁻⟩_AB = (|HH⟩_AB - |VV⟩_AB) / √2
    |Ψ⟩_in  = |ψ⟩_C ⊗ |Φ⁻⟩_AB

Expanding gives four polarization terms whose post-BS Fock supports are
pairwise orthogonal (distinguished by B-side polarization plus αβ-port
polarization composition), so they don't interfere.  Working out each
term gives clean closed-form detection probabilities, INDEPENDENT of
α, β:

    P(both arms, same pol)  = HOM(τ) / 2 = (1/4)[1 − D_M(Δω τ)²/M²]
    P(both arms, diff pol)  = 1/4                                     (constant)
    P(one  arm, same pol)   = (1 − HOM(τ)) / 2
    P(one  arm, diff pol)   = 1/4                                     (constant)

where  HOM(τ) = (1/2)[1 − D_M(Δω τ)²/M²]  is the standard HOM dip, with
the M-term Dirichlet kernel  D_M(x) = sin(M x/2) / sin(x/2).
The τ-dependence lives entirely in the *same-polarization* channels —
exactly the channels the BS Bell-measurement uses to distinguish Bell
states, so this is where timing jitter erodes the teleportation.

We cross-check at M = 3 with an explicit mrmustard simulation: build the
full 6M-mode input ket with mixed cutoffs (3 for C/A modes that can
bunch post-BS, 2 for the untouched B modes), propagate through the BS
circuit, and aggregate joint Fock probabilities by photon counts at each
polarization-port.  Larger M is infeasible (3^20·2^10 ≈ 3.5 T elements
at M = 5) but the analytic formula covers the full sweep.
"""

import numpy as np
import matplotlib.pyplot as plt

from mrmustard import math as mm_math

mm_math.change_backend("tensorflow")  # PNR / Fock probs need the TF backend

import mrmustard.lab as lab

from coincidence_utils import (
    DELTA_OMEGA, OMEGA_0, T_REP, T_CAR,
    mode_frequencies, dirichlet_kernel,
)


# ----------------------------------------------------------------------
# Analytic detection-probability formulas
# ----------------------------------------------------------------------
def hom_dip(tau, M):
    """Standard HOM dip:  (1/2)[1 − D_M(Δω τ)²/M²]  with  D_M(x) = sin(M x/2)/sin(x/2)."""
    D = dirichlet_kernel(DELTA_OMEGA * tau, M)
    return 0.5 * (1.0 - (D / M) ** 2)


def detection_probs_analytic(tau, M):
    """Return dictionary of analytic detection probabilities."""
    H = hom_dip(tau, M)
    return {
        "coinc, same pol": H / 2,
        "coinc, diff pol": 0.25,
        "1-arm, same pol": (1.0 - H) / 2,
        "1-arm, diff pol": 0.25,
    }


# ----------------------------------------------------------------------
# Mode layout helper
# ----------------------------------------------------------------------
def _mode_idx(qubit, polarization, freq, M):
    """Global mode index for (qubit ∈ {C,A,B}, pol ∈ {H,V}, freq ∈ 0..M-1)."""
    qubit_offset = {"C": 0, "A": 2 * M, "B": 4 * M}[qubit]
    pol_offset = {"H": 0, "V": M}[polarization]
    return qubit_offset + pol_offset + freq


# ----------------------------------------------------------------------
# Input ket builder
# ----------------------------------------------------------------------
def build_input_ket(alpha, beta, M, ca_cutoff=3, b_cutoff=2):
    """
    Build  |Ψ⟩_in = (α|H⟩_C + β|V⟩_C) ⊗ (|HH⟩_AB − |VV⟩_AB) / √2.

    Mixed cutoffs: C/A modes at ca_cutoff (≥ 3 — BS can bunch both photons
    into one mode); B modes at b_cutoff (≥ 2 — never modified).  Returns a
    numpy array of shape (ca_cutoff,)*(4M) + (b_cutoff,)*(2M).
    """
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


# ----------------------------------------------------------------------
# Joint Fock probabilities → 4 detection-event probabilities
# ----------------------------------------------------------------------
def event_probabilities(probs, M):
    """Aggregate the joint Fock-probability tensor into the 4 categories."""
    # Marginalize over B modes (the last 2M axes)
    probs_AB = probs
    for _ in range(2 * M):
        probs_AB = probs_AB.sum(axis=-1)

    # idx_arr is a tensor of shape (4M, ca_cutoff, ca_cutoff, ..., ca_cutoff)
    # Mathematically, idx_arr[i, a_0, a_1, ..., a_{4M-1}] = a_i (the photon number in mode i).
    idx_arr = np.indices(probs_AB.shape)

    # Each of below sums is a tensor of the same shape as probs_AB, (3, 3, 3,...).
    n_aH = idx_arr[0:M].sum(axis=0) # e.g., n_aH[a_0, a_1, ..., a_{4M-1}] = a_0 + a_1 + ... + a_{M-1} (total photons in A_H modes)
    n_aV = idx_arr[M:2*M].sum(axis=0)
    n_bH = idx_arr[2*M:3*M].sum(axis=0)
    n_bV = idx_arr[3*M:4*M].sum(axis=0)

    # Total photons in output ports A and B
    n_a = n_aH + n_aV
    n_b = n_bH + n_bV

    # Create Boolean event masks based on total photon counts
    coinc   = (n_a == 1) & (n_b == 1)
    bunch_a = (n_a == 2) & (n_b == 0)
    bunch_b = (n_a == 0) & (n_b == 2)

    same_coinc = coinc & (((n_aH == 1) & (n_bH == 1)) | ((n_aV == 1) & (n_bV == 1)))
    diff_coinc = coinc & (((n_aH == 1) & (n_bV == 1)) | ((n_aV == 1) & (n_bH == 1)))
    same_a = bunch_a & ((n_aH == 2) | (n_aV == 2))
    diff_a = bunch_a & ((n_aH == 1) & (n_aV == 1))
    same_b = bunch_b & ((n_bH == 2) | (n_bV == 2))
    diff_b = bunch_b & ((n_bH == 1) & (n_bV == 1))

    # Use the Boolean masks to filter and sum the actual probability values
    return {
        "coinc, same pol": float(probs_AB[same_coinc].sum()),
        "coinc, diff pol": float(probs_AB[diff_coinc].sum()),
        "1-arm, same pol": float(probs_AB[same_a | same_b].sum()),
        "1-arm, diff pol": float(probs_AB[diff_a | diff_b].sum()),
    }


# ----------------------------------------------------------------------
# mrmustard simulation
# ----------------------------------------------------------------------
def detection_probs_mrmustard(alpha, beta, tau, M, ca_cutoff=3, b_cutoff=2):
    omegas = mode_frequencies(M)

    state = lab.State(ket=build_input_ket(alpha, beta, M, ca_cutoff, b_cutoff))

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

    return event_probabilities(probs, M)


# ======================================================================
# Numbers + plots
# ======================================================================
print(f"Mode spacing  Δω = {DELTA_OMEGA}   (T_rep = 2π/Δω = {T_REP:.4f})")
print(f"Carrier       ω₀ = {OMEGA_0}    (T_car = 2π/ω₀ = {T_CAR:.4f}, ω₀/Δω = {OMEGA_0/DELTA_OMEGA:.0f})")
print()

# parameters
alpha, beta = 1.0 / np.sqrt(2), 1.0 / np.sqrt(2)   # any (α, β) — formula is α,β-independent
mm_M = 3
mm_taus = np.array([T_REP * k / 16 for k in range(-8, 9)])

# --- mrmustard cross-check ---------------------------------------------
categories = list(detection_probs_analytic(0, mm_M).keys())
print(f"== mrmustard cross-check (M = {mm_M} modes/pol/qubit, "
      f"|ψ⟩ = (|H⟩+|V⟩)/√2,  ca_cutoff = 3, b_cutoff = 2) ==")
print(f"{'τ':>10}  " + "  ".join(f"{c:>20}" for c in categories))
mm_probs = np.empty((len(mm_taus), 4))
for i, tau in enumerate(mm_taus):
    p_an = detection_probs_analytic(tau, mm_M)
    p_mm = detection_probs_mrmustard(alpha, beta, tau, mm_M)
    mm_probs[i] = list(p_mm.values())
    print(f"{tau:+10.4f}  " + "  ".join(
        f"{a:7.4f} / {m:7.4f}" for a, m in zip(p_an.values(), p_mm.values())
    ))
print("(each cell:  analytic / mrmustard)")
print()

# --- plots -----------------------------------------------------------
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']

fig, axes = plt.subplots(1, 2, figsize=(13, 6.0))

# (a) all 4 detection probs vs τ for M = mm_M, with mrmustard markers
ax = axes[0]
tau_grid = np.linspace(-0.6 * T_REP, 0.6 * T_REP, 4001)
ps_a = np.array([list(detection_probs_analytic(t, mm_M).values()) for t in tau_grid]).T
colors_cat  = ["tab:blue", "tab:cyan", "tab:red", "tab:orange"]
markers_cat = ["o", "s", "^", "D"]
for p, lbl, c in zip(ps_a, categories, colors_cat):
    ax.plot(tau_grid, p, color=c, lw=1.4, label=lbl)
for i, (mk, c) in enumerate(zip(markers_cat, colors_cat)):
    ax.plot(mm_taus, mm_probs[:, i], mk, color=c,
            markeredgecolor="black", markeredgewidth=0.8, markersize=7,
            linestyle="none")
ax.axhline(0.25, color="gray", linestyle="--", linewidth=0.7)
for k in [-1, 0, 1]:
    ax.axvline(k * T_REP, color="gray", linestyle=":", linewidth=0.7)
ax.set_xlim(-4.0, 4.0)
ax.set_xlabel(r"delay  $\tau$", fontsize=24, fontweight='bold')
ax.set_ylabel("probability", fontsize=24, fontweight='bold')
ax.set_title(f"(a) detection events vs delay\n(M = {mm_M};  markers = mrmustard)", fontsize=20, fontweight='bold', pad=12)
ax.set_ylim(-0.02, 0.55)
ax.set_yticks(np.arange(0.0, 0.6, 0.1))
ax.tick_params(axis='both', which='major', labelsize=22)
ax.legend(fontsize=14, loc="upper right")
ax.grid(alpha=0.3)

# (b) P(both arms, same pol) vs τ for several M — the τ-dependent signal
ax = axes[1]
M_curves = [3, 5, 7, 15]
M_to_color = dict(zip(M_curves, plt.cm.viridis(np.linspace(0.15, 0.85, len(M_curves)))))
for M in M_curves:
    p_same = np.array([detection_probs_analytic(t, M)["coinc, same pol"] for t in tau_grid])
    ax.plot(tau_grid, p_same, color=M_to_color[M], lw=1.4, label=f"M = {M}")
ax.plot(mm_taus, mm_probs[:, 0], "o", color=M_to_color[mm_M],
        markeredgecolor="black", markeredgewidth=0.8, markersize=7,
        linestyle="none", label=f"mm  M = {mm_M}")
ax.axhline(0.25, color="gray", linestyle="--", linewidth=0.7,
           label=r"asymptote 1/4")
for k in [-1, 0, 1]:
    ax.axvline(k * T_REP, color="gray", linestyle=":", linewidth=0.7)
ax.set_xlim(-4.0, 4.0)
ax.set_xlabel(r"delay  $\tau$", fontsize=24, fontweight='bold')
ax.set_ylabel(r"$P(\mathrm{both\ arms,\ same\ pol})$", fontsize=18, fontweight='bold')
ax.set_title("(b) τ-dependent same-pol coincidence", fontsize=24, fontweight='bold', pad=12)
ax.set_ylim(-0.01, 0.30)
ax.set_yticks(np.arange(0.0, 0.35, 0.1))
ax.tick_params(axis='both', which='major', labelsize=22)
ax.legend(fontsize=14, loc="lower right")
ax.grid(alpha=0.3)

plt.suptitle(rf"Bell-measurement with input-qubit timing jitter  "
             rf"($\omega_0/\Delta\omega = {OMEGA_0/DELTA_OMEGA:.0f}$)", fontsize=26, fontweight='bold')
plt.tight_layout(rect=[0, 0, 1, 0.92], pad=1.0)
plt.savefig("results/teleportation_time_jitter.svg")
print("Plot saved to results/teleportation_time_jitter.png")
