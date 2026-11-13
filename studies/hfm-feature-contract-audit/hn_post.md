Show HN: I found a train/serve feature bug with a 402× threshold mismatch

I built a small public fixture from a production-audit failure in a crypto ML
pipeline. The historical code defined `large_share` using individual trade
quantities. The live code used the 75th percentile of per-second net aggressive
volume as a cutoff for individual trades.

In the public AAVEUSDT example, those thresholds are 4.3 and 1,730. The second
is 402× larger, so the live feature becomes zero on the supplied trades even
though the batch feature is 0.741.

The package has a dependency-free reproduction, tests, a frozen audit snapshot,
and an explicit boundary: it does not reproduce the private October market-data
archive or claim a trading result.

Repository: https://github.com/icesurf666/quant-research-notes/tree/main/studies/hfm-feature-contract-audit
