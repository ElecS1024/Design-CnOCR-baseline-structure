# Experiment Record

## Record Table

| Date | Model | Dataset | Key Params | Result | Notes |
| --- | --- | --- | --- | --- | --- |
| 2026-03-16 | baseline | sample | rec_model_name=densenet_lite_136-fc | pending | initial project scaffold |
| 2026-03-17 | CnOCR default model | sample (50 images) | onnxruntime backend, default recognizer | line_acc=0.800, char_acc=0.950954, avg_edit_distance=0.36 | baseline inference, evaluation, and case visualization completed |
| 2026-03-17 | CnOCR default model | hard_cases (905 images) | onnxruntime backend, default recognizer | line_acc=0.179006, char_acc=0.324043, avg_edit_distance=2.867403 | grouped evaluation completed on difficult subsets |
| 2026-03-31 | DualModalOCR probe | train(512) / val(128) on server | server=Tesla P100 16GB, torch=2.9.1+cu126, batch_size=8, epochs=1 | train_loss=34.843395, val_line_acc=0.000000, val_char_acc=0.000000 | server-side probe run passed; code, data, and GPU path verified |
| 2026-03-31 | DualModalOCR formal run | train / val on server | server=Tesla P100 16GB, torch=2.9.1+cu126, batch_size=16, epochs=2, max_steps_per_epoch=5000, num_workers=4 | train_loss=3.160761, val_line_acc=0.010665, val_char_acc=0.127606, avg_edit_distance=5.399424 | formal server-side training completed |
| 2026-03-31 | DualModalOCR | hard_cases (905 images) on server | checkpoint=outputs/dual_modal/checkpoints/best.pt | line_acc=0.002210, char_acc=0.019276, avg_edit_distance=4.160221 | grouped hard-cases evaluation completed |
| 2026-03-31 | DualModalOCR v2 | train / val on server | server=Tesla P100 16GB, torch=2.9.1+cu126, batch_size=16, epochs=5, max_steps_per_epoch=8000, num_workers=4 | best_val_line_acc=0.210228, best_val_char_acc=0.560172, best_val_avg_edit_distance=2.722186 | stronger formal server run completed |
| 2026-03-31 | DualModalOCR v2 | hard_cases (905 images) on server | checkpoint=outputs/dual_modal_v2/checkpoints/best.pt | line_acc=0.041989, char_acc=0.160719, avg_edit_distance=3.560221 | grouped hard-cases evaluation completed |
| 2026-03-31 | DualModalOCR v2 | full_test (128610 images) on server | checkpoint=outputs/dual_modal_v2/checkpoints/best.pt | line_acc=0.210054, char_acc=0.557444, avg_edit_distance=2.733979 | grouped full-test evaluation completed |
| 2026-03-31 | SingleModalOCR v1 | train / val on server | server=Tesla P100 16GB, torch=2.9.1+cu126, batch_size=16, epochs=5, max_steps_per_epoch=8000, num_workers=4 | best_val_line_acc=0.397200, best_val_char_acc=0.691481, best_val_avg_edit_distance=1.909486 | ablation control run completed |
| 2026-03-31 | SingleModalOCR v1 | hard_cases (905 images) on server | checkpoint=outputs/single_modal_v1/checkpoints/best.pt | line_acc=0.078453, char_acc=0.200573, avg_edit_distance=3.391160 | grouped hard-cases ablation evaluation completed |
| 2026-03-31 | SingleModalOCR v1 | full_test (128610 images) on server | checkpoint=outputs/single_modal_v1/checkpoints/best.pt | line_acc=0.394052, char_acc=0.688281, avg_edit_distance=1.925706 | grouped full-test ablation evaluation completed |

## Current Baseline Summary

- Environment: `cnocr` conda environment
- Python: 3.10.20
- Backend: onnxruntime
- Device: CPU
- Prediction file: `outputs/preds/baseline_preds.csv`
- Metrics file: `outputs/eval/baseline_metrics.json`
- Visualization output: `outputs/figures/correct_cases` and `outputs/figures/error_cases`

## Follow-up Experiments

