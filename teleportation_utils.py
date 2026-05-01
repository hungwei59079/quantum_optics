import numpy as np
import mrmustard.lab as lab

from display_utils import state_to_braket


def apply_X(ket):
    """X on Bob's polarization qubit: swap |H> and |V>."""
    return np.swapaxes(ket, 0, 1)


def apply_Z(ket):
    """Z on Bob's polarization qubit: phase flip on |V>."""
    new_ket = ket.copy()
    new_ket[:, 1] *= -1
    return new_ket


_PAULI = {"X": apply_X, "Z": apply_Z}

# Photon-counting outcome -> ordered Pauli corrections Bob applies to recover
# |psi>, keyed by the resource Bell state used.  Each tuple lists ops left-to-
# right (first element applied first).  Bunched outcomes are absent because
# Phi+ and Phi- are indistinguishable in a BS-only scheme; no single Pauli
# correction reliably recovers |psi> from them.
corrections = {
    "Phi_minus": {
        (1, 0, 0, 1): ("X",),
        (0, 1, 1, 0): ("X",),
        (1, 1, 0, 0): ("X", "Z"),  # X first, then Z
        (0, 0, 1, 1): ("Z", "X"),  # Z first, then X
    },
    # "Phi_plus":  { ... },  # to be implemented
    # "Psi_minus": { ... },  # to be implemented
    # "Psi_plus":  { ... },  # to be implemented
}


def bell_measurement(out_ket, resource_type, psi_C, threshold=1e-6, verbose=True):
    """Run Bell measurement, print results, and return per-outcome fidelities.

    Args:
        out_ket:       Shape-(3,3,3,3,2,2) numpy array — the 6-mode output ket
                       after applying the Bell-measurement circuit.
        resource_type: Key into `corrections` naming the resource Bell state
                       (e.g. "Phi_minus").
        psi_C:         Shape-(2,2) ket of the intended state to teleport, used
                       to compute the post-correction fidelity F = |<psi|out>|^2.
        threshold:     Outcomes with probability below this are skipped.
        verbose:       If False, suppress all printed output.

    Returns:
        dict mapping correctable outcome tuples (n0,n1,n2,n3) -> fidelity float.
    """
    outcome_corrections = corrections[resource_type]

    if verbose:
        print("=" * 60)
        print(f"Outcomes |n_C_H, n_C_V, n_A_H, n_A_V>  (resource: {resource_type})")
        print("Bob: raw state -> after Pauli correction")
        print("=" * 60)

    total_p = 0.0
    fidelities = {}
    for n0, n1, n2, n3 in np.ndindex(3, 3, 3, 3):
        if n0 + n1 + n2 + n3 != 2:
            continue  # photon-number conservation: 2 photons land on the C/A side
        sub = out_ket[n0, n1, n2, n3, :, :]
        prob = float(np.sum(np.abs(sub) ** 2))
        if prob < threshold:
            continue

        total_p += prob
        cond_ket = sub / np.sqrt(prob)

        if verbose:
            raw_braket = state_to_braket(lab.State(ket=cond_ket), [2, 2], [[0, 1]])
            outcome = f"|{n0},{n1},{n2},{n3}>"
            print(f"  {outcome:<13} P={prob*100:6.2f}%   raw : {raw_braket}")

        key = (n0, n1, n2, n3)
        if key in outcome_corrections:
            ops = outcome_corrections[key]
            corr_ket = cond_ket
            for op in ops:
                corr_ket = _PAULI[op](corr_ket)
            fidelity = float(abs(np.sum(np.conj(psi_C) * corr_ket)) ** 2)
            fidelities[key] = fidelity
            if verbose:
                corr_braket = state_to_braket(lab.State(ket=corr_ket), [2, 2], [[0, 1]])
                ops_str = " then ".join(ops)
                print(f"  {'':<13}                apply {ops_str}: {corr_braket}   F={fidelity:.4f}")
        elif verbose:
            print(f"  {'':<13}                [Phi+/Phi- ambiguous -- no Pauli correction recovers |psi>]")

    if verbose:
        print()
        print(f"Total probability over listed outcomes: {total_p*100:.2f}%")

    return fidelities
