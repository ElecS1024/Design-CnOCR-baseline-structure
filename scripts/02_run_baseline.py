import argparse
import csv
from pathlib import Path
from statistics import mean
from typing import Any


IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}


def load_labels(label_file: Path) -> dict[str, str]:
    with label_file.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return {
            row["filename"].strip(): row["text"].strip()
            for row in reader
            if row.get("filename") and row.get("text")
        }


def extract_text_and_score(result: Any) -> tuple[str, float | None]:
    if result is None:
        return "", None
    if isinstance(result, str):
        return result, None
    if isinstance(result, dict):
        text = str(
            result.get("text")
            or result.get("pred")
            or result.get("prediction")
            or result.get("value")
            or ""
        )
        score = result.get("score") or result.get("confidence") or result.get("prob")
        return text, float(score) if isinstance(score, (int, float)) else None
    if isinstance(result, (list, tuple)):
        if len(result) == 2 and isinstance(result[0], str) and isinstance(result[1], (int, float)):
            return result[0], float(result[1])

        parts = []
        scores = []
        for item in result:
            text, score = extract_text_and_score(item)
            if text:
                parts.append(text)
            if score is not None:
                scores.append(score)
        merged = "".join(parts)
        avg_score = mean(scores) if scores else None
        return merged, avg_score
    return str(result), None


def predict_single_line(ocr: Any, image_path: Path) -> tuple[str, float | None]:
    if hasattr(ocr, "ocr_for_single_line"):
        result = ocr.ocr_for_single_line(str(image_path))
    else:
        result = ocr.ocr(str(image_path))
    return extract_text_and_score(result)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run CnOCR baseline inference on sample images.")
    root = Path(__file__).resolve().parents[1]
    parser.add_argument("--input-dir", default=str(root / "data" / "sample"))
    parser.add_argument("--label-file", default=str(root / "data" / "labels_sample.csv"))
    parser.add_argument("--output-file", default=str(root / "outputs" / "preds" / "baseline_preds.csv"))
    parser.add_argument(
        "--rec-model-name",
        default="",
        help="Optional recognition model name. Leave empty to use cnocr default.",
    )
    args = parser.parse_args()

    from cnocr import CnOcr

    input_dir = Path(args.input_dir)
    label_file = Path(args.label_file)
    output_file = Path(args.output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    labels = load_labels(label_file)
    image_paths = sorted(
        p for p in input_dir.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES
    )

    ocr = CnOcr(rec_model_name=args.rec_model_name) if args.rec_model_name else CnOcr()
    rows = []
    for image_path in image_paths:
        gt_text = labels.get(image_path.name, "")
        pred_text, score = predict_single_line(ocr, image_path)
        rows.append(
            {
                "filename": image_path.name,
                "gt_text": gt_text,
                "pred_text": pred_text,
                "score": "" if score is None else f"{score:.6f}",
                "exact_match": int(pred_text == gt_text),
            }
        )

    with output_file.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["filename", "gt_text", "pred_text", "score", "exact_match"]
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"model: {args.rec_model_name or 'cnocr default model'}")
    print(f"images processed: {len(rows)}")
    print(f"results saved to: {output_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
