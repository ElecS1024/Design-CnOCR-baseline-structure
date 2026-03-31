# Dual-Modal Value Proof Workflow

## Core Goal

The next stage should no longer aim first at fully surpassing the pretrained baseline on the whole test set.

The more defensible thesis goal is:

1. prove that a second modality can provide measurable value under a controlled setup
2. prove that the value is most likely to appear on difficult samples
3. only then discuss whether the improved pipeline can approach or surpass the original baseline

## Why the Main Goal Changes

The current three-way comparison already shows:

- `baseline > single_modal_v1 > dual_modal_v2`

This means the current semantic branch and fusion design have not yet created a positive gain over the matched visual-only control.

Therefore, the most important next experiment is not another blind long training run, but a more targeted setup that gives the second modality a fairer role.

## New Working Route

### Route A. Baseline Output + Semantic Correction

This route treats the pretrained baseline as the primary recognizer and lets the second modality work as a correction module.

The workflow is:

1. run baseline recognition
2. collect `(baseline_text, target_text)` correction pairs
3. train a correction or reranking module
4. evaluate whether the corrected output improves over the raw baseline output

This route is the best fit for proving that the second modality has practical value.

### Route B. Hard-Cases-Focused Refinement

This route keeps the current dual-modal design but gives difficult samples more importance.

Typical moves include:

- hard-case oversampling
- higher sampling weight for `vertical_text`, `oblique_or_curved`, and `occlusion`
- reducing the mismatch between training-time semantic input and inference-time semantic input

This route is easier to implement but less likely than Route A to exceed the current baseline.

## Recommended Execution Order

1. Prepare correction datasets from existing baseline predictions.
2. Build a baseline-correction experiment on `hard_cases` first.
3. If it shows local gains, expand to the larger `full_test` set.
4. Keep the ablation structure:
   - raw `baseline`
   - `baseline + correction`
   - existing `single_modal_v1`
   - existing `dual_modal_v2`

## Immediate Deliverables

- [x] Three-way ablation result: `baseline` vs `single_modal_v1` vs `dual_modal_v2`
- [x] New workflow defined around proving multimodal value
- [x] Correction dataset preparation script
- [x] Hard-cases correction pairs generated
- [x] Full-test correction pairs generated
- [x] Error-only correction subsets generated for both `hard_cases` and `full_test`
- [ ] First correction experiment launched

## Thesis Writing Guidance

The thesis can frame the next section as:

- the original dual-modal fusion path was implemented and evaluated
- ablation showed that the current semantic branch did not yet outperform the matched visual-only control
- therefore a second experimental path was introduced, where the second modality serves as a semantic correction mechanism on top of the baseline output

This framing remains faithful to the original proposal while making the argument more rigorous.
