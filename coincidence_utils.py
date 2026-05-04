"""Mode-locked-comb building blocks shared by the BS coincidence scripts.

Both `coincidence_coherent.py` and `coincidence_number_states.py` model a
pulsed beam as a comb of N+1 frequency modes
    ω_k = ω₀ + k · Δω,    k = −N/2 .. +N/2   (N even),
all with the same per-mode amplitude.  The comb gives a pulse train in
time with repetition  T_rep = 2π/Δω  and pulse width ~ T_rep/N; the
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


def mode_frequencies(N):
    """N+1-mode comb symmetric about ω₀:  ω_k = ω₀ + k Δω, k = −N/2..+N/2."""
    if N % 2 != 0:
        raise ValueError("N must be even (modes range k = −N/2..+N/2)")
    k = np.arange(-N // 2, N // 2 + 1)
    return OMEGA_0 + k * DELTA_OMEGA


def dirichlet_kernel(x, N):
    """D_N(x) = Σ_{k=−N/2}^{+N/2} e^{i k x} = sin((N+1) x/2) / sin(x/2).

    Real-valued.  Regular at x = 2π m  (limit N+1, since N is even).
    """
    x = np.asarray(x, dtype=float)
    den = np.sin(x / 2)
    safe_den = np.where(np.abs(den) < 1e-12, 1.0, den)
    val = np.sin((N + 1) * x / 2) / safe_den
    return np.where(np.abs(den) < 1e-12, float(N + 1), val)


def pulse_envelope(t, N):
    """Peak-normalized single-beam pulse intensity:  |D_N(Δω t) / (N+1)|².

    The carrier drops out of |⟨E(t)⟩|² so this is the same envelope for
    coherent-state intensity (up to an overall α²(N+1)² scale) and for the
    single-photon wavepacket |ψ(t)|² (up to a 1/(N+1) normalization).
    """
    return (dirichlet_kernel(DELTA_OMEGA * t, N) / (N + 1)) ** 2
