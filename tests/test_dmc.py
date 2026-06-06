import unittest

from helium3_dmc.dmc import DMCConfig, run_dmc


class TestDMCSmoke(unittest.TestCase):
    def test_reproducible_short_run(self):
        cfg = DMCConfig(lattice_constant=5.2, n_walkers=16, equil_steps=10, prod_steps=20, dtau=0.002, seed=123)
        r1 = run_dmc(cfg)
        r2 = run_dmc(cfg)
        self.assertAlmostEqual(r1.energy_per_particle, r2.energy_per_particle, places=12)


if __name__ == "__main__":
    unittest.main()
