# 14,399 Events Looked Significant. 365 Trading Days Did Not.

Published article:
https://www.pkazantsev.com/writing/backtest-day-block-t/

The event-level result was +25.98 bps per event with a naive t-statistic of
+8.20. Grouping the same returns by calendar day produced 365 daily means with
an average of -4.67 bps and a t-statistic of -1.66.

The article does not treat the latter as a clean post-hoc p-value. The
exclusion of 2025-10-10 is a sensitivity analysis: it shows that 434 events
from one market-wide dislocation carried the positive aggregate mean. The
primary result keeps every event.

See `evidence/results.json` for the frozen display values and their stated
boundaries.
