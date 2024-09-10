import unittest
import sys
import pathlib

sys.path.append(pathlib.Path(__file__).parent.as_posix())
sys.path.append((pathlib.Path(__file__).parent / "src/").as_posix())

from kicadtestpoints import kicad_testpoints
# import plugin


class TestPadPosition(unittest.TestCase):
    def test_calc_pad_position(self):
        origin = (10, 10)  # in pixel coordinates
        centers = [  # in pixel coordinates
            (0, 0),
            (10, 10),
        ]
        expected_values = (  # cartesian
            (-10, 10),
            (0, 0),
        )
        for center, expected in zip(centers, expected_values):
            out = kicad_testpoints.calc_pad_position(center, origin)
            assert out == expected
