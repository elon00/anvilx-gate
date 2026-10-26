"""Fail-closed local source-integrity tests; not simulated protocol verification."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class SourceIntegrity(unittest.TestCase):
    def test_rust_source_has_no_control_bytes(self):
        source = (ROOT / "src" / "main.rs").read_bytes()
        invalid = [byte for byte in source if byte < 32 and byte not in (9, 10, 13)]
        self.assertEqual(invalid, [])

    def test_no_unearned_security_or_network_claims(self):
        source = (ROOT / "src" / "main.rs").read_text(encoding="utf-8")
        for claim in (
            "Treasury Escrows Verified",
            "Security Vault: ACTIVE",
            "RPC Gateway: CONNECTED",
            "Production Invariant Cycles",
        ):
            self.assertNotIn(claim, source)


if __name__ == "__main__":
    unittest.main()
