---
title: Three Crypto Edges. Three Different Killers.
description: Three crypto research candidates encountered different failure points: modelled costs, a reported holdout result, and parameter sensitivity.
tags: algotrading, python, datascience, machinelearning
cover_image: https://raw.githubusercontent.com/icesurf666/quant-research-notes/main/studies/round2-three-edges-three-killers/figures/research_summary.png
canonical_url: https://www.pkazantsev.com/writing/three-edges-three-killers/
---

A research platform should not make it easy to stop at a good-looking number. My research process uses transaction-cost checks, held-out evaluation, and parameter sweeps. Not every candidate reaches every stage. These three failed at different points; here is what the reported results show and what they leave unresolved.

| Edge | Peak result | Killer | Verdict |
|---|---|---|---|
| Price mean reversion | Gross Sharpe 7–13 | Transaction costs | REJECT |
| Funding carry | +48.6% net, Sharpe 1.17 | Reported holdout result | REJECT |
| Daily momentum | +97% net, best case | Robustness checks | WEAK |

## Edge 1: Mean reversion, killed by costs

Cross-sectional reversal on 15-minute crypto bars had a gross Sharpe between 7 and 13, positive in over 80% of out-of-sample windows across 76 test periods. In this development sample, recent relative losers tended to outperform recent relative winners before transaction costs.

None of the tested implementations produced a robust net result after modelled costs. Rebalancing every bar, friction ran 5 to 10 times the size of the available edge. I tested entry and exit thresholds, hysteresis to reduce turnover, slower timeframes, and less frequent rebalancing. Nothing produced a parameter plateau. Adjacent settings swung from +45% to −60% net. Positive settings existed, but they did not establish a stable, tradeable result.

Diagnosis: a strong pre-cost pattern without a robust net implementation under the tested execution assumptions.

These figures summarize the earlier research revisions in the source report. A [separate deep-dive](https://pkazantsev.com/writing/crypto-backtest-trading-costs/) examines a controlled evaluation; its metrics should not be mixed with this summary as if they came from one run.

## Edge 2: Funding carry, rejected after holdout evaluation

Funding carry is structurally different from price reversion: long spot, short the perpetual, collect the funding rate. Lower turnover reduces the transaction-cost burden; it does not eliminate execution costs or other risks. On development data covering 4.5 years across 76 walk-forward windows, the result was +48.6% net, Sharpe 1.17, positive every single year including the 2022 bear market.

Before treating that as a tradeable result, I ran two tests. A null decomposition shuffled which coin's funding the strategy received. The null still made +28%, suggesting that a substantial part of the development return did not depend on selecting the right coins. This was evidence of a shared funding premium in that sample, not proof of a durable selection edge.

The original report describes a frozen strategy evaluated on a reserved interval from September 1, 2025 to September 1, 2026. It reports −0.5% net return and Sharpe −0.02. These are historical reported results, not a rerun performed for this article.

A later code audit found two qualifications. First, the current evaluator generates 17 complete 21-day trading windows, covering September 1, 2025 through August 24, 2026 (exclusive): 357 days, not the full reserved year. The original run's saved window list is not included in this evidence package, so this code inspection does not independently establish the exact coverage of that historical result.

Second, the evaluator selects eligible coins from the current data cache, including a funding-record-count filter applied before date restriction. Without the original frozen universe and a dated run manifest, I cannot rule out future data availability influencing that selection. The report calls the interval sealed; the public package does not independently demonstrate an untouched holdout.

![Reported funding-carry Sharpe: development 1.17, holdout −0.02](https://raw.githubusercontent.com/icesurf666/quant-research-notes/main/studies/round2-three-edges-three-killers/figures/carry_reported_sharpe.png)

*Reported Sharpe values, not a fresh reproduction. Development return was +48.6% over approximately 4.5 years; reported holdout return was −0.5%. No annualized-return comparison is plotted because exact historical coverage is not independently verified here.*

Diagnosis: the reported holdout result did not reproduce development performance. It supports the research decision not to advance this candidate, not proof that the market-wide funding premium disappeared. Low turnover does not exclude costs as a contributor; the cause of that failure remains unresolved.

Distinguishing premium decay from selection failure requires a comparison that controls for exposure, turnover and execution costs. Follow-up analysis of the opened interval is exploratory, not a fresh out-of-sample confirmation.

## Edge 3: Daily momentum, killed by robustness

Daily cross-sectional momentum trades a weekly rebalance and survives costs where 15-minute reversion could not. The best configuration produced +97% net even at taker fees. But a single number is not a result.

The lookback sweep was not a plateau. It was a spike: 7 days +33%, 10 days −23%, 14 days +97%, 21 days +35%. The +97% configuration was not locally robust. Without an economic reason to prefer exactly 14 days over 10 or 21, I could not distinguish discovery from parameter selection.

![Momentum net returns at four lookback settings: +33%, −23%, +97%, +35%](https://raw.githubusercontent.com/icesurf666/quant-research-notes/main/studies/round2-three-edges-three-killers/figures/momentum_sweep.png)

*Rounded development returns reported in the frozen research summary. These are parameter comparisons, not four independent validation results.*

The regime analysis completed the picture: about half the return came from the 2021 bull market, with 2022 negative. That profile is consistent with residual market exposure, but this experiment did not estimate a formal beta decomposition.

Diagnosis: a single parameter island without a supporting plateau, plus material regime dependence. The result was not robust enough to call neutral momentum alpha.

## Three different failure points

If all three edges had failed the same way, the lesson would be narrow. Mean reversion failed at the execution layer before reaching a holdout. Funding carry reported −0.5% net in its holdout evaluation, with the provenance qualifications described above. Momentum failed on the question of whether the result was robust or merely the best-looking number in a sweep.

Each guard catches a different class of failure. A research process that only runs one can miss weaknesses exposed by the others. Running all three identifies where a candidate fails; it does not always identify the economic cause.

## No strategy ready to trade.

No tradeable edge came out of this. What the framework produced was a bounded diagnosis for each hypothesis: one pre-cost pattern failed the tested execution assumptions, one carry candidate did not reproduce development performance in its reported holdout evaluation, and one momentum result failed local robustness checks.

The next hypothesis goes into the same framework, not into a live account.

This article summarizes development backtests, not live trading. The [frozen research report and figures](https://github.com/icesurf666/quant-research-notes/tree/main/studies/round2-three-edges-three-killers) document the reported results; the package is not a complete independent reproduction of the private data pipeline. Its SHA-256 checks establish file identity, not the correctness of the backtests. The original summary retains stronger causal claims that this article does not endorse. Machine-readable historical results, run configurations and a frozen universe are still needed for an independent numerical audit.

Evidence source SHA-256: `cf9ce73542af24be3e5c2872864b2b41c6ce864e3b2f07b760e5434a1bdb23ba`

---

*Research system: HFM · Development walk-forward evaluation · Bybit spot and perpetuals · Python*
