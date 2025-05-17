import unittest
from unittest.mock import MagicMock
import pandas as pd
from kicad_testpoints import kicad_testpoints

class PAD:
    pass

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
            self.assertEqual(out, expected)

    def test_calc_probe_distance(self):
        a = {"x": 0, "y": 0}
        b = {"x": 3, "y": 4}
        dist = kicad_testpoints.calc_probe_distance(a, b)
        self.assertAlmostEqual(dist, 5.0)

    def test_calc_probe_distances(self):
        probes_df = MagicMock()
        # Mock dataframe to return rows
        probes_df.__getitem__.side_effect = lambda key: pd.DataFrame([
            {"test point ref des": "TP1", "x": 0, "y": 0},
            {"test point ref des": "TP2", "x": 3, "y": 4},
        ])
        probes_df.iterrows.return_value = [
            (0, pd.Series({"test point ref des": "TP1", "x": 0, "y": 0})),
            (1, pd.Series({"test point ref des": "TP2", "x": 3, "y": 4})),
        ]
        distances = kicad_testpoints.calc_probe_distances("TP1", probes_df)
        self.assertIn("TP2", distances)
        self.assertAlmostEqual(distances["TP2"], 5.0)

    def test_get_pad_side_top(self):
        pad = MagicMock()
        footprint = MagicMock()
        footprint.GetSide.return_value = 0
        pad.GetParentFootprint.return_value = footprint
        pad.GetLayer.return_value = 0
        side = kicad_testpoints.get_pad_side(pad)
        self.assertEqual(side, "TOP")

    def test_get_pad_side_bottom(self):
        pad = MagicMock()
        footprint = MagicMock()
        footprint.GetSide.return_value = 1
        pad.GetParentFootprint.return_value = footprint
        pad.GetLayer.return_value = 0
        side = kicad_testpoints.get_pad_side(pad)
        self.assertEqual(side, "BOTTOM")

    def test_get_pad_position_uses_aux_origin(self):
        pad = MagicMock()
        board = MagicMock()
        ds = MagicMock()
        ds.GetAuxOrigin.return_value = (1000, 1000)
        board.GetDesignSettings.return_value = ds
        pad.GetBoard.return_value = board
        pad.GetCenter.return_value = (1100, 900)
        settings = kicad_testpoints.Settings()
        settings.use_aux_origin = True
        # Patch pcbnew.ToMM to just return the same coords for testing
        kicad_testpoints.pcbnew = MagicMock()
        kicad_testpoints.pcbnew.ToMM.side_effect = lambda x: x
        pos = kicad_testpoints.get_pad_position(pad, settings)
        expected = (1100 - 1000, -(900 - 1000))
        self.assertEqual(pos, [expected[0], expected[1]])

    def test_get_net_name(self):
        pad = MagicMock()
        pad.GetNetname.return_value = "GND"
        net_name = kicad_testpoints.get_net_name(pad)
        self.assertEqual(net_name, "GND")

    def test_build_test_point_report(self):
        pad = MagicMock()
        pad.GetParentFootprint.return_value.GetReferenceAsString.return_value = "U1"
        pad.GetNumber.return_value = "1"
        pad.GetNetname.return_value = "NET1"
        pad.GetNetClassName.return_value = "DEFAULT"
        pad.HasHole.return_value = True
        pad.GetParentFootprint.return_value.GetSide.return_value = 0
        pad.GetLayer.return_value = 0
        pad.GetCenter.return_value = (100, 200)
        board = MagicMock()
        ds = MagicMock()
        ds.GetAuxOrigin.return_value = None
        board.GetDesignSettings.return_value = ds
        settings = kicad_testpoints.Settings()
        pads = (pad,)

        kicad_testpoints.pcbnew = MagicMock()
        kicad_testpoints.pcbnew.PAD = MagicMock

        kicad_testpoints.pcbnew.ToMM.side_effect = lambda x: x
        report = kicad_testpoints.build_test_point_report(board, settings, pads)
        self.assertIsInstance(report, list)
        self.assertEqual(report[0]["source ref des"], "U1")
        self.assertEqual(report[0]["source pad"], "1")
        self.assertEqual(report[0]["net"], "NET1")
        self.assertEqual(report[0]["net class"], "DEFAULT")
        self.assertEqual(report[0]["pad type"], "THRU")
        self.assertEqual(report[0]["footprint side"], "TOP")

    def test_get_pads_found(self):
        board = MagicMock()
        module = MagicMock()
        board.FindFootprintByReference.return_value = module
        pad = MagicMock()
        pad.GetNumber.return_value = "1"
        module.Pads.return_value = [pad]
        pads = kicad_testpoints.get_pads((("U1", 1),), board)
        self.assertEqual(len(pads), 1)
        self.assertEqual(pads[0], pad)

    def test_get_pads_not_found(self):
        board = MagicMock()
        board.FindFootprintByReference.return_value = None
        with self.assertRaises(UserWarning):
            kicad_testpoints.get_pads((("U1", PAD()),), board)

    def test_get_pads_pad_not_found(self):
        board = MagicMock()
        module = MagicMock()
        module.Pads.return_value = []
        board.FindFootprintByReference.return_value = module
        with self.assertRaises(UserWarning):
            kicad_testpoints.get_pads((("U1", PAD()),), board)

    def test_get_pads_by_property(self):
        board = MagicMock()
        pad1 = MagicMock()
        pad2 = MagicMock()
        pad1.GetProperty.return_value = 4
        pad2.GetProperty.return_value = 5
        board.GetPads.return_value = [pad1, pad2]
        pads = kicad_testpoints.get_pads_by_property(board)
        self.assertIn(pad1, pads)
        self.assertNotIn(pad2, pads)

if __name__ == "__main__":
    unittest.main()
