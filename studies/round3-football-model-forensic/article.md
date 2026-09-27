---
title: My Football Model Passed Validation. A Five-Check Audit Killed It.
description: Val away CLV was +152 bps, confidence interval excluded zero. Then I ran five forensic checks. Four failed, one passed, and the pass made the four failures harder to argue away.
tags: machinelearning, python, datascience, research
cover_image: https://raw.githubusercontent.com/icesurf666/quant-research-notes/main/studies/round3-football-model-forensic/figures/clv_decomposition.png
canonical_url: https://pkazantsev.com/writing/football-model-forensic/
---

My football prediction model passed validation. Val away CLV was +152 bps, confidence interval excluded zero. Then I ran five forensic checks. Four failed, one passed, and the pass made the four failures harder to argue away.

## The experiment

The hypothesis: EPL bookmakers systematically underprice high-odds away teams. A LightGBM classifier trained on seven seasons of opening-line data would find those games and generate positive closing line value.

CLV is `mean(model_prob - devigged_closing_prob)`. Devigging removes the bookmaker's margin from decimal odds to recover fair probabilities that sum to 1. Positive CLV means your model put higher probability on an outcome than the final Pinnacle price did, after sharp money finished moving it. It is the standard measure of model skill in sports prediction research.

14 features, all opening-line: devigged Pinnacle probabilities, B365, market consensus, Pinnacle-vs-consensus disagreement, raw decimal odds. No temporal index, no threshold from the full dataset. LightGBM with `n_estimators=300, learning_rate=0.03, num_leaves=15`, hyperparameters locked before touching val. Logistic regression as a same-feature baseline. 380 val games (EPL 2022-23). One pre-registered hypothesis: AWAY outcome.

The surface result:

| Split | Outcome | CLV | CI | Status |
|-------|---------|----:|-----|--------|
| Val 2223 | **Away** | **+152 bps** | [+55, +251] | CLV_ONLY_BRIER_FAIL |
| Val 2223 | Home | −39 bps | [−132, +52] | NULL_RESULT |
| Test 2324 | Away | +11 bps | [−79, +100] | NULL_RESULT |
| Test 2324 | Home | +176 bps | [+95, +263] | CLV_ONLY_BRIER_FAIL |

Val away CI excludes zero, which is what the hypothesis required. The verdict column reads `CLV_ONLY_BRIER_FAIL` rather than `EDGE_CANDIDATE` because the protocol requires positive CLV *and* Brier improvement over the closing line. Five forensic checks determined why.

## Check 1: What does the market itself drift?

Any model trained on opening odds will inherit whatever directional drift the market already has between open and close. Measure that drift first, with no model, so you know what the baseline is.

Val away drift: **+3.9 bps** (CI: −19.5 to +26.8, crosses zero). No systematic directional movement in 2022-23 for away outcomes.

The model showed +152 bps on the same split, so +148 bps was model-generated with no structural drift to explain it.

## Check 2: Brier skill score

A model that systematically overestimates probabilities in the right direction will show positive CLV while being less accurate than the market. Brier score separates the two. To claim predictive value, the model needs a lower Brier score than the closing line on the same games.

