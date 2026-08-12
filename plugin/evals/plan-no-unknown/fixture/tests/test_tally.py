"""Byte-for-byte guard on the text output of `tally`."""

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GOLDEN = ROOT / "tests" / "golden" / "two-files.txt"
ARGUMENTS = ["tests/data/a.txt", "tests/data/b.txt"]


class TextOutputTest(unittest.TestCase):
    def test_two_files_match_the_recorded_output(self):
        result = subprocess.run(
            [sys.executable, "tally.py", *ARGUMENTS],
            cwd=ROOT,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, GOLDEN.read_bytes())


if __name__ == "__main__":
    unittest.main()
