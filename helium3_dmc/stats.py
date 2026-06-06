"""Simple blocking statistics utilities."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


@dataclass
class Estimate:
    mean: float
    stderr: float
    nsamples: int


def blocking_estimate(values: list[float], block_size: int = 20) -> Estimate:
    if not values:
        return Estimate(mean=float("nan"), stderr=float("nan"), nsamples=0)

    arr = np.asarray(values, dtype=float)
    if len(arr) < block_size:
        mean = float(np.mean(arr))
        stderr = float(np.std(arr, ddof=1) / math.sqrt(len(arr))) if len(arr) > 1 else 0.0
        return Estimate(mean=mean, stderr=stderr, nsamples=len(arr))

    n_blocks = len(arr) // block_size
    trimmed = arr[: n_blocks * block_size]
    blocks = trimmed.reshape(n_blocks, block_size)
    block_means = np.mean(blocks, axis=1)
    mean = float(np.mean(block_means))
    stderr = float(np.std(block_means, ddof=1) / math.sqrt(n_blocks)) if n_blocks > 1 else 0.0
    return Estimate(mean=mean, stderr=stderr, nsamples=len(arr))
