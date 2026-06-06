"""Simple timestep and walker sensitivity checks."""

from __future__ import annotations

import json

from helium3_dmc.dmc import DMCConfig, run_dmc


if __name__ == "__main__":
    base_a = 5.3
    dt_tests = [0.002, 0.003, 0.004]
    walker_tests = [32, 64, 96]

    dt_results = [
        run_dmc(DMCConfig(lattice_constant=base_a, dtau=dt, n_walkers=64, equil_steps=120, prod_steps=200, seed=20 + i))
        for i, dt in enumerate(dt_tests)
    ]

    walker_results = [
        run_dmc(
            DMCConfig(
                lattice_constant=base_a,
                dtau=0.003,
                n_walkers=nw,
                equil_steps=120,
                prod_steps=200,
                seed=40 + i,
            )
        )
        for i, nw in enumerate(walker_tests)
    ]

    print(
        json.dumps(
            {
                "timestep_bias": [r.__dict__ for r in dt_results],
                "walker_bias": [r.__dict__ for r in walker_results],
            },
            indent=2,
        )
    )
