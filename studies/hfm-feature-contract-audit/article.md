# My ML Feature Used the Wrong Unit. The Threshold Was 400× Too Large.

The live validator used a percentile of per-second net aggressive volume to
classify individual trades. That is a unit mismatch.

On the AAVEUSDT calibration example, p75 of individual trade quantity was 4.3
units. p75 of per-second NAV was 1,730 units. The latter is 402.3 times larger.
It made `large_share` close to zero for almost every live event.

The problem did not stop at one feature. The historical and live paths also
used different definitions of `run_frac`, `pre_vel`, and `trailing_nav`.

The October correction is not presented as a performance result. Raw October
trades were unavailable for two repaired features, so the 15,557-candidate
replay was analytical rather than exact. Its estimated −0.67 bps gross and
−10.67 bps after a 10 bps round-trip commission assumption are diagnostic
numbers only.

The public fixture tests the part that can be tested without market data:
individual-trade and per-second-volume thresholds must never be substituted for
each other.

Frozen result snapshot SHA-256: `d4b236d0129313287c5312e1c10b7d8820f010ae2d654a3c1f9f9dab1e50cc3d`
