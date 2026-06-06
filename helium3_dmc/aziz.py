"""Aziz pair potential for helium-helium interactions."""

from __future__ import annotations

import math

EPSILON_K = 10.8  # Kelvin
RM_ANGSTROM = 2.9673
A = 0.5448504e6
ALPHA = 13.353384
# Exponential prefactor used in the short-range repulsive term.
BETA = 0.4253785
C6 = 1.3732412
# Dispersion coefficient; same numeric value as BETA in the HFD-B(HE) fit.
C8 = 0.4253785
C10 = 0.178100
D = 1.241314


def _f_damp(x: float) -> float:
    if x >= D:
        return 1.0
    return math.exp(-((D / x) - 1.0) ** 2)


def aziz_potential(r_angstrom: float) -> float:
    """Return Aziz HFD-B(HE) potential in Kelvin."""
    if r_angstrom <= 0:
        raise ValueError("r_angstrom must be positive")

    x = r_angstrom / RM_ANGSTROM
    repulsive = A * math.exp(-ALPHA * x + BETA * x * x)
    attractive = _f_damp(x) * (C6 / x**6 + C8 / x**8 + C10 / x**10)
    return EPSILON_K * (repulsive - attractive)
