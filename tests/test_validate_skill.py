from __future__ import annotations

import unittest
from pathlib import Path

from scripts.validate_skill import validate_package


class ValidateSkillTests(unittest.TestCase):
    def test_current_skill_package_is_valid(self) -> None:
        root = Path(__file__).resolve().parents[1]
        issues = validate_package(root)
        self.assertEqual(issues, [])


if __name__ == "__main__":
    unittest.main()
