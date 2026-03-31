# Correction Model V1 Summary

## Training Artifact Snapshot

- artifact directory: `artifacts/correction_model_v1`
- included files:
  - `best.pt`
  - `last.pt`
  - `vocab.json`
  - `train.log`
  - `train_history.json`
  - `best_val_metrics.json`
  - `hard_cases_preds.csv`
  - `hard_cases_metrics.json`
  - `hard_cases_group_metrics.csv`
  - `hard_cases_group_metrics.md`
  - `val_preds.csv`

## Validation Result

- correction validation set: `hard_cases_correction_errors_only`
- `line_acc=0.020188`

## Hard Cases Result

- `line_acc=0.041989`
- `char_acc=0.000000`
- `avg_edit_distance=4.741436`

## Comparison Note

- the first correction-model attempt has completed end-to-end
- however, it does not yet improve over the raw baseline on `hard_cases`
- this means the correction route is technically feasible, but the current seq2seq design still needs stronger modeling or better training strategy
