# Baseline + Dual-Modal Optimization Plan

## Goal

Before the thesis enters full writing, complete a defensible experimental chain around the hypothesis that adding a dual-modal module after the baseline can improve recognition quality, especially on difficult samples.

## Target Questions

1. Can the dual-modal module improve over a visual-only model built with the same training framework?
2. Can the improved pipeline outperform the current CnOCR baseline on `hard_cases` or on selected difficult subgroups?
3. If it does not outperform the baseline overall, can we still show that the second modality provides positive gains under controlled ablation?

## Execution Checklist

### Stage 1. Build a clean ablation path

- [x] Keep the current baseline results unchanged as the main reference group.
- [x] Keep the current dual-modal implementation as the multimodal experiment group.
- [x] Add a single-modal control path with the same visual encoder and CTC training loop, but without the semantic branch or fusion module.
- [ ] Run the single-modal probe on server to verify training and prediction.
- [ ] Run the single-modal formal experiment on server.

### Stage 2. Complete ablation comparison

- [ ] Evaluate single-modal on `hard_cases`.
- [ ] Evaluate single-modal on `full_test`.
- [ ] Generate grouped comparison tables for `baseline`, `single_modal`, and `dual_modal`.
- [ ] Focus comparison on `hard_cases`, `vertical_text`, `oblique_or_curved`, and `occlusion`.

### Stage 3. Optimize for a realistic win condition

- [ ] Prefer proving `single_modal < dual_modal` first.
- [ ] Then try to improve `hard_cases` rather than aiming for a full-test win immediately.
- [ ] If needed, add hard-case reweighting or oversampling in training.
- [ ] If needed, reduce the training/inference gap caused by teacher forcing in the semantic branch.

### Stage 4. Prepare thesis-ready materials

- [ ] Export overall metrics tables for `baseline`, `single_modal`, and `dual_modal`.
- [ ] Export grouped metrics tables for major subsets and hard-case subsets.
- [ ] Summarize whether the second modality brings positive gains.
- [ ] Update Chapter 3 and Chapter 4 notes for the module design and implementation.
- [ ] Update Chapter 5 notes for ablation and comparison analysis.

## Recommended Near-Term Order

1. Run the single-modal probe.
2. Run the single-modal formal training.
3. Evaluate single-modal on `hard_cases`.
4. Evaluate single-modal on `full_test`.
5. Build a three-way comparison table: `baseline` vs `single_modal` vs `dual_modal_v2`.
6. Decide whether to spend more time on hard-case-focused optimization.

## Current Working Conclusion

- The current `dual_modal_v2` training is technically stable and clearly stronger than earlier short dual-modal runs.
- However, it is still below the current CnOCR baseline on both `hard_cases` and `full_test`.
- Therefore, the most important next experiment is not another blind long run, but a controlled ablation with a single-modal model.
- If the single-modal model is weaker than the dual-modal model, that will support the claim that the semantic branch has positive value, even if the overall system has not yet surpassed the pretrained baseline.