![Model Brier score vs closing line across 6 split-outcome combinations. Lower is better.](https://raw.githubusercontent.com/icesurf666/quant-research-notes/main/studies/round3-football-model-forensic/figures/brier_comparison.png)

*Model Brier vs closing line, all 6 split-outcome combinations. Lower is better. The model is worse on every single one.*

The model lost on Brier in all six combinations. Delta ranged from +0.004 to +0.019, consistently worse than the closing line.

> A model can beat the closing line on CLV while losing to it on Brier. It is overestimating probabilities in the right direction at the wrong magnitude. That is systematic bias.

## Check 3: Feature cleanliness

The first version of this experiment had two contaminated features. `season_num` was a global index 0-8 derived from the full nine-season dataset, so val season got index 7 and the model extrapolated outside its training range. `is_high_odds_away` was a binary flag using a threshold of 0.62 set by a calibration run on all nine seasons, including val and test.

I removed both and reran from scratch with 14 features: opening odds from Pinnacle, B365, and market consensus; bookmaker disagreement; raw decimal odds. All from pre-match data only. Check 3: PASS. Zero violations.

Removing the contaminated features dropped val away CLV from +216 bps to +152 bps, so the contamination was inflating the result by about 64 bps. With a clean feature set, the remaining failures have nothing to blame.

## Check 4: Incremental CLV

Standard CLV is `model_prob - close_prob`. To separate the model's contribution from the market's own drift, compute `model_prob - open_prob` instead. The closing line cancels algebraically:

```
(model - close) - (open - close) = model - open
```

![Val away CLV decomposed. Market drifted +3.9 bps. Model added +147.7 bps.](https://raw.githubusercontent.com/icesurf666/quant-research-notes/main/studies/round3-football-model-forensic/figures/clv_decomposition.png)

*Val away CLV decomposed. Market drifted +3.9 bps. Model added +147.7 bps. The model contributes 38x the underlying signal.*

The model pushed away probabilities **147.7 bps above the opening line** (CI: [+52.5, +244.4]). True market drift was +3.9 bps. The model overshot by 38x.

On test, the same model produced +11 bps CLV for away (CI: [−79, +100], crosses zero). The model was overestimating away probabilities in both splits. In val that overshoot happened to align with a small positive drift. In test it produced noise.

## Check 5: Season stability

If removing one training season flips the sign of the result, the result depends on that season, not on a real underlying relationship. Leave-one-out validation removes one training season at a time and re-measures val CLV.

| Outcome | Mean CLV | Std | Range | Sign stable? |
|---------|----------:|----:|------:|:---:|
| Home | −39.7 bps | 85.6 | [−200, +114] | No |
| Draw | −134.2 bps | 44.2 | [−213, −81] | Yes (consistently negative) |
| **Away** | **+106.3 bps** | **126.6** | **[−151, +314]** | **No (sign flips)** |

Away CLV standard deviation: 126.6 bps. Removing season 2020-21 gives +314 bps, removing season 2021-22 gives −151 bps. The val result is entirely a function of which seasons happened to land in the training set.

## Four failures. One pass. Verdict unchanged.

Fixing the contamination improved the experiment, not the result. The core failures are independent of the bad features.

| Check | Finding | Status |
|-------|---------|--------|
| Opening-line baseline | True drift +3.9 bps; model added 38x more | FAIL |
| Brier skill score | Model worse than market on all 6 combinations | FAIL |
| Feature cleanliness | 14 features, zero violations, clean rerun | PASS |
| Incremental CLV | Model overshoots by 148 bps; collapses to noise on test | FAIL |
| Season stability | Std 126.6 bps, sign flips on leave-one-out | FAIL |

Logistic regression on the same features: val away CLV +87 bps (CI: [+57, +117]), Brier 0.185 vs closing 0.182, test away −102 bps (CI: [−135, −71]). Same pattern. The calibration failure is not specific to LightGBM.

All four failing checks trace to the same thing: the model overestimates away probabilities. In 2022-23 that overshoot happened to align with a small and statistically insignificant positive drift. In 2023-24 it produced +11 bps with a CI that crosses zero. REJECT.

## The contamination fix that changed nothing

Val away CLV dropped from 216 to 152 bps when the contaminated features were removed. The contamination inflated the number. But 152 bps still excludes zero, so one could argue the signal survived.

Brier closes that argument. With clean features, on both val and test, the model is less accurate than the closing line on all six outcome-split combinations. A model that cannot beat the market's accuracy is overfit, not predictive. The contamination was real. Removing it changed the CLV. The Brier failure is independent and survived the cleanup.

> Finding contamination and fixing it is not enough. The clean rerun has to pass all gates. This one does not.

## What a genuine signal would require

To restart this experiment honestly, the protocol needs harder gates. Brier improvement over closing as a required gate, not a diagnostic. Sign-stable LOO results before the test set is touched at all. Multi-league or multi-season test data, because one EPL season (380 games) is too small for confirmation at this effect size. At 150 bps, 380 games gives borderline statistical power and cannot separate a real edge from model miscalibration of the same magnitude. That is a different experiment from what this was.

*Research system: HFM · LightGBM · 9 EPL seasons · Walk-forward OOS · Clean features v2*
