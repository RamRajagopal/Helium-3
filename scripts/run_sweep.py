"""CLI entry point for helium-3 lattice sweep."""

from __future__ import annotations

import argparse
import json

from helium3_dmc.sweep import SweepConfig, run_lattice_sweep


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run helium-3 DMC lattice constant sweep")
    p.add_argument("--a-min", type=float, default=5.0)
    p.add_argument("--a-max", type=float, default=5.8)
    p.add_argument("--a-step", type=float, default=0.05)
    p.add_argument("--cells", type=int, nargs=3, default=(2, 2, 2))
    p.add_argument("--n-walkers", type=int, default=64)
    p.add_argument("--equil-steps", type=int, default=200)
    p.add_argument("--prod-steps", type=int, default=400)
    p.add_argument("--dtau", type=float, default=0.003)
    p.add_argument("--seed", type=int, default=11)
    p.add_argument("--output-dir", type=str, default="outputs")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    cfg = SweepConfig(
        a_min=args.a_min,
        a_max=args.a_max,
        a_step=args.a_step,
        output_dir=args.output_dir,
        cells=tuple(args.cells),
        n_walkers=args.n_walkers,
        equil_steps=args.equil_steps,
        prod_steps=args.prod_steps,
        dtau=args.dtau,
        seed=args.seed,
    )
    results = run_lattice_sweep(cfg)
    min_r = min(results, key=lambda r: r.energy_per_particle)
    print(
        json.dumps(
            {
                "min_lattice_constant_A": min_r.lattice_constant,
                "min_energy_per_particle_K": min_r.energy_per_particle,
                "stderr_K": min_r.stderr,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
