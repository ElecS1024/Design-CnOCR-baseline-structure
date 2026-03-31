# Dual-Modal Formal Training Summary

## Experiment Setup

- Date: `2026-03-31`
- Training host: remote server
- Server GPU: `Tesla P100-PCIE-16GB`
- Runtime: `torch 2.9.1+cu126`
- Script: `scripts/09_train_dual_modal.py`
- Output dir: `outputs/dual_modal`

## Formal Training Parameters

- `epochs=2`
- `batch_size=16`
- `num_workers=4`
- `max_steps_per_epoch=5000`
- `log_interval=50`

## Validation Result Table

| Epoch | Train Loss | Val Samples | Exact Match | Line Acc | Char Acc | Total Edit Distance | Avg Edit Distance |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 5.969488 | 127704 | 395 | 0.003093 | 0.023286 | 771981 | 6.045081 |
| 2 | 3.160761 | 127704 | 1362 | 0.010665 | 0.127606 | 689528 | 5.399424 |

## Thesis-Oriented Summary

This formal dual-modal training run completed successfully on the remote GPU server. Compared with epoch 1, epoch 2 showed a clear reduction in training loss and an increase in validation line accuracy and character accuracy. The average edit distance also decreased from `6.045081` to `5.399424`, which indicates that the model predictions moved closer to the ground-truth text after continued training.

Although the absolute validation accuracy remains low at the current training scale, the experiment confirms that the dual-modal training path is stable and produces measurable improvement across epochs. Therefore, the resulting checkpoint can be used for the next-stage evaluation on `hard_cases` and `full_test`.
