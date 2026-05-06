"""
Bell-measurement detection statistics with timing jitter on the input qubit.

Mode layout (M = N+1 frequency modes per polarization):
    C: input qubit          modes [0..2M-1]   (H: 0..M-1,    V: M..2M-1)
    A: Alice (Bell pair)     modes [2M..4M-1]  (H: 2M..3M-1,  V: 3M..4M-1)
    B: Bob   (Bell pair)     modes [4M..6M-1]  (H: 4M..5M-1,  V: 5M..6M-1)

The Bell-measurement BS couples (C_P,k <-> A_P,k) for each polarization P
and frequency k.  A delay τ on the C qubit puts a per-mode phase
exp(i ω_k τ) on every C mode (both polarizations together — the qubit is
delayed as one).

Input state — each |P⟩_X is a single photon in equal superposition across
N+1 frequency modes (mode-locked picture, c_k = 1/√(N+1)):

    |ψ⟩_C   = α|H⟩_C + β|V⟩_C
    |Φ⁻⟩_AB = (|HH⟩_AB - |VV⟩_AB) / √2
    |Ψ⟩_in  = |ψ⟩_C ⊗ |Φ⁻⟩_AB

Expanding gives four polarization terms whose post-BS Fock supports are
pairwise orthogonal (distinguished by B-side polarization plus αβ-port
polarization composition), so they don't interfere.  Working out each
term gives clean closed-form detection probabilities, INDEPENDENT of
α, β:

    P(both arms, same pol)  = HOM(τ) / 2 = (1/4)[1 − D_N(Δω τ)²/(N+1)²]
    P(both arms, diff pol)  = 1/4                                     (constant)
    P(one  arm, same pol)   = (1 − HOM(τ)) / 2
    P(one  arm, diff pol)   = 1/4                                     (constant)

where  HOM(τ) = (1/2)[1 − D_N(Δω τ)²/(N+1)²]  is the standard HOM dip.
The τ-dependence lives entirely in the *same-polarization* channels —
exactly the channels the BS Bell-measurement uses to distinguish Bell
states, so this is where timing jitter erodes the teleportation.

We cross-check at N = 2 with an explicit mrmustard simulation: build the
full 6(N+1)-mode input ket with mixed cutoffs (3 for C/A modes that can
bunch post-BS, 2 for the untouched B modes), propagate through the BS
circuit, and aggregate joint Fock probabilities by photon counts at each
polarization-port.  Larger N is infeasible (3^20·2^10 ≈ 3.5 T elements
at N = 4) but the analytic formula covers the full sweep.
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
def hom_dip(tau, N):
    """Standard HOM dip:  (1/2)[1 − D_N(Δω τ)²/(N+1)²]."""
    D = dirichlet_kernel(DELTA_OMEGA * tau, N)
    return 0.5 * (1.0 - (D / (N + 1)) ** 2)


def detection_probs_analytic(tau, N):
    """Return (P_coinc_same, P_coinc_diff, P_1arm_same, P_1arm_diff)."""
    H = hom_dip(tau, N)
    return H / 2, 0.25, (1.0 - H) / 2, 0.25


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
def build_input_ket(alpha, beta, N, ca_cutoff=3, b_cutoff=2):
    """
    Build  |Ψ⟩_in = (α|H⟩_C + β|V⟩_C) ⊗ (|HH⟩_AB − |VV⟩_AB) / √2.

    Mixed cutoffs: C/A modes at ca_cutoff (≥ 3 — BS can bunch both photons
    into one mode); B modes at b_cutoff (≥ 2 — never modified).  Returns a
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


# ----------------------------------------------------------------------
# Joint Fock probabilities → 4 detection-event probabilities
# ----------------------------------------------------------------------
def event_probabilities(probs, N):
    """Aggregate the joint Fock-probability tensor into the 4 categories."""
    M = N + 1

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
    return (
        float(probs_AB[same_coinc].sum()),
        float(probs_AB[diff_coinc].sum()),
        float(probs_AB[same_a | same_b].sum()),
        float(probs_AB[diff_a | diff_b].sum()),
    )


# ----------------------------------------------------------------------
# mrmustard simulation
# ----------------------------------------------------------------------
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


# ======================================================================
# Numbers + plots
# ======================================================================
print(f"Mode spacing  Δω = {DELTA_OMEGA}   (T_rep = 2π/Δω = {T_REP:.4f})")
print(f"Carrier       ω₀ = {OMEGA_0}    (T_car = 2π/ω₀ = {T_CAR:.4f}, ω₀/Δω = {OMEGA_0/DELTA_OMEGA:.0f})")
print()

CATEGORIES = ["coinc, same pol", "coinc, diff pol", "1-arm, same pol", "1-arm, diff pol"]

