"""FCC lattice generation and periodic geometry helpers."""

from __future__ import annotations

import numpy as np

FCC_BASIS = np.array(
    [
        [0.0, 0.0, 0.0],
        [0.0, 0.5, 0.5],
        [0.5, 0.0, 0.5],
        [0.5, 0.5, 0.0],
    ],
    dtype=float,
)


def build_fcc_positions(cells: tuple[int, int, int], lattice_constant: float) -> np.ndarray:
    nx, ny, nz = cells
    points = []
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                shift = np.array([i, j, k], dtype=float)
                for b in FCC_BASIS:
                    points.append((shift + b) * lattice_constant)
    return np.asarray(points, dtype=float)


def box_lengths(cells: tuple[int, int, int], lattice_constant: float) -> np.ndarray:
    return np.asarray(cells, dtype=float) * lattice_constant


def minimum_image(displacement: np.ndarray, box: np.ndarray) -> np.ndarray:
    return displacement - box * np.round(displacement / box)


def pair_distances(positions: np.ndarray, box: np.ndarray) -> list[float]:
    n = positions.shape[0]
    dists: list[float] = []
    for i in range(n - 1):
        for j in range(i + 1, n):
            dr = minimum_image(positions[i] - positions[j], box)
            dists.append(float(np.linalg.norm(dr)))
    return dists
