"""Executable integration tests against the actual Rust local diagnostic.

No mock network success, blockchain emulator, PQC, TLS or production acceptance.
"""
from pathlib import Path
import re
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
MASK = (1 << 64) - 1
SEED = 0x55AA55AA55AA55AA
MIX = 0x9E3779B97F4A7C15


def reference_state(rounds=10_000):
    state = SEED
    for _ in range(rounds):
        rotated = ((state >> 7) | ((state << 57) & MASK)) & MASK
        state = (state ^ rotated ^ MIX) & MASK
    return state


class ActualRustBinaryRegression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proc = subprocess.run(
            ["cargo", "run", "--quiet"], cwd=ROOT,
            text=True, capture_output=True, timeout=120, check=True,
        )

    def test_actual_binary_matches_independent_reference(self):
        match = re.search(r"^STATE_HEX=([0-9a-f]{16})$", self.proc.stdout, re.M)
        self.assertIsNotNone(match, self.proc.stdout)
        self.assertEqual(int(match.group(1), 16), reference_state())

    def test_binary_declares_missing_capabilities(self):
        output = self.proc.stdout
        self.assertIn("IMPLEMENTATION_STATUS=PLACEHOLDER", output)
        self.assertIn("SECURITY_STATUS=UNVERIFIED", output)
        self.assertIn("NETWORK_STATUS=NOT_CONNECTED", output)
        for claim in ("100/100", "FIPS", "CERTIFIED", "RPC Gateway: CONNECTED"):
            self.assertNotIn(claim, output)


if __name__ == "__main__":
    unittest.main()
