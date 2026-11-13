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
- frozen audit metrics and artifact hashes.

## What it does not reproduce

The full October 2026 market-data archive is not distributed. In particular,
raw October trades were unavailable for two corrected features. This package
does not reproduce the 15,557-candidate analytical replay and does not make a
claim about deployable trading performance.

The public snapshot records that the analytical replay estimated −0.67 bps
gross and −10.67 bps after a 10 bps round-trip commission assumption. Those
are audit diagnostics, not reproduced strategy results.

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