- Run baseline on the full `test` split.
- Compare scene, document, web, and hard-case subsets separately.
- Record fine-tuning settings and post-tuning metrics with the same table format.

## Hard Cases Summary

- Dataset size: 905
- Prediction file: `outputs/preds/hard_cases_preds.csv`
- Metrics file: `outputs/eval/hard_cases_metrics.json`
- Group table: `outputs/eval/hard_cases_group_metrics.md`
- Most difficult subsets in current baseline:
  - `vertical_text`: line_acc=0.000000, char_acc=0.002193
  - `oblique_or_curved`: line_acc=0.030000, char_acc=0.078278
  - `bg_confusion`: line_acc=0.115385, char_acc=0.417143

## Dual-Modal Experiment Placeholder

- Experiment target: visual feature + text semantic feature fusion
- Training script: `scripts/09_train_dual_modal.py`
- Prediction script: `scripts/10_predict_dual_modal.py`
- Design note: `docs/dual_modal_module_design.md`
- Pending outputs:
  - `outputs/dual_modal/eval/hard_cases_metrics.json`
  - `outputs/dual_modal/eval/test_metrics.json`
  - `outputs/dual_modal/eval/summary_table.csv` (via existing summary script)

## Server Training Note

- Server IP: `47.112.28.163`
- Login user: `root`
- GPU: `Tesla P100-PCIE-16GB`
- Driver / CUDA: `570.195.03 / 12.8`
- Runtime note:
  - `torch 2.9.1+cu128` is incompatible with `sm_60` on P100
  - server environment switched to `torch 2.9.1+cu126`
- Data sync status:
  - `data/train`, `data/val`, `data/test`, `data/processed/hard_cases_eval` uploaded and extracted on server
- Formal training log:
  - server path: `/root/Design-CnOCR-baseline-structure/outputs/dual_modal/logs/train.log`
- Formal training summary saved locally:
  - `outputs/eval/dual_modal_formal_train_history.csv`
  - `outputs/eval/dual_modal_formal_train_summary.md`
  - `outputs/eval/dual_modal_v2_summary_table.csv`
  - `outputs/eval/dual_modal_v2_group_compare.csv`

## 2026-03-31 Next Optimization Focus

- New plan file: `docs/baseline_dual_modal_optimization_plan.md`
- Primary next step:
  - run a `single_modal` ablation model with the same visual encoder and CTC loop as the current dual-modal experiment
- Why this matters:
  - the current comparison `baseline vs dual_modal` changes too many factors at once
  - adding a single-modal control is necessary to verify whether the second modality itself brings positive gains
- Expected comparison chain:
  - `baseline`
  - `single_modal`
  - `dual_modal_v2`

## 2026-03-31 Ablation Conclusion

- Three-way comparison files:
  - `outputs/eval/ablation_three_way_summary.csv`
  - `outputs/eval/ablation_three_way_summary.md`
  - `outputs/eval/ablation_three_way_group_compare.csv`
  - `outputs/eval/ablation_three_way_group_compare.md`
- Current conclusion:
  - `baseline > single_modal_v1 > dual_modal_v2` on both `hard_cases` and `full_test`
  - the current semantic branch does not yet provide a positive gain over the matched visual-only control
  - the next optimization should focus on redesigning semantic input or hard-case-focused training rather than simply extending training time

## 2026-03-31 Baseline Correction Route Started

- New workflow note:
  - `docs/dual_modal_value_proof_workflow.md`
- New script:
  - `scripts/11_prepare_correction_dataset.py`
- Generated correction-pair datasets:
  - `outputs/correction/hard_cases_correction_pairs.csv`
  - `outputs/correction/full_test_correction_pairs.csv`
  - `outputs/correction/hard_cases_correction_errors_only.csv`
  - `outputs/correction/full_test_correction_errors_only.csv`
- Current data observation:
  - `hard_cases` baseline output has `743 / 905` error samples, error ratio `0.820994`
  - `full_test` baseline output has `59807 / 128610` error samples, error ratio `0.465026`
- Interpretation:
  - the hard-cases subset is highly suitable for the first correction experiment
  - this supports the new route of proving multimodal value through `baseline + semantic correction`
