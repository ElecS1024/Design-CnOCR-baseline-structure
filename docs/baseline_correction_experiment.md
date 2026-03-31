# Baseline Correction Experiment

## Purpose

This experiment route is designed to prove multimodal value in a more defensible way.

Instead of replacing the pretrained OCR baseline, the new model tries to correct or rerank the baseline output.

## Core Idea

1. run the strong pretrained baseline first
2. use the baseline prediction as the first-stage input
3. train a correction model to map `baseline_text -> target_text`
4. compare the corrected result with the original baseline output

## Current Skeleton

### Data

- correction-pair preparation script:
  - `scripts/11_prepare_correction_dataset.py`
- prepared datasets:
  - `outputs/correction/hard_cases_correction_pairs.csv`
  - `outputs/correction/full_test_correction_pairs.csv`
  - `outputs/correction/hard_cases_correction_errors_only.csv`
  - `outputs/correction/full_test_correction_errors_only.csv`

### Model

- tokenizer:
  - `experiments/correction/tokenizer.py`
- dataset:
  - `experiments/correction/data.py`
- seq2seq correction model:
  - `models/correction_model.py`

### Scripts

- training:
  - `scripts/12_train_correction_model.py`
- prediction:
  - `scripts/13_predict_correction_model.py`

## Recommended First Run

Train on correction pairs and validate on hard cases:

```powershell
C:\Users\10840\.conda\envs\cnocr\python.exe scripts\12_train_correction_model.py --epochs 3 --batch-size 64 --train-csv outputs\correction\full_test_correction_errors_only.csv --val-csv outputs\correction\hard_cases_correction_errors_only.csv --output-dir outputs\correction_model_v1
```

Then predict on the hard-cases correction set:

```powershell
C:\Users\10840\.conda\envs\cnocr\python.exe scripts\13_predict_correction_model.py --input-csv outputs\correction\hard_cases_correction_pairs.csv --checkpoint outputs\correction_model_v1\checkpoints\best.pt --vocab-file outputs\correction_model_v1\vocab.json --output-file outputs\correction_model_v1\preds\hard_cases_preds.csv
```

Finally reuse the existing evaluator:

```powershell
C:\Users\10840\.conda\envs\cnocr\python.exe scripts\03_eval_baseline.py --pred-file outputs\correction_model_v1\preds\hard_cases_preds.csv --output-file outputs\correction_model_v1\eval\hard_cases_metrics.json
```

## Success Criterion

The first practical success target is:

- corrected hard-cases result better than raw baseline hard-cases result on at least one meaningful metric or subgroup

This is a better fit for proving multimodal value than requiring the correction route to outperform every existing model on the full test set.
