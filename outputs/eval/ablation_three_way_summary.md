# Baseline vs Single-Modal vs Dual-Modal Summary

| Dataset | Model | Samples | Exact Match | Line Acc | Char Acc | Avg Edit Distance |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| hard_cases | baseline | 905 | 162 | 0.179006 | 0.324043 | 2.867403 |
| hard_cases | single_modal_v1 | 905 | 71 | 0.078453 | 0.200573 | 3.391160 |
| hard_cases | dual_modal_v2 | 905 | 38 | 0.041989 | 0.160719 | 3.560221 |
| full_test | baseline | 128610 | 68803 | 0.534974 | 0.762601 | 1.466581 |
| full_test | single_modal_v1 | 128610 | 50679 | 0.394052 | 0.688281 | 1.925706 |
| full_test | dual_modal_v2 | 128610 | 27015 | 0.210054 | 0.557444 | 2.733979 |