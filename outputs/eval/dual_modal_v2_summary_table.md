# Baseline vs Dual-Modal V2 Summary

| Dataset | Samples | Exact Match | Line Acc | Char Acc | Total Edit Distance | Avg Edit Distance |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| hard_cases baseline | 905 | 162 | 0.179006 | 0.324043 | 2595 | 2.867403 |
| hard_cases dual_modal_v2 | 905 | 38 | 0.041989 | 0.160719 | 3222 | 3.560221 |
| full_test baseline | 128610 | 68803 | 0.534974 | 0.762601 | 188617 | 1.466581 |
| full_test dual_modal_v2 | 128610 | 27015 | 0.210054 | 0.557444 | 351617 | 2.733979 |

## Quick Reading

- The current `dual_modal_v2` model is significantly better than the earlier short dual-modal run, but it is still below the baseline on both `hard_cases` and `full_test`.
- On `hard_cases`, `dual_modal_v2` reaches `line_acc=0.041989`, which is higher than the earlier dual-modal checkpoint, but still lower than the baseline `0.179006`.
- On `full_test`, `dual_modal_v2` reaches `line_acc=0.210054`, while the baseline remains `0.534974`.
- Therefore, the current `dual_modal_v2` experiment should be described as a stable and improved dual-modal training result relative to earlier dual-modal attempts, but not yet as a final model that surpasses the baseline.
