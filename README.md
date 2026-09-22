# Quantitative Research Notes

This repository contains compact, reproducible evidence packages for published
quantitative engineering studies. It is not a strategy catalog and does not
present development backtests as deployable trading systems.

Each folder under `studies/` contains:

- the article;
- immutable headline metrics and limitations;
- figures used by the article;
- a manifest of file hashes;
- only the reusable code required to understand the mechanism.

The first study is
[`round1-cross-sectional-reversal`](studies/round1-cross-sectional-reversal/README.md).

## Research standard

Each published result is treated as an auditable claim. A study must include:

- a machine-readable result snapshot tied to one code and data revision;
- the assumptions and accounting identities required to interpret the result;
- deterministic tests for causal timing and portfolio mechanics;
- visible limitations and an explicit evidence status;
- integrity checks that fail when the article, figures, metrics, or review record drift.

Development backtests are reported as development evidence. Lockbox, paper-trading,
and live results are labeled separately and are never inferred from one another.

## What can be reproduced

The tests reproduce the signal construction, execution delay, unit-gross
normalization, turnover accounting, and cost identity on deterministic fixtures.
The full historical result cannot be reproduced from this repository because the
market-data cache is not distributed here. The study manifest states that boundary
explicitly.

## Quality gate

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
make quality
```

`make quality` fails on formatting, lint, strict typing, tests, evidence drift,
common secret patterns, private filesystem paths, or accidental data files.
