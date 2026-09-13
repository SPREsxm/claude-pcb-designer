from __future__ import annotations

import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.audit_release import classify, run_audit


GERBER = """%FSLAX46Y46*%
%MOMM*%
%ADD10C,0.250000*%
D10*
X100000Y100000D02*
X200000Y100000D01*
M02*
"""


def write_release(root: Path, include_bom: bool = True, mismatch: bool = False) -> None:
    (root / "board.gtl").write_text(GERBER, encoding="utf-8")
    (root / "board.gbl").write_text(GERBER, encoding="utf-8")
    (root / "board.gts").write_text(GERBER, encoding="utf-8")
    (root / "board.gbs").write_text(GERBER, encoding="utf-8")
    (root / "board.gko").write_text(GERBER, encoding="utf-8")
    (root / "board.drl").write_text(
        "M48\nMETRIC\nT1C0.300\n%\nT1\nX0Y0\nM30\n",
        encoding="utf-8",
    )
    if include_bom:
        second_designator = "C2" if mismatch else "C1"
        (root / "bom.csv").write_text(
            "Designator,Qty,MPN,Package\n"
            "R1,1,RC0603FR-0710KL,0603\n"
            f"{second_designator},1,GRM188R71C104KA01D,0603\n",
            encoding="utf-8",
        )
        (root / "cpl.csv").write_text(
            "Designator,Mid X,Mid Y,Layer,Rotation\n" "R1,1.0,2.0,Top,0\n" "C1,2.0,2.0,Top,90\n",
            encoding="utf-8",
        )


class AuditReleaseTests(unittest.TestCase):
    def test_kicad_style_layer_names_classify(self) -> None:
        self.assertEqual(classify("F_Cu.gbr", GERBER), "top_copper")
        self.assertEqual(classify("B_Cu.gbr", GERBER), "bottom_copper")
        self.assertEqual(classify("In1_Cu.gbr", GERBER), "inner_copper_1")
        self.assertEqual(classify("F_Mask.gbr", GERBER), "top_mask")
        self.assertEqual(classify("B_Mask.gbr", GERBER), "bottom_mask")
        self.assertEqual(classify("F_Silkscreen.gbr", GERBER), "top_silk")
        self.assertEqual(classify("Edge_Cuts.gbr", GERBER), "outline")
        self.assertEqual(classify("F_Paste.gbr", GERBER), "top_paste")

    def test_complete_release_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_release(root)
            result = run_audit(root, layers=2)
        self.assertEqual(result.errors, [])
        self.assertEqual(result.warnings, [])
        self.assertEqual(result.bom_designators, {"R1", "C1"})
        self.assertEqual(result.cpl_designators, {"R1", "C1"})

    def test_missing_layers_are_errors(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "board.gtl").write_text(GERBER, encoding="utf-8")
            result = run_audit(root, pcb_only=True, layers=2)
        codes = {issue.code for issue in result.errors}
        self.assertIn("missing-bottom_copper", codes)
        self.assertIn("missing-top_mask", codes)
        self.assertIn("missing-outline", codes)
        self.assertIn("missing-drill", codes)

    def test_bom_cpl_mismatch_is_warning(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_release(root, mismatch=True)
            result = run_audit(root, layers=2)
        codes = {issue.code for issue in result.warnings}
        self.assertIn("bom-cpl-bom-only", codes)
        self.assertIn("bom-cpl-cpl-only", codes)

    def test_zip_release(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_release(root)
            archive = root / "release.zip"
            with zipfile.ZipFile(archive, "w") as output:
                for path in root.iterdir():
                    if path != archive and path.is_file():
                        output.write(path, path.name)
            result = run_audit(archive, layers=2)
        self.assertEqual(result.errors, [])
        self.assertEqual(result.warnings, [])


if __name__ == "__main__":
    unittest.main()
