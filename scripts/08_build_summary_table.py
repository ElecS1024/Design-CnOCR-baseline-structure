import argparse
import csv
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a comparison table from evaluation metric files.")
    root = Path(__file__).resolve().parents[1]
    parser.add_argument(
        "--output-csv",
        default=str(root / "outputs" / "eval" / "summary_table.csv"),
    )
    parser.add_argument(
        "--output-md",
        default=str(root / "outputs" / "eval" / "summary_table.md"),
    )
    args = parser.parse_args()

    entries = [
        ("sample_baseline", root / "outputs" / "eval" / "baseline_metrics.json"),
        ("hard_cases", root / "outputs" / "eval" / "hard_cases_metrics.json"),
        ("full_test", root / "outputs" / "eval" / "test_metrics.json"),
    ]

    rows = []
    for name, path in entries:
        if not path.exists():
            continue
        metrics = load_json(path)
        rows.append(
            {
                "dataset": name,
                "samples": metrics["total_samples"],
                "exact_match_samples": metrics["exact_match_samples"],
                "line_accuracy": metrics["line_accuracy"],
                "character_accuracy": metrics["character_accuracy"],
                "total_edit_distance": metrics["total_edit_distance"],
                "average_edit_distance": metrics["average_edit_distance"],
            }
        )

    output_csv = Path(args.output_csv)
    output_md = Path(args.output_md)
    output_csv.parent.mkdir(parents=True, exist_ok=True)

    with output_csv.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "dataset",
                "samples",
                "exact_match_samples",
                "line_accuracy",
                "character_accuracy",
                "total_edit_distance",
                "average_edit_distance",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    md_lines = [
        "| Dataset | Samples | Exact Match | Line Acc | Char Acc | Total Edit Distance | Avg Edit Distance |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        md_lines.append(
            f"| {row['dataset']} | {row['samples']} | {row['exact_match_samples']} | "
            f"{float(row['line_accuracy']):.6f} | {float(row['character_accuracy']):.6f} | "
            f"{row['total_edit_distance']} | {float(row['average_edit_distance']):.6f} |"
        )
    output_md.write_text("\n".join(md_lines), encoding="utf-8")

    print("\n".join(md_lines))
    print(f"saved: {output_csv}")
    print(f"saved: {output_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
