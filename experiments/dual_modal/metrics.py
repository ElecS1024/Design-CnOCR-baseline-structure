from __future__ import annotations


def levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)

    prev = list(range(len(b) + 1))
    for i, ch_a in enumerate(a, start=1):
        curr = [i]
        for j, ch_b in enumerate(b, start=1):
            cost = 0 if ch_a == ch_b else 1
            curr.append(min(curr[-1] + 1, prev[j] + 1, prev[j - 1] + cost))
        prev = curr
    return prev[-1]


def compute_metrics(rows: list[dict[str, str]]) -> dict[str, float | int]:
    total_samples = len(rows)
    exact_match_samples = 0
    total_gt_chars = 0
    total_edit_distance = 0

    for row in rows:
        gt_text = row.get("gt_text", "")
        pred_text = row.get("pred_text", "")
        exact_match_samples += int(gt_text == pred_text)
        total_gt_chars += len(gt_text)
        total_edit_distance += levenshtein(gt_text, pred_text)

    line_accuracy = exact_match_samples / total_samples if total_samples else 0.0
    char_accuracy = (
        (total_gt_chars - total_edit_distance) / total_gt_chars if total_gt_chars else 0.0
    )
    return {
        "total_samples": total_samples,
        "exact_match_samples": exact_match_samples,
        "line_accuracy": round(line_accuracy, 6),
        "character_accuracy": round(max(char_accuracy, 0.0), 6),
        "total_edit_distance": total_edit_distance,
        "average_edit_distance": round(total_edit_distance / total_samples, 6) if total_samples else 0.0,
    }

