Good questions — both are about subtle details.

Q1. Why apply correction to target instead of to the post-measurement ket?
It's the identity you suspect, made precise. Fidelity is

$$
F = \langle\psi_\text{target}|,U,\rho_\text{post},U^\dagger,|\psi_\text{target}\rangle
$$

For a pure |B⟩ contribution this is |⟨ψ_target | U | B⟩|². Using
⟨ψ_target|U|B⟩ = ⟨U†ψ_target|B⟩, we can move U across the bra:


|⟨ψ_target | U | B⟩|²  =  |⟨U†ψ_target | B⟩|²
So either "apply U to B and inner-product with ψ_target" or "apply U† to ψ_target and inner-product with B" gives the same number.

Why we picked the second: efficiency. The correction is the same for every Fock outcome inside a given macro (there are M² of them). If we applied U to each B-slice we'd do M² ops per macro; applying U† to the target once at the macro level and reusing the result across M² inner products does 1 op per macro. For M=3 that's a 9× saving; for M=5 it's 25×.

About U vs U†, especially for two-Pauli compositions: for a single Pauli op (X or Z), $X^\dagger = X$ and $Z^\dagger = Z$, so $U = U^\dagger$ and the order doesn't matter. For a composition like ("X", "Z") (apply X first, then Z), the composite operator is $U = ZX$ and $U^\dagger = (ZX)^\dagger = X^\dagger Z^\dagger = XZ$.

Now, $XZ$ and $ZX$ are not the same operator — they differ by a global sign because Pauli X and Z anti-commute:

$$
XZ = -ZX.
$$

But that sign is a global phase on the ket. Since fidelity uses $|\cdot|^2$, the sign cancels:


|⟨XZ·ψ_target | B⟩|²  =  |⟨−ZX·ψ_target | B⟩|²  =  |⟨ZX·ψ_target | B⟩|²
So applying the tuple operators in their listed order (apply_correction does out = X(out); out = Z(out), which builds $ZX|\psi\rangle$ — note that the order of function application on the ket is the reverse of the operator-matrix order, since each new op multiplies on the left) gives the same |amp|² as applying $U^\dagger = XZ$ would. The code is using this slack on purpose — the docstring on apply_correction notes it.

If the corrections ever included a non-Pauli unitary (or if we wanted amplitudes instead of squared magnitudes), we'd have to be careful to use $U^\dagger$ exactly. For our four-outcome Pauli table, it doesn't matter.

Q2. Why no : placeholders for the trailing axes?
Standard numpy behavior. When you index an ndarray with a tuple of length k that is less than the number of dimensions d, numpy treats the remaining d − k trailing axes as if you'd written : for each of them.

For ket_out of shape (3,)*(4M) + (2,)*(2M) (total 6M dims) and ab_idx of length 4M:


ket_out[ab_idx]
# equivalent to
ket_out[ab_idx[0], ab_idx[1], ..., ab_idx[4M-1]]
# equivalent to
ket_out[ab_idx[0], ab_idx[1], ..., ab_idx[4M-1], :, :, :, :, :, :]
                                                  └─── 2M trailing colons ───┘
So the result has shape (2,)*(2M) — exactly Bob's reduced Fock-space ket conditioned on the αβ outcome ab_idx.

Two small clarifications:

Tuple vs unpacking. ket_out[ab_idx] works only because ab_idx is a tuple. If it were a list, numpy would interpret it as "fancy indexing" along axis 0 (broadcasting it as an index array), which gives a totally different result. That's why alpha_beta_outcomes yields tuples (yield aH + aV + bH + bV where each piece is a tuple, so + concatenates).
The ... shorthand. You could also write ket_out[ab_idx + (slice(None),) * (2*M)] or ket_out[(*ab_idx, ...)] — the latter uses Ellipsis to make "fill the rest with colons" explicit. The bare ket_out[ab_idx] form is the most concise; whether that's clearer or sneakier is a style call. If you ever find yourself confused reading it, the ... form might be worth adding for explicitness.