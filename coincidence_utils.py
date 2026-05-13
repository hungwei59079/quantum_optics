"""Mode-locked-comb building blocks shared by the BS coincidence scripts.

Both `coincidence_coherent.py` and `coincidence_number_states.py` model a
pulsed beam as a comb of M frequency modes
    ω_k = ω₀ + k · Δω,    k = −(M−1)/2 .. +(M−1)/2   (M odd),
all with the same per-mode amplitude.  The comb gives a pulse train in
time with repetition  T_rep = 2π/Δω  and pulse width ~ T_rep/(M−1); the
carrier ω₀ sets the optical period  T_car = 2π/ω₀.  Real pulsed lasers
have ω₀/Δω > 10³ — we keep the ratio moderate so the carrier fringes in
the coherent script stay visible against the envelope.
"""

import numpy as np


# --- Mode-locked comb parameters ------------------------------------
DELTA_OMEGA = 1.0
OMEGA_0 = 30.0 * DELTA_OMEGA
T_REP = 2.0 * np.pi / DELTA_OMEGA
T_CAR = 2.0 * np.pi / OMEGA_0


def mode_frequencies(M):
    """M-mode comb symmetric about ω₀:  ω_k = ω₀ + k Δω, k = −(M−1)/2..+(M−1)/2."""
    if M % 2 != 1:
        raise ValueError("M must be odd (modes range k = −(M−1)/2..+(M−1)/2)")
    half = (M - 1) // 2
    k = np.arange(-half, half + 1)
    return OMEGA_0 + k * DELTA_OMEGA


def dirichlet_kernel(x, M):
    """D_M(x) = Σ_{k=−(M−1)/2}^{+(M−1)/2} e^{i k x} = sin(M x/2) / sin(x/2).

    Real-valued.  Regular at x = 2π m  (limit M, since M−1 is even when M odd).
    """
    x = np.asarray(x, dtype=float)
    den = np.sin(x / 2)
    safe_den = np.where(np.abs(den) < 1e-12, 1.0, den)
    val = np.sin(M * x / 2) / safe_den
    return np.where(np.abs(den) < 1e-12, float(M), val)


def pulse_envelope(t, M):
    """Peak-normalized single-beam pulse intensity:  |D_M(Δω t) / M|².

    The carrier drops out of |⟨E(t)⟩|² so this is the same envelope for
    coherent-state intensity (up to an overall α² M² scale) and for the
    single-photon wavepacket |ψ(t)|² (up to a 1/M normalization).
    """
    return (dirichlet_kernel(DELTA_OMEGA * t, M) / M) ** 2
