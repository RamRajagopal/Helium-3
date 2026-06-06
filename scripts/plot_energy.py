"""Plot E(a) from lattice sweep CSV output."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Plot E(a) from energy_vs_lattice.csv")
    p.add_argument("--input-csv", type=str, default="outputs/energy_vs_lattice.csv")
    p.add_argument("--output-png", type=str, default="outputs/energy_vs_lattice.png")
    return p.parse_args()


def load_data(path: Path) -> tuple[list[float], list[float], list[float]]:
    a_vals: list[float] = []
    energies: list[float] = []
    errors: list[float] = []

    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            a_vals.append(float(row["lattice_constant_A"]))
            energies.append(float(row["energy_per_particle_K"]))
            errors.append(float(row["stderr_K"]))

    if not a_vals:
        raise ValueError(f"No data rows found in {path}")
    return a_vals, energies, errors


def main() -> None:
    args = parse_args()
    input_csv = Path(args.input_csv)
    output_png = Path(args.output_png)

    if not input_csv.exists():
        raise FileNotFoundError(f"Input CSV not found: {input_csv}")

    output_png.parent.mkdir(parents=True, exist_ok=True)
    a_vals, energies, errors = load_data(input_csv)

    plt.figure(figsize=(7, 4.5))
    plt.errorbar(a_vals, energies, yerr=errors, fmt="o-", capsize=3)
    plt.xlabel("Lattice constant a (Å)")
    plt.ylabel("Energy per particle E(a) (K)")
    plt.title("Helium-3 FCC DMC: E(a)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_png, dpi=180)
    print(f"Plot saved to: {output_png}")


if __name__ == "__main__":
    main()
