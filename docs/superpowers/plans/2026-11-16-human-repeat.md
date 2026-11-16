# Human Repeat Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans; bounded inline execution continues the user-approved repeat.

**Goal:** Зберегти першу нову генерацію після авторського baseline і передати її для самостійного timed review.
**Architecture:** Optional adapter output directory; existing payload/budget/no-retry guards; immutable earlier experiment.
**Tech Stack:** Python3.12/pytest9.2, urllib Responses API.
**Spec:** docs/superpowers/specs/2026-11-16-human-repeat-design.md

## Global Constraints

One paid attempt≤$0.05; existing$0.03 upper-bound guard unchanged. Historical source snapshots/reports remain preserved; app/prompts/mutants unchanged. User baseline and raw generation unchanged apart from Git EOL normalization at promotion. No assistant review verdicts before user review. Publication/submission only after verification and under existing user authorization.

## Review Focus

- New output path must not overwrite historical generation: actual main offline test preserves sentinel.
- Default path backward compatible: same test with omitted optional flag.
- Duplicate output still fails before sending: existing reserve_output guard test remains.
- Forecast must precede call and new mutation runs: explicit commit chronology and metadata source_commit.
- Human timer/authoring must not migrate into historical comparator: stage status/provenance references exact new baseline.

### Task 1: Isolated output and forecast

**Files:** tools/generate_openai.py; tests/infrastructure/test_generate_openai.py; experiments/human-repeat/forecast.md; experiments/human-repeat/timing.json.
**Interfaces:** main reads optional --output-dir Path, default ROOT/reports/openai-generation; same artifact schema and reserved exclusive directory.
- [ ] Add real-main offline test with fake external HTTP response/revision lookup, default and explicit output, historical sentinel preserved. Observe missing optional flag RED.
- [ ] Minimal argparse/output change; full suite GREEN and user baseline15PASS. Commit explicit source/test/config/spec/plan files.
- [ ] Forecast exact IDs on frozen12; separate commit before request or new mutation runs. Record no pauses from author, no fabricated clocks.

### Task 2: One request and author review handoff

**Files:** experiments/human-repeat/generation/{request.json,response.json,metadata.json,extracted.py}; review-log.md and README.md under experiments/human-repeat; aiq-final references only.
**Interfaces:** successful first response → raw function list and blank author review rows, not assistant verdicts; metadata exact usage/time/status/hash.
- [ ] Verify current model/pricing, conservative cap<user limit, source public hash, no uncommitted protected changes; make one request with explicit separate output.
- [ ] Preserve raw first response and extracted bytes; commit before running generated tests, do not improve/remove functions.
- [ ] Prepare numbered blank review worksheet; open it and raw source in IDE, let author explicitly start timed review and report per-function time/rewrites.
- [ ] Update/stage final-project LRA7/EvidenceMap/README partial progress with exact local commits; no claims of finished full experiment.
- [ ] Whole-range fresh read-only review when implementation stage ends; full offline suite and frozen user SHA remain green; hand off author participation.

### Task 3: Approved promotion and paired measurements

User explicitly authorized switching tests/manual, tests/generated and tests/rewritten to the saved repeat after the safety block; historical commits/reports remain available. Review amendments are frozen at24d88b3. This extends the earlier handoff plan, not its original constraints retroactively.

- [ ] Promote saved suites unchanged and package the already recorded new response in reports/generation.json; no new paid call. Verify Git-normalized equality, full suite and summary, then freeze a technical commit before mutation runs.
- [ ] Run unchanged runner on manual/generated/all against the same frozen12 list; keep new timestamped reports distinct. Measure coverage into reports/human-repeat, verify every kill is assertion-based and audit forecasts without editing them.
- [ ] Update ten-section impact report, full review journal, readiness and reproducibility docs with actual metrics, all human workflow overhead, limitations and historical scope. Preserve raw green rejected tests; rewritten stays outside comparators.
- [ ] Freeze deliverables, clone that exact revision into a separate temporary directory, install/check pinned requirements and run the required offline cascade. Record proof without inventing remote publication.
- [ ] One fresh-context whole-range read-only review; address important findings with verification. Update/stage aiq-final LRA7/EvidenceMap/README exact evidence; no LRA7 completion without L14.
