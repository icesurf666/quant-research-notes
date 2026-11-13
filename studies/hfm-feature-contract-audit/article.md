# My ML Feature Used the Wrong Unit. The Threshold Was 400× Too Large.

The live validator used a percentile of per-second net aggressive volume to
classify individual trades. That is a unit mismatch.

On the AAVEUSDT calibration example, p75 of individual trade quantity was 4.3
units. p75 of per-second NAV was 1,730 units. The latter is 402.3 times larger.
It made `large_share` close to zero for almost every live event.

The problem did not stop at one feature. The historical and live paths also
used different definitions of `run_frac`, `pre_vel`, and `trailing_nav`.

The raw Binance archive was later recovered for the recorded sessions. The
four affected feature families were rebuilt at the original timestamps for
14,681 of 14,682 candidates; one LDOUSDT detection second was absent from the
archive. Matching frozen artifacts reproduced the recorded scores with a mean
absolute difference of 1.04×10⁻⁶.

The repaired features selected 52 candidates. Their raw five-second Binance
markout averaged +8.67 bps and −1.33 bps after a 10 bps round-trip fee
assumption. No strategy was promoted. This is not an execution test: it keeps
candidate generation and the logged `nav_abs` / `nav_overshoot` convention
fixed, and raw markout is not an executable fill.

The public fixture tests the part that can be tested without market data:
individual-trade and per-second-volume thresholds must never be substituted for
each other.

Frozen result snapshot SHA-256 is recorded in `manifest.json`.
