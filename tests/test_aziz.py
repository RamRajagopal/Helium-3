import unittest

from helium3_dmc.aziz import aziz_potential


class TestAzizPotential(unittest.TestCase):
    def test_repulsive_at_short_range(self):
        self.assertGreater(aziz_potential(2.5), 0.0)

    def test_attractive_at_longer_range(self):
        self.assertLess(aziz_potential(3.6), 0.0)


if __name__ == "__main__":
    unittest.main()
