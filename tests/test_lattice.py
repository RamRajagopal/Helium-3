import unittest

import numpy as np

from helium3_dmc.lattice import build_fcc_positions, minimum_image


class TestLatticeUtilities(unittest.TestCase):
    def test_fcc_cell_particle_count(self):
        pos = build_fcc_positions((2, 2, 2), 5.2)
        self.assertEqual(pos.shape, (32, 3))

    def test_minimum_image_wrap(self):
        box = np.array([10.0, 10.0, 10.0])
        dr = np.array([6.0, -6.0, 1.0])
        wrapped = minimum_image(dr, box)
        np.testing.assert_allclose(wrapped, np.array([-4.0, 4.0, 1.0]))


if __name__ == "__main__":
    unittest.main()
