"""Verify frozen values and artifact hashes for the public feature-contract package."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

STUDY = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    results_path = STUDY / "evidence" / "results.json"
    results = json.loads(results_path.read_text(encoding="utf-8"))
    manifest = json.loads((STUDY / "manifest.json").read_text(encoding="utf-8"))

    example = results["large_share_unit_mismatch"]["aaveusdt_example"]
    assert example["per_trade_quantity_p75"] == 4.3
    assert example["per_second_nav_p75"] == 1730.0
    assert example["ratio"] > 400.0
    assert results["candidate_count"] == 15557
    assert results["analytical_replay"]["multi_day"]["exact_reconstruction"] is False

    for relative_path, expected_hash in manifest["sha256"].items():
        actual_hash = sha256(STUDY / relative_path)
        assert actual_hash == expected_hash, f"hash drift: {relative_path}"

    print("hfm-feature-contract-audit: evidence snapshot and manifest verified")


if __name__ == "__main__":
    main()
