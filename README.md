# Pavel Kazantsev: research companions

This repository contains the smallest public artifact needed to inspect the code
behind a published engineering article. It is not a mirror of my private research
system and it is not a collection of trading strategies.

Each folder under `studies/` owns:

- the article;
- immutable headline metrics and limitations;
- figures used by the article;
- a manifest of file hashes;
- only the reusable code required to understand the mechanism.

The first study is
[`round1-cross-sectional-reversal`](studies/round1-cross-sectional-reversal/README.md).

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
