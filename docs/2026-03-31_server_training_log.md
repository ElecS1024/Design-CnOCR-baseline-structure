# 2026-03-31 Server Training Log

## Goal

Move the dual-modal OCR experiment from the local laptop to a remote GPU server and launch the first formal training run.

## Server Profile

- Public IP: `47.112.28.163`
- Login user: `root`
- OS: `Ubuntu 20.04 64-bit`
- GPU: `Tesla P100-PCIE-16GB`
- Driver: `570.195.03`
- CUDA reported by `nvidia-smi`: `12.8`

## Deployment Summary

1. SSH access was enabled by fixing the security-group rule for `TCP 22`.
2. The private key was moved to `C:\Users\10840\.ssh\CnOCR.pem` and permission-tightened.
3. `git`, `wget`, and `Miniconda` were installed on the server.
4. The project repo was cloned to:
   - `/root/Design-CnOCR-baseline-structure`
5. A `cnocr` conda environment was created on the server.
6. Project dependencies were installed on the server.

## Data Transfer Summary

The formal dataset directories were archived locally and uploaded to the server:

- `train.tar`
- `val.tar`
- `test.tar`
- `hard_cases_eval.tar`

After extraction, the server-side data layout was verified at:

- `/root/Design-CnOCR-baseline-structure/data/train`
- `/root/Design-CnOCR-baseline-structure/data/val`
- `/root/Design-CnOCR-baseline-structure/data/test`
- `/root/Design-CnOCR-baseline-structure/data/processed/hard_cases_eval`

## Compatibility Issue and Fix

The first server attempt failed because:

- `torch 2.9.1+cu128` does not support `sm_60`
- `Tesla P100` is `sm_60`

Observed failure:

- `CUDA error: no kernel image is available for execution on the device`

Fix applied:

- switched the server runtime to `torch 2.9.1+cu126`
- matching packages:
  - `torchvision 0.24.1+cu126`
  - `torchaudio 2.9.1+cu126`

## Probe Run

A small server-side probe run completed successfully:

- Script: `scripts/09_train_dual_modal.py`
- Output dir: `outputs/dual_modal_probe`
- Params:
  - `epochs=1`
  - `batch_size=8`
  - `num_workers=2`
  - `max_train_samples=512`
  - `max_val_samples=128`

Observed training log:

- `epoch=1 step=20 loss=20.833611 avg_loss=83.236599`
- `epoch=1 step=40 loss=10.374497 avg_loss=49.203364`
- `epoch=1 step=60 loss=11.329812 avg_loss=36.485990`
- `epoch=1 train_loss=34.843395 val_line_acc=0.000000 val_char_acc=0.000000`

Conclusion:

- server environment is usable
- data path is correct
- dual-modal code path is correct
- GPU training is functional on the server

## Formal Training Launch

The first formal server-side training run was launched in background mode.

- Script: `scripts/09_train_dual_modal.py`
- Output dir: `outputs/dual_modal`
- Params:
  - `epochs=2`
  - `batch_size=16`
  - `num_workers=4`
  - `max_steps_per_epoch=5000`
  - `log_interval=50`

Main process observed:

- PID: `5844`

Server log target:

- `/root/Design-CnOCR-baseline-structure/outputs/dual_modal/logs/train.log`

## Formal Training Result

The formal server-side run has completed.

Final recorded training summary:

- epoch count: `2`
- final train loss: `3.160761`
- validation total samples: `127704`
- validation exact match samples: `1362`
- validation line accuracy: `0.010665`
- validation character accuracy: `0.127606`
- validation total edit distance: `689528`
- validation average edit distance: `5.399424`

Epoch-level history:

- Epoch 1:
  - train loss: `5.969488`
  - val line accuracy: `0.003093`
  - val character accuracy: `0.023286`
  - val average edit distance: `6.045081`
- Epoch 2:
  - train loss: `3.160761`
  - val line accuracy: `0.010665`
  - val character accuracy: `0.127606`
  - val average edit distance: `5.399424`

Interpretation:

- training loss decreased clearly from epoch 1 to epoch 2
- validation metrics improved in the expected direction
- the dual-modal training path is stable enough to continue with `hard_cases` and `full_test` evaluation

## Next Steps

1. Wait for the formal training run to finish.
2. Pull back or inspect:
   - `best.pt`
   - `last.pt`
   - `best_val_metrics.json`
   - `train_history.json`
3. Run server-side prediction on:
   - `hard_cases`
   - `full_test`
4. Update the local thesis experiment table and comparison tables.
