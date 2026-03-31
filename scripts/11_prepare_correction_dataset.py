from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


def edit_distance(a: str, b: str) -> int:
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)

    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        curr = [i]
        for j, cb in enumerate(b, start=1):
            cost = 0 if ca == cb else 1
            curr.append(
                min(
                    prev[j] + 1,
                    curr[j - 1] + 1,
                    prev[j - 1] + cost,
                )
            )
        prev = curr
    return prev[-1]


def infer_group(filename: str) -> str:
    if filename.startswith("document_"):
        return "document"
    if filename.startswith("scene_"):
        return "scene"
    if filename.startswith("web_"):
        return "web"
    if filename.startswith("bg_confusion_"):
        return "bg_confusion"
    if filename.startswith("blur_"):
        return "blur"
    if filename.startswith("oblique_or_curved_"):
        return "oblique_or_curved"
    if filename.startswith("occlusion_"):
        return "occlusion"
    if filename.startswith("vertical_text_"):
        return "vertical_text"
    return "unknown"


def summarize(rows: list[dict[str, object]]) -> dict[str, object]:
    total = len(rows)
    errors = sum(int(row["needs_correction"]) for row in rows)
    avg_edit_distance = sum(int(row["edit_distance"]) for row in rows) / total if total else 0.0
    group_counter = Counter(str(row["group"]) for row in rows)
    error_group_counter = Counter(str(row["group"]) for row in rows if int(row["needs_correction"]))
    return {
        "total_samples": total,
        "error_samples": errors,
        "error_ratio": round(errors / total, 6) if total else 0.0,
        "avg_edit_distance": round(avg_edit_distance, 6),
        "group_counts": dict(sorted(group_counter.items())),
        "error_group_counts": dict(sorted(error_group_counter.items())),
    }


def write_markdown_summary(path: Path, summary: dict[str, object], dataset_name: str) -> None:
    lines = [
        f"# Correction Dataset Summary: {dataset_name}",
        "",
        f"- total_samples: `{summary['total_samples']}`",
        f"- error_samples: `{summary['error_samples']}`",
        f"- error_ratio: `{summary['error_ratio']}`",
        f"- avg_edit_distance: `{summary['avg_edit_distance']}`",
        "",
        "## Group Counts",
        "",
        "| Group | Samples | Error Samples |",
        "| --- | ---: | ---: |",
    ]
    group_counts = summary["group_counts"]
    error_group_counts = summary["error_group_counts"]
    for group, count in group_counts.items():
        lines.append(f"| {group} | {count} | {error_group_counts.get(group, 0)} |")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert baseline prediction CSV into correction-pair datasets."
    )
    root = Path(__file__).resolve().parents[1]
    parser.add_argument("--pred-file", required=True)
    parser.add_argument("--output-csv", required=True)
    parser.add_argument("--output-json", default="")
    parser.add_argument("--output-md", default="")
    parser.add_argument("--dataset-name", default="correction_dataset")
    parser.add_argument("--error-only", action="store_true")
    parser.add_argument("--min-edit-distance", type=int, default=0)
    args = parser.parse_args()

    pred_file = Path(args.pred_file)
    output_csv = Path(args.output_csv)
    output_json = Path(args.output_json) if args.output_json else output_csv.with_suffix(".json")
    output_md = Path(args.output_md) if args.output_md else output_csv.with_suffix(".md")

    rows: list[dict[str, object]] = []
    with pred_file.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            gt_text = row["gt_text"]
            pred_text = row["pred_text"]
            dist = edit_distance(pred_text, gt_text)
            needs_correction = int(pred_text != gt_text)
            if args.error_only and not needs_correction:
                continue
            if dist < args.min_edit_distance:
                continue
            filename = row["filename"]
            rows.append(
                {
                    "filename": filename,
                    "group": infer_group(filename),
                    "baseline_text": pred_text,
                    "target_text": gt_text,
                    "needs_correction": needs_correction,
                    "edit_distance": dist,
                    "baseline_score": row.get("score", ""),
                }
            )

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "filename",
                "group",
                "baseline_text",
                "target_text",
                "needs_correction",
                "edit_distance",
                "baseline_score",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    summary = summarize(rows)
    output_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown_summary(output_md, summary, args.dataset_name)

    print(f"prepared correction pairs: {len(rows)}")
    print(f"saved: {output_csv}")
    print(f"saved: {output_json}")
    print(f"saved: {output_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
