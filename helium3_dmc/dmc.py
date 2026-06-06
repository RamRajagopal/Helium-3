"""Diffusion Monte Carlo engine for solid helium-3."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .aziz import aziz_potential
from .lattice import box_lengths, build_fcc_positions, minimum_image
from .stats import Estimate, blocking_estimate
from .wavefunction import fcc_k_vectors, trial_logpsi


@dataclass
class DMCConfig:
    lattice_constant: float
    cells: tuple[int, int, int] = (2, 2, 2)
    n_walkers: int = 64
    equil_steps: int = 200
    prod_steps: int = 400
    dtau: float = 0.003
    seed: int = 7
    initial_noise: float = 0.03


@dataclass
class DMCResult:
    lattice_constant: float
    n_particles: int
    energy_per_particle: float
    stderr: float
    acceptance: float
    n_samples: int


def local_potential_energy(positions: np.ndarray, box: np.ndarray) -> float:
    n = positions.shape[0]
    e = 0.0
    for i in range(n - 1):
        for j in range(i + 1, n):
            dr = minimum_image(positions[i] - positions[j], box)
            r = float(np.linalg.norm(dr))
            e += aziz_potential(r)
    return e


def run_dmc(config: DMCConfig) -> DMCResult:
    rng = np.random.default_rng(config.seed)
    ref = build_fcc_positions(config.cells, config.lattice_constant)
    n = ref.shape[0]
    box = box_lengths(config.cells, config.lattice_constant)
    if n % 2 != 0:
        raise ValueError("Number of particles must be even for spin-balanced Slater-Jastrow wavefunction")

    n_up = n // 2
    k_up = fcc_k_vectors(box, n_up)
    k_down = fcc_k_vectors(box, n - n_up)

    walkers = np.repeat(ref[None, :, :], config.n_walkers, axis=0)
    walkers += rng.normal(scale=config.initial_noise, size=walkers.shape)
    walkers %= box

    eref = local_potential_energy(ref, box) / n
    energies: list[float] = []
    accepted = 0
    proposed = 0

    for step in range(config.equil_steps + config.prod_steps):
        new_walkers = []
        local_es = []

        for w in walkers:
            proposal = w + rng.normal(scale=np.sqrt(config.dtau), size=w.shape)
            proposal %= box

            old_log, old_sign = trial_logpsi(w, box, k_up, k_down)
            new_log, new_sign = trial_logpsi(proposal, box, k_up, k_down)

            if old_sign == 0.0 or new_sign == 0.0 or old_sign != new_sign:
                ratio = 0.0
            else:
                ratio = float(np.exp(2.0 * (new_log - old_log)))

            proposed += 1
            if rng.random() < min(1.0, ratio):
                current = proposal
                accepted += 1
            else:
                current = w

            e_loc = local_potential_energy(current, box) / n
            weight = np.exp(-(e_loc - eref) * config.dtau)
            copies = max(1, int(weight + rng.random()))
            for _ in range(copies):
                new_walkers.append(current.copy())
                local_es.append(e_loc)

        if not new_walkers:
            new_walkers = [ref.copy()]
            local_es = [local_potential_energy(ref, box) / n]

        if len(new_walkers) > config.n_walkers:
            idx = rng.choice(len(new_walkers), size=config.n_walkers, replace=False)
            walkers = np.asarray([new_walkers[i] for i in idx])
            local_arr = np.asarray([local_es[i] for i in idx], dtype=float)
        else:
            while len(new_walkers) < config.n_walkers:
                j = rng.integers(0, len(new_walkers))
                new_walkers.append(new_walkers[j].copy())
                local_es.append(local_es[j])
            walkers = np.asarray(new_walkers)
            local_arr = np.asarray(local_es, dtype=float)

        # Population-control feedback: penalize growth above target walkers, boost when below target.
        eref = float(np.mean(local_arr)) - (len(walkers) - config.n_walkers) / max(config.n_walkers, 1) / config.dtau

        if step >= config.equil_steps:
            energies.append(float(np.mean(local_arr)))

    est: Estimate = blocking_estimate(energies, block_size=20)
    return DMCResult(
        lattice_constant=config.lattice_constant,
        n_particles=n,
        energy_per_particle=est.mean,
        stderr=est.stderr,
        acceptance=accepted / max(1, proposed),
        n_samples=est.nsamples,
    )
