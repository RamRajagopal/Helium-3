"""Trial-wavefunction utilities with Jastrow and exchange terms."""

from __future__ import annotations

import numpy as np

from .lattice import minimum_image

# Finite floor for near-singular determinants to avoid inf/nan in acceptance ratios.
LOG_AMP_FLOOR = -1e6


def jastrow_log(positions: np.ndarray, box: np.ndarray, a: float = 2.2, b: float = 1.2) -> float:
    n = positions.shape[0]
    total = 0.0
    for i in range(n - 1):
        for j in range(i + 1, n):
            dr = minimum_image(positions[i] - positions[j], box)
            r = np.linalg.norm(dr)
            if r > 1e-12:
                total += -0.5 * (a / r) ** b
    return float(total)


def fcc_k_vectors(box: np.ndarray, count: int) -> np.ndarray:
    rec = 2.0 * np.pi / box
    ks = []
    shell = 0
    while len(ks) < count:
        shell += 1
        for nx in range(-shell, shell + 1):
            for ny in range(-shell, shell + 1):
                for nz in range(-shell, shell + 1):
                    if nx == ny == nz == 0:
                        continue
                    ks.append(rec * np.array([nx, ny, nz], dtype=float))
                    if len(ks) >= count:
                        break
                if len(ks) >= count:
                    break
            if len(ks) >= count:
                break
    return np.asarray(ks, dtype=float)


def slater_logabs_sign(positions: np.ndarray, ks: np.ndarray) -> tuple[float, float]:
    mat = np.exp(1j * positions @ ks.T)
    det = np.linalg.det(mat)
    amp = np.abs(det)
    if amp < 1e-300:
        return LOG_AMP_FLOOR, 0.0
    return float(np.log(amp)), float(np.sign(det.real))


def trial_logpsi(
    positions: np.ndarray,
    box: np.ndarray,
    k_up: np.ndarray,
    k_down: np.ndarray,
) -> tuple[float, float]:
    n = positions.shape[0]
    n_up = n // 2
    up = positions[:n_up]
    down = positions[n_up:]

    jlog = jastrow_log(positions, box)
    up_log, up_sign = slater_logabs_sign(up, k_up)
    dn_log, dn_sign = slater_logabs_sign(down, k_down)
    return jlog + up_log + dn_log, up_sign * dn_sign
