# Baseline vs Dual-Modal V2 Group Comparison

| Group | Samples | Baseline Line Acc | Dual-Modal V2 Line Acc | Baseline Char Acc | Dual-Modal V2 Char Acc | Baseline Avg Edit Distance | Dual-Modal V2 Avg Edit Distance |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| scene | 63646 | 0.381297 | 0.122977 | 0.577446 | 0.354851 | 2.129608 | 3.251453 |
| document | 50000 | 0.776540 | 0.323320 | 0.954818 | 0.742042 | 0.360800 | 2.059920 |
| web | 14059 | 0.394480 | 0.212248 | 0.540723 | 0.455553 | 2.307490 | 2.735401 |
| hard_cases | 905 | 0.179006 | 0.041989 | 0.324043 | 0.160719 | 2.867403 | 3.560221 |
| bg_confusion | 104 | 0.115385 | 0.009615 | 0.417143 | 0.186286 | 4.903846 | 6.846154 |
| blur | 500 | 0.270000 | 0.062000 | 0.414990 | 0.172103 | 1.686000 | 2.386000 |
| oblique_or_curved | 100 | 0.030000 | 0.010000 | 0.078278 | 0.076321 | 4.710000 | 4.720000 |
| occlusion | 101 | 0.118812 | 0.049505 | 0.431655 | 0.291367 | 3.128713 | 3.900990 |
| vertical_text | 100 | 0.000000 | 0.000000 | 0.002193 | 0.010965 | 4.550000 | 4.510000 |

## Key Notes

- `dual_modal_v2` is still below the baseline across the major top-level groups: `scene`, `document`, `web`, and `hard_cases`.
- The current model shows its most interesting relative behavior on `vertical_text`, where line accuracy stays at `0`, but character accuracy and average edit distance are slightly better than the baseline.
- On `oblique_or_curved`, the dual-modal result is close to the baseline in character accuracy, but still weaker in line accuracy.
- For thesis writing, this table is useful for supporting an honest conclusion: the current dual-modal design and training pipeline are valid, but the present checkpoint has not yet surpassed the baseline.
