# Experiment Record

## Record Table

| Date | Model | Dataset | Key Params | Result | Notes |
| --- | --- | --- | --- | --- | --- |
| 2026-03-16 | baseline | sample | rec_model_name=densenet_lite_136-fc | pending | initial project scaffold |
| 2026-03-17 | CnOCR default model | sample (50 images) | onnxruntime backend, default recognizer | line_acc=0.800, char_acc=0.950954, avg_edit_distance=0.36 | baseline inference, evaluation, and case visualization completed |
| 2026-03-17 | CnOCR default model | hard_cases (905 images) | onnxruntime backend, default recognizer | line_acc=0.179006, char_acc=0.324043, avg_edit_distance=2.867403 | grouped evaluation completed on difficult subsets |

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
