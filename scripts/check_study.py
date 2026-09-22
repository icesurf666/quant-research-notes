"""Validate a public study's claims, limitations, figures, and frozen hashes."""

from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{path} must contain a JSON object")
    return value


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: check_study.py STUDY_DIRECTORY")
    study = Path(sys.argv[1]).resolve()
    metrics = load_json(study / "evidence" / "metrics.json")
    results_path = study / "evidence" / "results.json"
    results = load_json(results_path)
    manifest = load_json(study / "manifest.json")
    review = load_json(study / "review.json")
    article_path = study / "article.md"
    article = article_path.read_text(encoding="utf-8")

    failures: list[str] = []
    results_hash = sha256(results_path)
    article_hash = sha256(article_path)
    if results_hash != metrics["results_sha256"]:
        failures.append("results snapshot hash does not match metrics.json")
    if results_hash not in article:
        failures.append("article is missing the results snapshot hash")
    if review["article_sha256"] != article_hash:
        failures.append("review does not identify the current article")
    if review["results_sha256"] != results_hash:
        failures.append("review does not identify the current results snapshot")
    if not review.get("passed"):
        failures.append("editorial review is not passing")

    scenarios = results["scenarios"]
    headline_checks = {
        "zero_transaction_cost_sharpe": scenarios["baseline_every_bar_zero_transaction_bps"][
            "metrics"
        ]["sharpe"],
        "zero_transaction_cost_positive_oos_windows": scenarios[
            "baseline_every_bar_zero_transaction_bps"
        ]["metrics"]["fraction_positive_windows"],
        "zero_transaction_cost_max_drawdown": scenarios["baseline_every_bar_zero_transaction_bps"][
            "metrics"
        ]["max_drawdown"],
        "zero_transaction_cost_total_turnover": scenarios[
            "baseline_every_bar_zero_transaction_bps"
        ]["metrics"]["total_turnover"],
        "net_sharpe_10_bps": scenarios["net_every_bar_10_bps"]["metrics"]["sharpe"],
        "net_positive_oos_windows_10_bps": scenarios["net_every_bar_10_bps"]["metrics"][
            "fraction_positive_windows"
        ],
        "net_total_return_10_bps": scenarios["net_every_bar_10_bps"]["metrics"]["total_return"],
        "oos_windows": results["walk_forward"]["n_windows"],
        "cost_to_gross_alpha_10_bps": scenarios["net_every_bar_10_bps"]["metrics"][
            "cost_to_gross_alpha"
        ],
    }
    for key, actual in headline_checks.items():
        expected = metrics["headline"][key]
        if not math.isclose(float(actual), float(expected), rel_tol=0.0, abs_tol=1e-12):
            failures.append(f"headline metric drift: {key}")

    sensitivity_checks = {
        ("pessimistic_15_bps", "every_bar"): scenarios["net_every_bar_15_bps"]["metrics"]["sharpe"],
        ("pessimistic_15_bps", "every_bar_positive_windows"): scenarios["net_every_bar_15_bps"][
            "metrics"
        ]["fraction_positive_windows"],
        ("pessimistic_15_bps", "every_16_bars"): scenarios["net_4h_15_bps"]["metrics"]["sharpe"],
        ("pessimistic_15_bps", "every_16_bars_positive_windows"): scenarios["net_4h_15_bps"][
            "metrics"
        ]["fraction_positive_windows"],
        ("pessimistic_15_bps", "every_96_bars"): scenarios["net_daily_15_bps"]["metrics"]["sharpe"],
        ("pessimistic_15_bps", "every_96_bars_positive_windows"): scenarios["net_daily_15_bps"][
            "metrics"
        ]["fraction_positive_windows"],
        ("daily", "maker_3_bps"): scenarios["net_daily_maker_3_bps"]["metrics"]["sharpe"],
        ("daily", "maker_3_bps_positive_windows"): scenarios["net_daily_maker_3_bps"]["metrics"][
            "fraction_positive_windows"
        ],
        ("daily", "taker_7_5_bps"): scenarios["net_daily_taker_7_5_bps"]["metrics"]["sharpe"],
        ("daily", "taker_7_5_bps_positive_windows"): scenarios["net_daily_taker_7_5_bps"][
            "metrics"
        ]["fraction_positive_windows"],
    }
    for (group, key), actual in sensitivity_checks.items():
        expected = metrics["sensitivity"][group][key]
        if not math.isclose(float(actual), float(expected), rel_tol=0.0, abs_tol=1e-12):
            failures.append(f"sensitivity metric drift: {group}.{key}")

    strategy_name = str(results["strategy"])
    try:
        signal_lookback = int(strategy_name.rsplit("l", maxsplit=1)[1])
    except (IndexError, ValueError):
        failures.append(f"cannot derive signal lookback from strategy: {strategy_name}")
        signal_lookback = -1
    reproduction_checks = {
        "cached_symbol_directories": results["universe"]["cached_symbol_directories"],
        "data_file_count": results["data_fingerprint"]["file_count"],
        "data_byte_size": results["data_fingerprint"]["byte_size"],
        "formation_days": results["walk_forward"]["formation_days"],
        "oos_days": results["walk_forward"]["oos_days"],
        "step_days": results["walk_forward"]["step_days"],
        "lookback_bars": signal_lookback,
        "target_ann_vol": results["normalization"]["target_ann_vol"],
        "vol_lookback_bars": results["normalization"]["vol_lookback_bars"],
        "max_leverage": results["normalization"]["max_leverage"],
    }
    for key, actual in reproduction_checks.items():
        expected = metrics["reproduction"][key]
        if not math.isclose(float(actual), float(expected), rel_tol=0.0, abs_tol=1e-12):
            failures.append(f"reproduction setting drift: {key}")

    for display in metrics["locked_displays"]:
        if display not in article:
            failures.append(f"article is missing locked display: {display}")
    for limitation in metrics["limitations"]:
        if limitation not in article:
            failures.append(f"article is missing limitation: {limitation}")
    for banned in metrics["banned_claims"]:
        if banned.lower() in article.lower():
            failures.append(f"article contains banned claim: {banned}")
    for marker in metrics["required_code_markers"]:
        if marker not in article:
            failures.append(f"article is missing required code marker: {marker}")
    for relative, expected in manifest["sha256"].items():
        path = study / relative
        if not path.is_file():
            failures.append(f"manifest file is missing: {relative}")
        elif sha256(path) != expected:
            failures.append(f"hash drift: {relative}")
    if failures:
        raise SystemExit("\n".join(failures))


if __name__ == "__main__":
    main()
