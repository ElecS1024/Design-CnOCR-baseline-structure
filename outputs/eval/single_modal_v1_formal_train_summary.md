# Single-Modal V1 Formal Training Summary

- Model tag: `single_modal_v1`
- Training setting: `epochs=5`, `batch_size=16`, `max_steps_per_epoch=8000`, `num_workers=4`
- Purpose: ablation control for the current dual-modal architecture

## Best Validation Result

- `line_acc=0.397200`
- `char_acc=0.691481`
- `avg_edit_distance=1.909486`

## Hard Cases Result

- `line_acc=0.078453`
- `char_acc=0.200573`
- `avg_edit_distance=3.391160`

## Full Test Result

- `line_acc=0.394052`
- `char_acc=0.688281`
- `avg_edit_distance=1.925706`

## Key Observation

- `single_modal_v1` is clearly stronger than the current `dual_modal_v2` on both `hard_cases` and `full_test`.
- However, it is still below the pretrained baseline on the same evaluation sets.
- This means the current semantic branch has not yet produced a positive gain over the matched visual-only control.