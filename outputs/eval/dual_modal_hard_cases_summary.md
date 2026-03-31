# Dual-Modal Hard Cases Summary

## Overall Result

| Dataset | Samples | Exact Match | Line Acc | Char Acc | Total Edit Distance | Avg Edit Distance |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| hard_cases | 905 | 2 | 0.002210 | 0.019276 | 3765 | 4.160221 |

## Grouped Result

| Group | Samples | Exact Match | Line Acc | Char Acc | Total Edit Distance | Avg Edit Distance |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| overall | 905 | 2 | 0.002210 | 0.019276 | 3765 | 4.160221 |
| hard_cases | 905 | 2 | 0.002210 | 0.019276 | 3765 | 4.160221 |
| bg_confusion | 104 | 0 | 0.000000 | 0.024000 | 854 | 8.211538 |
| blur | 500 | 2 | 0.004000 | 0.012491 | 1423 | 2.846000 |
| oblique_or_curved | 100 | 0 | 0.000000 | 0.017613 | 502 | 5.020000 |
| occlusion | 101 | 0 | 0.000000 | 0.044964 | 531 | 5.257426 |
| vertical_text | 100 | 0 | 0.000000 | 0.002193 | 455 | 4.550000 |

## Thesis-Oriented Note

This hard-cases evaluation shows that the current dual-modal checkpoint is still not competitive with the existing baseline on difficult samples. Therefore, the present model should be described as an early formal training result, not yet as the final improved model. The main value of this experiment is that it verifies the complete remote training and evaluation workflow, and it provides a concrete starting point for further tuning.
