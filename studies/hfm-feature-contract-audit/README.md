# HFM feature-contract audit

Companion evidence package for
[`My ML Feature Used the Wrong Unit. The Threshold Was 400× Too Large.`](https://www.pkazantsev.com/writing/ml-feature-drift/)

## Claim

The historical and live pipelines used the name `large_share` for different
computations. The historical feature classified **individual trade quantities**
against a per-trade threshold. The live validator classified individual trades
against a percentile of **per-second net aggressive volume**. The latter was
163–423 times larger on affected symbols.

For the AAVEUSDT calibration example, the recorded per-trade p75 was 4.3 units
and the per-second NAV p75 was 1,730 units, a ratio of 402.3×. Almost no
individual trade can exceed the second quantity, so the live feature collapsed
toward zero.

The audit also found contract mismatches in `run_frac`, `pre_vel`, and
`trailing_nav`.

## What this package reproduces

- the unit-mismatch mechanism on deterministic synthetic trade inputs;
- the exact p75 values used in the public AAVEUSDT example;
- the resulting `large_share` collapse;
- the distinction between a feature-contract test and a market-performance
  claim;
- a frozen summary of the later raw-trade reconstruction;
- frozen audit metrics and artifact hashes.

## What it does not reproduce

The full October 2026 market-data archive is not distributed. This package does
not rerun the raw reconstruction, nor does it distribute exchange data. It
records the immutable aggregate result instead: four repaired feature families
were rebuilt for 14,681 of 14,682 recorded candidates. The resulting 52
selected candidates averaged +8.67 bps on a raw five-second Binance markout
and −1.33 bps after a 10 bps round-trip fee assumption.

That result is a feature-reconstruction check, not a claim about deployable
trading performance. It retains the original candidate-generation path and the
logged `nav_abs` / `nav_overshoot` convention; a raw Binance markout is not an
executable fill.

## Verify

```bash
python -m pytest studies/hfm-feature-contract-audit/reproduction/test_feature_contract.py
python studies/hfm-feature-contract-audit/verify.py
```

## Why this is a separate study

A distribution-drift test can show that two feature distributions differ. It
cannot show whether the two implementations used the same unit, aggregation
window, or direction convention. Feature parity needs both implementations to
run against the same recorded raw input before model scores are interpreted.
