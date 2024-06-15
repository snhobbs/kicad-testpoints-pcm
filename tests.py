import unittest
import sys
import pathlib

sys.path.append(pathlib.Path(__file__).parent.as_posix())
sys.path.append((pathlib.Path(__file__).parent / "kicadtestpoints/").as_posix())

#from kicadtestpoints import plugin
import plugin


class TestPadPosition(unittest.TestCase):
    def test_calc_pad_position(self):
        origin = (1,2)
        center = (100,10)  # Position is to the bottom right of the origin
        mult_settings = [
            (1,1), # gerber coordinates
            (1,-1),
            (-1,1),
            (-1,-1)
        ]
        expected_values = (
            (99,8), # bottom right
            (99,-8),
            (-99,8),
            (-99,-8)
        )
        for mult, expected in zip(mult_settings, expected_values):
            out = plugin.calc_pad_position(center, origin, mult[0], mult[1])
            assert out == expected
