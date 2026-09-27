I was not trying to prove a grand theory about crypto. I was testing simple, falsifiable baselines and looking for one result worth a second experiment.

Cross-sectional reversal looked almost too clean: Sharpe 13.44 before transaction costs, with positive returns in 67/76 out-of-sample windows. Then I charged the same signal for the trading it required. At 10 bps per side, net Sharpe fell to -40.13, and not one of those 76 windows remained positive.

That is not a typo. I genuinely did not see it coming — the pre-cost numbers looked clean enough that I spent twenty minutes checking whether I had made an error somewhere before I accepted the result. It is what can happen when a short-lived pattern asks for a new portfolio every 15 minutes.

---

## What I actually tested

15-minute bars from January 2021 to September 2025 on 451 Bybit USDT perpetual symbols:

- eight-bar (2-hour) return signal
- 90-day formation periods, 21-day OOS periods
- 76 non-overlapping OOS windows
- causal volatility targeting at 10% annualized, 96-bar trailing estimate, 3× leverage cap

The 451-symbol universe is not a point-in-time liquidity screen. Survivorship and availability bias are possible. This is a development diagnostic, not evidence of a deployable alpha.

---

## The signal was deliberately boring

At each timestamp: measure every asset's return over the previous 8 bars, standardize across the cross-section, reverse the sign. Recent relative losers get positive weights, winners get negative weights.

```python
recent = prices.select(
    "ts", (pl.col(symbols) / pl.col(symbols).shift(config.lookback_bars) - 1.0)
)
stats = long.group_by("ts").agg(
    mean=pl.col("return").mean(),
    standard_deviation=pl.col("return").std(),
)
signal = long.join(stats, on="ts").with_columns(
    signal=pl.when(pl.col("standard_deviation") > 0)
    .then(-(pl.col("return") - pl.col("mean")) / pl.col("standard_deviation"))
    .otherwise(0.0)
)
```

Weight at time `t` becomes live at `t+1` — no lookahead.

![The cost model implementation](https://raw.githubusercontent.com/icesurf666/quant-research-notes/main/studies/round1-cross-sectional-reversal/figures/workspace-cost-model.jpg)

---

## Zero-cost baseline

| Metric | Value |
|---|---:|
| Annualized Sharpe | 13.44 |
| Positive OOS windows | 67 / 76 (88.2%) |
| Max drawdown | -11.62% |
| Summed absolute turnover | 29,451 |

That last row is the warning. A huge pre-cost Sharpe and huge turnover can be two descriptions of the same fragile result.

I am not a professional quant. I run these experiments on my own time and try to document what actually happens rather than what I hoped would happen. When I saw 13.44 I let myself get briefly excited. That was a mistake.

![Before and after trading costs](https://raw.githubusercontent.com/icesurf666/quant-research-notes/main/studies/round1-cross-sectional-reversal/figures/baseline-vs-net.png)

---

## After adding costs

Using 6 bps fees + 4 bps slippage per side:

| Metric | Value |
|---|---:|
| Annualized Sharpe | -40.13 |
| Positive OOS windows | 0 / 76 |
| Cost / gross alpha | 4.00× |
| Total return | ~-100% |

I was hoping the cost model would hurt but leave something survivable. It did not.

The -40.13 is theatrical but mostly math: a stable negative cost stream annualized from 15-minute observations produces an absurdly negative ratio. The real number is that trading costs consumed 4× the gross PnL.

---

## Slowing it down

Under a pessimistic 15 bps/side scenario, net Sharpe improved as turnover fell:

| Rebalance interval | Net Sharpe | Positive OOS windows |
|---|---:|---:|
| Every 15 min | -66.00 | 0 / 76 |
| Every 4 hours | -16.24 | 0 / 76 |
| Every 1 day | -4.45 | 10 / 76 |

Best tested corner: daily rebalance + 3 bps/side → Sharpe -0.01, 39/76 positive. Still not there. The signal decayed while it waited.

![Cost sensitivity by rebalance interval](https://raw.githubusercontent.com/icesurf666/quant-research-notes/main/studies/round1-cross-sectional-reversal/figures/cost-sensitivity.png)

---

## What failed, and what did not

- **Research lead:** relative 2-hour moves contain a repeatable pre-cost pattern in this sample
- **Failed strategy:** resizing the book continuously consumes more than the pattern earns
- **Open engineering problem:** reduce turnover without waiting so long that the signal disappears

Specific follow-ups that make sense: threshold entries, hysteresis bands, cost-aware sizing, historical universe reconstruction, passive fill model. None assumed to work — just better questions than adding more indicators to the same high-turnover baseline.

---

## The result I kept

Turnover belongs inside the hypothesis from day one, not in the cleanup after a backtest looks good.

A pre-cost Sharpe is not a strategy. It is a claim before execution.

In this run, almost nothing remained.

---

Has anyone found a way to trade short-horizon reversal at 15-min bars profitably after realistic costs? Curious what execution approaches actually work here — threshold entries, passive execution, something else?
