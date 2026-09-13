from __future__ import annotations

import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.package_skill import package, skill_version


class PackageSkillTests(unittest.TestCase):
    def test_package_contains_runtime_files(self) -> None:
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(skill_version(root), "3.0.0")
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "pcb-designer.zip"
            package(root, output)
            with zipfile.ZipFile(output) as archive:
                names = set(archive.namelist())
        self.assertIn("pcb-designer/SKILL.md", names)
        self.assertIn("pcb-designer/references/release-checklist.md", names)
        self.assertIn("pcb-designer/scripts/pcbcalc.py", names)
        self.assertIn("pcb-designer/templates/design-brief.md", names)


if __name__ == "__main__":
    unittest.main()
