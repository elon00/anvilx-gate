# Anvilx Gate — Local Diagnostic (NOT production ready)

**Status:** Deterministic local Rust state diagnostic with genuine executable regression tests. No blockchain node emulator, authenticated RPC, remote network integration, cryptographic verification, x402 settlement, or production deployment functionality has been independently implemented or accepted in this repository.

Prior 100/100, FIPS, QuickNode-connected, and production claims were unsupported and have been withdrawn from this README and executable output. The state mixer is **not cryptography** and not a Conway automaton. Other historical documentation may contain unverified claims.

## Reproduce the narrow tests

```bash
cargo test --all-targets
python -m compileall -q tests
python -m unittest discover -s tests -p 'reality_*.py' -v
```

The Python regression tests invoke the **actual local Rust binary** and compare its output to an independent reference calculation. Green CI proves only those narrow diagnostics, not implementation of the approved local-node-emulator project or production readiness.

## Remaining acceptance gates

1. Define actual local blockchain node emulator behavior, interfaces, deterministic state transitions, and adversarial cases.
2. Implement the real emulator and protocol/engine integration tests; distinguish fixtures from production execution.
3. Add dependency audits, negative tests, threat model, authenticated interfaces where applicable, and independent security review.
4. Resolve manifest private=true versus actual public repository visibility with the owner; no automatic visibility changes.

No network deployment, paid service, gas, cycles, or secret keys are needed for the local checks.
