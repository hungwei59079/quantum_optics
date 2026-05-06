"""
Teleportation fidelity vs input-qubit timing jitter.

Builds on `teleportation_time_jitter.py` by completing the protocol:
  1. Project onto Bell-state-uniquely-identifying detection outcomes
     (the "diff pol" outcomes — coincidence with HV split, or 1-arm with
     HV bunched).  Outcomes that bunch HH/VV at one arm are ambiguous
     between Φ⁺ and Φ⁻, so we post-select against them.  Post-selection
     probability is exactly 1/2, independent of τ.
  2. Apply Bob's Pauli correction for that outcome (resource = |Φ⁻⟩_AB):
         (1, 0, 0, 1) "1H@α, 1V@β":   X        ← Ψ⁻
         (0, 1, 1, 0) "1V@α, 1H@β":   X        ← Ψ⁻
         (1, 1, 0, 0) "1H+1V@α, 0@β": X then Z ← Ψ⁺  (ZX as a single op)
         (0, 0, 1, 1) "0@α, 1H+1V@β": Z then X ← Ψ⁺  (XZ)
  3. Compute fidelity between Bob's corrected reduced density matrix and
     the ideal target — the same wavepacket-shape qubit |ψ⟩_B on Bob's
     2(N+1) modes.  Both target and Bob's actual state are *multi-mode*,
     so the fidelity is the multi-mode overlap, not just a polarization
     2×2 trace.

Working through the BS algebra term by term (only Terms 2 = HVV and
Term 3 = VHH contribute to "diff pol" outcomes; the four post-selected
macros all give the same form under H↔V or α↔β symmetries) yields:

    F(τ) = 1 − 4 |α|² |β|² · HOM(τ)
         = 1 − 2 |α|² |β|² · (1 − D_N(Δω τ)² / (N+1)²)

where  HOM(τ) = (1/2)[1 − D_N(Δω τ)²/(N+1)²]  is the standard HOM dip.

Notes:
  * Computational-basis states |H⟩, |V⟩ have |α|²|β|² = 0 and stay at
    F = 1 for any delay — the Bell measurement preserves the bit even
    when the BS interference is destroyed.
  * Equator states (|H⟩ + e^{iφ}|V⟩)/√2 have |α|²|β|² = 1/4 and feel the
    full HOM dip: F = 1 − HOM(τ), reaching F = 1/2 at full distinguishability.
  * The carrier ω₀ drops out; only Δω · τ matters (same as the basic HOM dip).

We cross-check at N = 2 by building the explicit 6(N+1)-mode post-BS ket
in mrmustard, slicing on each post-selected αβ Fock outcome, and summing
|⟨U|ψ_target⟩ | B_unnorm⟩|² over outcomes.
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

# parameters
alpha, beta = 1.0 / np.sqrt(2), 1.0 / np.sqrt(2)   # state to teleport
mm_N = 2
mm_taus = np.array([0.0, T_REP / 8, T_REP / 4, T_REP / 2, T_REP])


# ----------------------------------------------------------------------
# Analytic formulas
# ----------------------------------------------------------------------
def hom_dip(tau, N):
    """Standard HOM dip:  (1/2)[1 − D_N(Δω τ)²/(N+1)²]."""
    D = dirichlet_kernel(DELTA_OMEGA * tau, N)
    return 0.5 * (1.0 - (D / (N + 1)) ** 2)


def fidelity_analytic(alpha, beta, tau, N):
    """F(τ) = 1 − 4|α|²|β|² · HOM(τ).

    Post-selected (1/2 efficiency), with the right Pauli correction for each
    of the four diff-pol outcomes (resource = |Φ⁻⟩_AB).  Only |α|²|β|² enters,
    so the phase of α/β and individual magnitudes are irrelevant.
    """
    return 1.0 - 4.0 * (abs(alpha) ** 2) * (abs(beta) ** 2) * hom_dip(tau, N)


# ----------------------------------------------------------------------
# Mode layout helper
# ----------------------------------------------------------------------
def _mode_idx(qubit, polarization, freq, M):
    """Global mode index for (qubit ∈ {C,A,B}, pol ∈ {H,V}, freq ∈ 0..M-1)."""
    qubit_offset = {"C": 0, "A": 2 * M, "B": 4 * M}[qubit]
    pol_offset = {"H": 0, "V": M}[polarization]
    return qubit_offset + pol_offset + freq


# ----------------------------------------------------------------------
# Input ket builder (same as teleportation_time_jitter.py)
# ----------------------------------------------------------------------
def build_input_ket(alpha, beta, N, ca_cutoff=3, b_cutoff=2):
    """|Ψ⟩_in = (α|H⟩_C + β|V⟩_C) ⊗ (|HH⟩_AB − |VV⟩_AB)/√2 in mixed-cutoff Fock."""
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
# Bob's target ket (multi-mode single-photon polarization wavepacket)
# ----------------------------------------------------------------------
def target_ket(alpha, beta, N):
    """|ψ_target⟩_B = α|H⟩_B + β|V⟩_B with the same wavepacket as the input C qubit.

    Returned as a Fock-basis array of shape (2,)*(2(N+1)) over Bob's H,V freq modes
    (axes 0..M-1 are H, axes M..2M-1 are V).
    """
    M = N + 1
    n_modes = 2 * M
    ket = np.zeros((2,) * n_modes, dtype=complex)
    c = 1.0 / np.sqrt(M)
    for k in range(M):
        idx = [0] * n_modes
        idx[k] = 1
        ket[tuple(idx)] = alpha * c
    for k in range(M):
        idx = [0] * n_modes
        idx[M + k] = 1
        ket[tuple(idx)] = beta * c
    return ket


# ----------------------------------------------------------------------
# Pauli operators on Bob's polarization (acting on the multi-mode ket)
# ----------------------------------------------------------------------
def apply_X_to_bob(ket, N):
    """X = polarization swap.  Transpose H-block ↔ V-block axes."""
    M = N + 1
    perm = list(range(M, 2 * M)) + list(range(0, M))
    return np.transpose(ket, perm)


def apply_Z_to_bob(ket, N):
    """Z = +1 on H components, −1 on V components.

    For our single-photon ket: V-component identifier = (any V mode has n=1).
    """
    M = N + 1
    idx_arr = np.indices(ket.shape)
    n_V = idx_arr[M:2 * M].sum(axis=0)
    sign = np.where(n_V % 2 == 1, -1.0, 1.0)
    return ket * sign


def apply_correction(ket, ops_tuple, N):
    """Apply a sequence of Pauli ops in tuple order to Bob's ket.

    Note: Pauli matrices are Hermitian and self-inverse, so applying U vs U†
    differs only by a global sign on some basis components — same |amplitude|²
    in the fidelity.  Tuple order matches teleportation_utils.py convention.
    """
    out = ket
    for op in ops_tuple:
        if op == "X":
            out = apply_X_to_bob(out, N)
        elif op == "Z":
            out = apply_Z_to_bob(out, N)
        else:
            raise ValueError(f"Unknown Pauli op {op!r}")
    return out


# ----------------------------------------------------------------------
# Post-BS ket via mrmustard
# ----------------------------------------------------------------------
def post_BS_ket(alpha, beta, tau, N, ca_cutoff=3, b_cutoff=2):
    """Run |Ψ⟩_in through (delay on C) ∘ (BS_H, BS_V per frequency) and
    return the full post-BS ket as a numpy array."""
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
    return np.asarray(out.ket(cutoffs=cutoffs))


# ----------------------------------------------------------------------
# Enumerate αβ Fock outcomes within a polarization-port macro
# ----------------------------------------------------------------------
def alpha_beta_outcomes(n_aH, n_aV, n_bH, n_bV, M):
    """Yield αβ index tuples (length 4M) consistent with the polarization-port counts.

    Each polarization-port has at most 1 photon in our post-selected macros, so
    we iterate over which frequency mode holds the photon.
    """
    def ways(n, M):
        if n == 0:
            yield (0,) * M
        elif n == 1:
            for k in range(M):
                t = [0] * M
                t[k] = 1
                yield tuple(t)
        else:
            raise NotImplementedError(f"n = {n} per polarization-port not supported")

    for aH in ways(n_aH, M):
        for aV in ways(n_aV, M):
            for bH in ways(n_bH, M):
                for bV in ways(n_bV, M):
                    yield aH + aV + bH + bV


# ----------------------------------------------------------------------
# Post-selected Bell-measurement table (resource = |Φ⁻⟩_AB)
# ----------------------------------------------------------------------
POSTSEL_MACROS = [
    ((1, 0, 0, 1), ("X",)),       # Ψ⁻
    ((0, 1, 1, 0), ("X",)),       # Ψ⁻
    ((1, 1, 0, 0), ("X", "Z")),   # Ψ⁺  (apply X first, then Z)
    ((0, 0, 1, 1), ("Z", "X")),   # Ψ⁺  (apply Z first, then X)
]


# ----------------------------------------------------------------------
# Mr Mustard fidelity
# ----------------------------------------------------------------------
def fidelity_mrmustard(alpha, beta, tau, N, ca_cutoff=3, b_cutoff=2):
    """Post-selected, post-correction multi-mode fidelity from the explicit ket.

    For each post-selected αβ Fock outcome (k_α, l_β):
        |B_unnorm⟩  = ⟨αβ_outcome | Ψ_BS⟩       (slice into the post-BS ket)
        ψ_eff       = U |ψ_target⟩               (Pauli applied — see note in apply_correction)
        contribution to numerator   = |⟨ψ_eff | B_unnorm⟩|²
        contribution to denominator = ‖B_unnorm‖²   (= probability of this Fock outcome)
    F = numerator / denominator   (averaged over all post-selected outcomes).
    """
    M = N + 1
    target = target_ket(alpha, beta, N)
    ket_out = post_BS_ket(alpha, beta, tau, N, ca_cutoff, b_cutoff)

    numerator = 0.0
    denominator = 0.0

    for counts, corr in POSTSEL_MACROS:
        psi_eff = apply_correction(target, corr, N)
        psi_conj = np.conj(psi_eff)
        for ab_idx in alpha_beta_outcomes(*counts, M):
            B_unnorm = ket_out[ab_idx]                # shape (2,)*2M
            amp = np.sum(psi_conj * B_unnorm)
            prob = np.sum(np.abs(B_unnorm) ** 2)
            numerator += abs(amp) ** 2
            denominator += prob

    return float(numerator / denominator) if denominator > 0 else 0.0


# ======================================================================
# Numbers + plots
# ======================================================================
print(f"Mode spacing  Δω = {DELTA_OMEGA}   (T_rep = 2π/Δω = {T_REP:.4f})")
print(f"Carrier       ω₀ = {OMEGA_0}    (T_car = 2π/ω₀ = {T_CAR:.4f}, ω₀/Δω = {OMEGA_0/DELTA_OMEGA:.0f})")
print()

# --- analytic snapshot ------------------------------------------------
demo_N = 4
print(f"== Analytic post-selected fidelity  F(τ) = 1 − 4|α|²|β|² · HOM(τ)  (N = {demo_N}) ==")
states_demo = [
    ("|H⟩",            (1.0, 0.0)),
    ("(|H⟩+|V⟩)/√2",  (1 / np.sqrt(2),  1 / np.sqrt(2))),
    ("(|H⟩+i|V⟩)/√2", (1 / np.sqrt(2), 1j / np.sqrt(2))),
    ("0.6|H⟩+0.8|V⟩", (0.6, 0.8)),
]
print(f"{'state':>20}  {'4|α|²|β|²':>10}  " + "  ".join(f"τ={t:+.3f}" for t in [0.0, T_REP/16, T_REP/8, T_REP/4, T_REP/2]))
for name, (a, b) in states_demo:
    coef = 4 * abs(a) ** 2 * abs(b) ** 2
    Fs = [fidelity_analytic(a, b, t, demo_N) for t in [0.0, T_REP/16, T_REP/8, T_REP/4, T_REP/2]]
    print(f"{name:>20}  {coef:10.3f}  " + "  ".join(f"{F:8.4f}" for F in Fs))
print()

# --- mrmustard cross-check at N = 2 -----------------------------------
print(f"== mrmustard cross-check (N = {mm_N} → {mm_N+1} modes/pol/qubit, "
      f"|ψ⟩ = (|H⟩+|V⟩)/√2,  ca_cutoff = 3, b_cutoff = 2) ==")
print(f"{'τ':>10} {'analytic':>12} {'mrmustard':>12} {'Δ':>12}")
mm_F = np.empty_like(mm_taus)
for i, tau in enumerate(mm_taus):
    F_an = fidelity_analytic(alpha, beta, tau, mm_N)
    F_mm = fidelity_mrmustard(alpha, beta, tau, mm_N)
    mm_F[i] = F_mm
    print(f"{tau:+10.4f} {F_an:12.6f} {F_mm:12.6f} {F_mm - F_an:+12.2e}")
print()

# --- plots -----------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(13, 4.6))

# (a) F vs τ for several N at fixed |ψ⟩ = (|H⟩+|V⟩)/√2 (worst case)
ax = axes[0]
tau_grid = np.linspace(-0.6 * T_REP, 0.6 * T_REP, 4001)
N_curves = [2, 4, 6, 14]
N_to_color = dict(zip(N_curves, plt.cm.viridis(np.linspace(0.15, 0.85, len(N_curves)))))
a_eq, b_eq = 1 / np.sqrt(2), 1 / np.sqrt(2)
for N in N_curves:
    F = np.array([fidelity_analytic(a_eq, b_eq, t, N) for t in tau_grid])
    ax.plot(tau_grid, F, color=N_to_color[N], lw=1.4, label=f"N = {N}")
ax.plot(mm_taus, mm_F, "o", color=N_to_color[mm_N],
        markeredgecolor="black", markeredgewidth=0.8, markersize=7,
        linestyle="none", label=f"mm  N = {mm_N}")
ax.axhline(0.5, color="gray", linestyle="--", linewidth=0.7)
ax.axhline(1.0, color="gray", linestyle=":", linewidth=0.7)
for k in [-1, 0, 1]:
    ax.axvline(k * T_REP, color="gray", linestyle=":", linewidth=0.7)
ax.set_xlabel(r"delay  $\tau$")
ax.set_ylabel(r"fidelity  $F(\tau)$")
ax.set_title(r"(a) F vs $\tau$ for $|\psi\rangle = (|H\rangle + |V\rangle)/\sqrt{2}$")
ax.set_ylim(0.45, 1.03)
ax.legend(fontsize=8, loc="lower right")
ax.grid(alpha=0.3)

# (b) F vs τ for several |ψ⟩ at fixed N
ax = axes[1]
N_b = 4
states_plot = [
    ("|H⟩",                 (1.0, 0.0),                       "tab:blue"),
    ("0.6|H⟩+0.8|V⟩",       (0.6, 0.8),                       "tab:green"),
    ("(|H⟩+|V⟩)/√2",       (1 / np.sqrt(2),  1 / np.sqrt(2)), "tab:red"),
    ("(|H⟩+i|V⟩)/√2",      (1 / np.sqrt(2), 1j / np.sqrt(2)), "tab:orange"),
]
for name, (a, b), c in states_plot:
    F = np.array([fidelity_analytic(a, b, t, N_b) for t in tau_grid])
    coef = 4 * abs(a) ** 2 * abs(b) ** 2
    ax.plot(tau_grid, F, color=c, lw=1.4,
            label=rf"$|\psi\rangle =$ {name}  ($4|\alpha|^2|\beta|^2 = {coef:.2f}$)")
ax.axhline(0.5, color="gray", linestyle="--", linewidth=0.7)
ax.axhline(1.0, color="gray", linestyle=":", linewidth=0.7)
for k in [-1, 0, 1]:
    ax.axvline(k * T_REP, color="gray", linestyle=":", linewidth=0.7)
ax.set_xlabel(r"delay  $\tau$")
ax.set_ylabel(r"$F(\tau)$")
ax.set_title(rf"(b) F vs $\tau$ for several $|\psi\rangle$  (N = {N_b})")
ax.set_ylim(0.45, 1.03)
ax.legend(fontsize=8, loc="lower right")
ax.grid(alpha=0.3)

plt.suptitle(r"Post-selected teleportation fidelity vs input-qubit timing jitter")
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("teleportation_time_jitter_fidelity.png", dpi=150)
plt.show()
print("Plot saved to teleportation_time_jitter_fidelity.png")