# --- analytic snapshot at a representative N --------------------------
demo_N = 4
print(f"== Analytic detection probabilities (N = {demo_N} → {demo_N+1} modes/pol/qubit) ==")
print(f"{'τ':>10}  " + "  ".join(f"{c:>16}" for c in CATEGORIES))
for tau in [0.0, T_REP / 16, T_REP / 8, T_REP / 4, T_REP / 2, T_REP]:
    p = detection_probs_analytic(tau, demo_N)
    print(f"{tau:+10.4f}  " + "  ".join(f"{x:16.4f}" for x in p))
print()

# --- mrmustard cross-check at N = 2 -----------------------------------
alpha, beta = 1.0 / np.sqrt(2), 1.0 / np.sqrt(2)   # any (α, β) — formula is α,β-independent
mm_N = 2
mm_taus = np.array([0.0, T_REP / 8, T_REP / 4, T_REP / 2, T_REP])

print(f"== mrmustard cross-check (N = {mm_N} → {mm_N+1} modes/pol/qubit, "
      f"|ψ⟩ = (|H⟩+|V⟩)/√2,  ca_cutoff = 3, b_cutoff = 2) ==")
print(f"{'τ':>10}  " + "  ".join(f"{c:>20}" for c in CATEGORIES))
mm_probs = np.empty((len(mm_taus), 4))
for i, tau in enumerate(mm_taus):
    p_an = detection_probs_analytic(tau, mm_N)
    p_mm = detection_probs_mrmustard(alpha, beta, tau, mm_N)
    mm_probs[i] = p_mm
    print(f"{tau:+10.4f}  " + "  ".join(
        f"{a:7.4f} / {m:7.4f}" for a, m in zip(p_an, p_mm)
    ))
print("(each cell:  analytic / mrmustard)")
print()

# --- plots -----------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))

# (a) all 4 detection probs vs τ for N = mm_N, with mrmustard markers
ax = axes[0]
tau_grid = np.linspace(-0.6 * T_REP, 0.6 * T_REP, 4001)
ps_a = np.array([detection_probs_analytic(t, mm_N) for t in tau_grid]).T
colors_cat  = ["tab:blue", "tab:cyan", "tab:red", "tab:orange"]
markers_cat = ["o", "s", "^", "D"]
for p, lbl, c in zip(ps_a, CATEGORIES, colors_cat):
    ax.plot(tau_grid, p, color=c, lw=1.4, label=lbl)
for i, (mk, c) in enumerate(zip(markers_cat, colors_cat)):
    ax.plot(mm_taus, mm_probs[:, i], mk, color=c,
            markeredgecolor="black", markeredgewidth=0.8, markersize=7,
            linestyle="none")
ax.axhline(0.25, color="gray", linestyle="--", linewidth=0.7)
for k in [-1, 0, 1]:
    ax.axvline(k * T_REP, color="gray", linestyle=":", linewidth=0.7)
ax.set_xlabel(r"delay  $\tau$")
ax.set_ylabel("probability")
ax.set_title(f"(a) detection events vs delay  (N = {mm_N};  markers = mrmustard)")
ax.set_ylim(-0.02, 0.55)
ax.legend(fontsize=8, loc="center right")
ax.grid(alpha=0.3)

# (b) P(both arms, same pol) vs τ for several N — the τ-dependent signal
ax = axes[1]
N_curves = [2, 4, 6, 14]
N_to_color = dict(zip(N_curves, plt.cm.viridis(np.linspace(0.15, 0.85, len(N_curves)))))
for N in N_curves:
    p_same = np.array([detection_probs_analytic(t, N)[0] for t in tau_grid])
    ax.plot(tau_grid, p_same, color=N_to_color[N], lw=1.4, label=f"N = {N}")
ax.plot(mm_taus, mm_probs[:, 0], "o", color=N_to_color[mm_N],
        markeredgecolor="black", markeredgewidth=0.8, markersize=7,
        linestyle="none", label=f"mm  N = {mm_N}")
ax.axhline(0.25, color="gray", linestyle="--", linewidth=0.7,
           label=r"asymptote $1/4$")
for k in [-1, 0, 1]:
    ax.axvline(k * T_REP, color="gray", linestyle=":", linewidth=0.7)
ax.set_xlabel(r"delay  $\tau$")
ax.set_ylabel(r"$P(\mathrm{both\ arms,\ same\ pol})$")
ax.set_title("(b) τ-dependent same-pol coincidence")
ax.set_ylim(-0.01, 0.30)
ax.legend(fontsize=8, loc="lower right")
ax.grid(alpha=0.3)

plt.suptitle(rf"Bell-measurement with input-qubit timing jitter  "
             rf"($\omega_0/\Delta\omega = {OMEGA_0/DELTA_OMEGA:.0f}$)")
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("teleportation_time_jitter.png", dpi=150)
plt.show()
print("Plot saved to teleportation_time_jitter.png")
