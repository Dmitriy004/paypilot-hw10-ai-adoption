# Assistant Adoption Impact Report — reusable template

This is an empty measurement template, not a completed experiment. Separate measured facts, estimates and unknowns. Do not include confidential examples from an employer.

## Forecast before work

| Measure | Prediction recorded before execution | Actual | Explanation |
| --- | --- | --- | --- |
| Defects detected by independent baseline | To record | To measure | To explain |
| Defects detected by generated suite | To record | To measure | To explain |
| Weakest category in each suite | To record | To measure | To explain |

## 1. Independent baseline

Record target component/version, requirements source, authoring method, function and collected-case counts, start/end/time zone, actual elapsed minutes and immutable baseline revision. If independence or timing was not achieved, state that explicitly; do not substitute assumed minutes.

| Case ID | Rule | Input class | Independent expected result | Evidence |
| --- | --- | --- | --- | --- |
| To fill | To fill | To fill | To fill | To fill |

## 2. Frozen defect set

Record each deliberate single change, category, behavioral consequence and a witness input distinguishing it from the original. Freeze the final list before generating the comparator and before execution. Record revision and content hash; preserve equivalent changes without silently replacing them.

## 3. Review criteria and generation input

Freeze criteria for expected-result independence, assertion strength, claimed boundaries, test isolation, meaningful names and novelty. Explain how exception/property tests are evaluated. Save the exact input, permitted context, model/version/settings, tool permissions, forecast revision and timestamp before generation.

## 4. Generation and execution coverage

Preserve the first raw response with request ID, timestamps, usage, machine duration and separately labelled cost estimate or reconciled charge. Record original and retained function counts. Preserve original failing tests before removing them in an independent revision. Compare execution coverage using the same interpreter and configuration.

## 5. Review log

| Function ID | Accept/reject | Criterion | Reason | Action | Review minutes | Rewrite minutes |
| --- | --- | --- | --- | --- | --- | --- |
| To fill | To fill | To fill | To fill | To fill | Actual or unknown | Actual or unknown |

Every generated function gets a row. Keep useful replacements separate from the frozen comparator. Summarize accepted/rejected/rewritten counts with denominators and explain any later correction without erasing history.

## 6. Detection by category

| Defect category | Baseline detected/total | Generated detected/total | Combined detected/total |
| --- | --- | --- | --- |
| To fill | To measure | To measure | To measure |
| Total | To measure | To measure | To measure |

List survivors by ID, distinguish assertion failures from infrastructure errors, compare forecasts and identify marginal benefit. Do not generalize a deliberately selected defect list into a production failure probability.

## 7. Price in two currencies

| Resource | Baseline | Generated workflow | Provenance |
| --- | --- | --- | --- |
| Human authoring minutes | Actual/unknown | Actual/unknown | Timer |
| Human review/selection minutes | Actual/unknown | Actual/unknown | Review log |
| Human rewriting minutes | Actual/unknown | Actual/unknown | Review log |
| Total human minutes | Sum only measured inputs | Sum only measured inputs | Do not turn estimates into measurements |
| Machine generation minutes | Actual/none | Actual/none | Raw metadata |
| Generation cost | Actual estimate/charge/none | Actual estimate/charge/none | Usage, rates, reconciliation status |

Keep human and machine resources separate. Include review and rewrites before claiming a time saving; do not infer human speed from automation latency.

## 8. Seven-row decision

| Row | Required decision content |
| --- | --- |
| 1. Scope | Component, versions, frozen set, actual context and configuration |
| 2. Number | Detection with category breakdown, denominators and rejection share |
| 3. Failure classes | Which category each suite misses and resulting business harm |
| 4. Price | Actual human effort plus separate machine time/money and unknowns |
| 5. Division of work | What the assistant drafts, what an independent reviewer supplies and who accepts changes |
| 6. Mandate | Concrete actions under delivery-first versus stricter risk constraints |
| 7. Revisit | At least two events that trigger a new decision and experiment |

## 9. Residual risk

| Not covered | Consequence | Why tolerated for now | Defer or accept |
| --- | --- | --- | --- |
| To fill | To fill | To fill | To fill |

## 10. Declaration and reproducibility

Declare where an assistant was used and what output was rejected. Record clean checkout revision, dependency installation, exact verification commands/results and public evidence locations. Keep secrets out of tracked files. A runnable package is not proof that missing authorship/timing criteria were met.
