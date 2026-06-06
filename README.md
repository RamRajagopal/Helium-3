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
- `scripts/verification_checks.py` — timestep/walker sensitivity checks

## Install

```bash
cd <repo-root>
python -m pip install -e .
```

## Run lattice sweep (5.0 Å to 5.8 Å)

```bash
cd <repo-root>
python scripts/run_sweep.py --a-min 5.0 --a-max 5.8 --a-step 0.05 --output-dir outputs
```

Outputs:
- `outputs/energy_vs_lattice.csv`
- `outputs/energy_vs_lattice.json`

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
