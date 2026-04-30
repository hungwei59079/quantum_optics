import numpy as np
from mrmustard.lab import circuit_drawer


def explain_circuit(circuit, mode_labels):
    """Print the circuit diagram with a mode legend and per-gate annotation."""
    print("=" * 60)
    print("Mode legend:")
    for i, label in enumerate(mode_labels):
        print(f"  {i}: {label}")
    print()
    print("Operations (in order):")
    for op in circuit.ops:
        annotated = ", ".join(f"{m}={mode_labels[m]}" for m in op.modes)
        print(f"  {op.short_name} on [{annotated}]")
    print()
    print("Diagram:")
    print(circuit_drawer.circuit_text(circuit.ops))
    print()


def _format_coefficient(amp, decimals, threshold, is_first):
    """Format a complex amplitude into a sign + magnitude string."""
    real = round(float(np.real(amp)), decimals)
    imag = round(float(np.imag(amp)), decimals)

    if abs(imag) < threshold:
        sign = "" if real >= 0 else "-"
        body = f"{abs(real):.{decimals}f}"
    elif abs(real) < threshold:
        sign = "" if imag >= 0 else "-"
        body = f"{abs(imag):.{decimals}f}i"
    else:
        sign = ""
        sep = "+" if imag >= 0 else "-"
        body = f"({real:.{decimals}f}{sep}{abs(imag):.{decimals}f}i)"

    if is_first:
        return f"{sign}{body}"
    connector = "-" if sign == "-" else "+"
    return f"{connector} {body}"


def state_to_braket(state, cutoffs, mode_groups, polarization_labels=("H", "V"),
                    threshold=1e-4, decimals=4):
    """Format a pure state in polarization-grouped braket notation.

    Modes are grouped by spatial location; within each group, photons are
    written by polarization label. So 1 H-photon in arm A and 1 V-photon in
    arm B is rendered as ``|H>|V>``; 1 H + 1 V in arm A and nothing in arm B
    becomes ``|HV>|0>``; 2 H-photons in arm A becomes ``|HH>|0>``.

    Args:
        state: a pure ``State`` object (must have a ket).
        cutoffs: cutoff dimensions for each mode (list of ints).
        mode_groups: nested list of mode indices per spatial group. The order
            of indices within each inner list must match ``polarization_labels``.
            E.g. ``[[0, 1], [2, 3]]`` for two arms with H,V on each.
        polarization_labels: labels per mode within a group (default ``("H", "V")``).
        threshold: amplitudes with magnitude below this are dropped.
        decimals: digits to round coefficients to.
    """
    ket = np.asarray(state.ket(cutoffs=cutoffs))

    terms = []
    for idx in np.ndindex(*ket.shape):
        amp = ket[idx]
        if abs(amp) < threshold:
            continue

        labels = []
        for group in mode_groups:
            counts = [idx[m] for m in group]
            if sum(counts) == 0:
                labels.append("0")
            else:
                labels.append("".join(p * n for p, n in zip(polarization_labels, counts)))
        ket_str = "".join(f"|{l}>" for l in labels)
        terms.append((amp, ket_str))

    if not terms:
        return "0"

    parts = [
        f"{_format_coefficient(amp, decimals, threshold, is_first=(i == 0))} {ks}"
        for i, (amp, ks) in enumerate(terms)
    ]
    return " ".join(parts)
