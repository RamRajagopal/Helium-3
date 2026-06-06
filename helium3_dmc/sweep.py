"""Lattice constant sweep workflow."""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .dmc import DMCConfig, DMCResult, run_dmc


@dataclass
class SweepConfig:
    a_min: float = 5.0
    a_max: float = 5.8
    a_step: float = 0.05
    output_dir: str = "outputs"
    cells: tuple[int, int, int] = (2, 2, 2)
    n_walkers: int = 64
    equil_steps: int = 200
    prod_steps: int = 400
    dtau: float = 0.003
    seed: int = 11


def _frange(start: float, stop: float, step: float) -> list[float]:
    vals = []
    x = start
    while x <= stop + 1e-12:
        vals.append(round(x, 8))
        x += step
    return vals


def run_lattice_sweep(config: SweepConfig) -> list[DMCResult]:
    out = Path(config.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    results: list[DMCResult] = []
    for i, a in enumerate(_frange(config.a_min, config.a_max, config.a_step)):
        run_cfg = DMCConfig(
            lattice_constant=a,
            cells=config.cells,
            n_walkers=config.n_walkers,
            equil_steps=config.equil_steps,
            prod_steps=config.prod_steps,
            dtau=config.dtau,
            seed=config.seed + i,
        )
        results.append(run_dmc(run_cfg))

    csv_path = out / "energy_vs_lattice.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["lattice_constant_A", "energy_per_particle_K", "stderr_K", "acceptance", "samples"])
        for r in results:
            writer.writerow([r.lattice_constant, r.energy_per_particle, r.stderr, r.acceptance, r.n_samples])

    json_path = out / "energy_vs_lattice.json"
    with json_path.open("w", encoding="utf-8") as f:
        json.dump([asdict(r) for r in results], f, indent=2)

    return results
