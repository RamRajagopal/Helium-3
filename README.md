# Helium-3

Diffusion Monte Carlo (DMC) toolkit to estimate the ground-state energy of an FCC helium lattice using:
- Aziz pair potential
- Jastrow correlation
- Slater-Jastrow trial wavefunction with fixed-node exchange treatment (spin-balanced He-3)

## Project structure

- `helium3_dmc/aziz.py` — Aziz potential
- `helium3_dmc/lattice.py` — FCC lattice and periodic minimum-image helpers
- `helium3_dmc/wavefunction.py` — Jastrow and Slater determinant helpers
- `helium3_dmc/dmc.py` — DMC propagator, branching, and statistics
- `helium3_dmc/sweep.py` — lattice constant sweep and output writing
- `scripts/run_sweep.py` — command-line sweep runner
- `scripts/plot_energy.py` — E(a) plot generation from sweep CSV
- `scripts/verification_checks.py` — timestep/walker sensitivity checks

## Install

```bash
cd <repo-root>
python -m pip install -e .
```

## Run lattice sweep (4.4 Å to 6.0 Å)

```bash
cd <repo-root>
python scripts/run_sweep.py --a-min 4.4 --a-max 6.0 --a-step 0.05 --output-dir outputs
```

Outputs:
- `outputs/energy_vs_lattice.csv`
- `outputs/energy_vs_lattice.json`

## Plot E(a)

```bash
cd <repo-root>
python scripts/plot_energy.py --input-csv outputs/energy_vs_lattice.csv --output-png outputs/energy_vs_lattice.png
```

Output:
- `outputs/energy_vs_lattice.png`

## Verification checks

```bash
cd <repo-root>
python scripts/verification_checks.py
```

This reports timestep-bias and walker-population sensitivity data in JSON.

## Tests

```bash
cd <repo-root>
python -m unittest discover -s tests
```
