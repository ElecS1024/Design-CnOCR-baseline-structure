import argparse
import csv
import json
from collections import defaultdict
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


def infer_groups(filename: str) -> list[str]:
    groups = []
    if filename.startswith("scene_"):
        groups.append("scene")
    elif filename.startswith("document_"):
        groups.append("document")
    elif filename.startswith("web_"):
        groups.append("web")
    elif filename.startswith("bg_confusion_"):
        groups.extend(["hard_cases", "bg_confusion"])
    elif filename.startswith("blur_"):
        groups.extend(["hard_cases", "blur"])
    elif filename.startswith("oblique_or_curved_"):
        groups.extend(["hard_cases", "oblique_or_curved"])
    elif filename.startswith("occlusion_"):
        groups.extend(["hard_cases", "occlusion"])
    elif filename.startswith("vertical_text_"):
        groups.extend(["hard_cases", "vertical_text"])
    else:
        groups.append("other")
    groups.append("overall")
    return groups


def compute_metrics(rows: list[dict[str, str]]) -> dict[str, float | int]:
    total = len(rows)
    exact = 0
    total_gt_chars = 0
    total_edit_distance = 0
    for row in rows:
        gt_text = row.get("gt_text", "")
        pred_text = row.get("pred_text", "")
        exact += int(str(row.get("exact_match", "0")) == "1")
        total_gt_chars += len(gt_text)
        total_edit_distance += levenshtein(gt_text, pred_text)

    line_accuracy = exact / total if total else 0.0
    char_accuracy = (
        (total_gt_chars - total_edit_distance) / total_gt_chars if total_gt_chars else 0.0
    )
    return {
        "samples": total,
        "exact_match_samples": exact,
        "line_accuracy": round(line_accuracy, 6),
        "character_accuracy": round(max(char_accuracy, 0.0), 6),
        "total_edit_distance": total_edit_distance,
        "average_edit_distance": round(total_edit_distance / total, 6) if total else 0.0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate OCR predictions by dataset group.")
    root = Path(__file__).resolve().parents[1]
    parser.add_argument("--pred-file", default=str(root / "outputs" / "preds" / "baseline_preds.csv"))
    parser.add_argument(
        "--output-csv",
        default=str(root / "outputs" / "eval" / "group_metrics.csv"),
    )
    parser.add_argument(
        "--output-json",
        default=str(root / "outputs" / "eval" / "group_metrics.json"),
    )
    parser.add_argument(
        "--output-md",
        default=str(root / "outputs" / "eval" / "group_metrics.md"),
    )
    args = parser.parse_args()

    pred_file = Path(args.pred_file)
    output_csv = Path(args.output_csv)
    output_json = Path(args.output_json)
    output_md = Path(args.output_md)
    output_csv.parent.mkdir(parents=True, exist_ok=True)

    with pred_file.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        for group in infer_groups(row["filename"]):
            grouped[group].append(row)

    order = [
        "overall",
        "scene",
        "document",
        "web",
        "hard_cases",
        "bg_confusion",
        "blur",
        "oblique_or_curved",
        "occlusion",
        "vertical_text",
        "other",
    ]

    result_rows = []
    result_json = {}
    for group in order:
        if group not in grouped:
            continue
        metrics = compute_metrics(grouped[group])
        result_json[group] = metrics
        result_rows.append({"group": group, **metrics})

    with output_csv.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "group",
                "samples",
                "exact_match_samples",
                "line_accuracy",
                "character_accuracy",
                "total_edit_distance",
                "average_edit_distance",
            ],
        )
        writer.writeheader()
        writer.writerows(result_rows)

    output_json.write_text(json.dumps(result_json, ensure_ascii=False, indent=2), encoding="utf-8")

    md_lines = [
        "| Group | Samples | Exact Match | Line Acc | Char Acc | Total Edit Distance | Avg Edit Distance |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in result_rows:
        md_lines.append(
            f"| {row['group']} | {row['samples']} | {row['exact_match_samples']} | "
            f"{row['line_accuracy']:.6f} | {row['character_accuracy']:.6f} | "
            f"{row['total_edit_distance']} | {row['average_edit_distance']:.6f} |"
        )
    output_md.write_text("\n".join(md_lines), encoding="utf-8")

    print("\n".join(md_lines))
    print(f"saved: {output_csv}")
    print(f"saved: {output_json}")
    print(f"saved: {output_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
