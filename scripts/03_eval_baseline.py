import argparse
import csv
import json
from pathlib import Path


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


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate CnOCR baseline predictions.")
    root = Path(__file__).resolve().parents[1]
    parser.add_argument("--pred-file", default=str(root / "outputs" / "preds" / "baseline_preds.csv"))
    parser.add_argument("--output-file", default=str(root / "outputs" / "eval" / "baseline_metrics.json"))
    args = parser.parse_args()

    pred_file = Path(args.pred_file)
    output_file = Path(args.output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with pred_file.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    total_samples = len(rows)
    exact_matches = sum(int(row.get("exact_match", "0")) for row in rows)
    total_gt_chars = 0
    total_edit_distance = 0

    for row in rows:
        gt_text = row.get("gt_text", "")
        pred_text = row.get("pred_text", "")
        total_gt_chars += len(gt_text)
        total_edit_distance += levenshtein(gt_text, pred_text)

    line_accuracy = exact_matches / total_samples if total_samples else 0.0
    char_accuracy = (
        (total_gt_chars - total_edit_distance) / total_gt_chars if total_gt_chars else 0.0
    )
    metrics = {
        "total_samples": total_samples,
        "exact_match_samples": exact_matches,
        "line_accuracy": round(line_accuracy, 6),
        "character_accuracy": round(max(char_accuracy, 0.0), 6),
        "total_edit_distance": total_edit_distance,
        "average_edit_distance": round(total_edit_distance / total_samples, 6) if total_samples else 0.0,
    }

    output_file.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(metrics, ensure_ascii=False, indent=2))
    print(f"metrics saved to: {output_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
