import argparse
import csv
import random
import shutil
from pathlib import Path


IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}


def read_labels(label_file: Path) -> list[dict[str, str]]:
    with label_file.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = []
        for row in reader:
            filename = (row.get("filename") or "").strip()
            text = (row.get("text") or "").strip()
            if filename and text:
                rows.append({"filename": filename, "text": text})
        return rows


def write_labels(rows: list[dict[str, str]], output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["filename", "text"])
        writer.writeheader()
        writer.writerows(rows)


def copy_split_images(rows: list[dict[str, str]], source_dir: Path, target_dir: Path) -> None:
    target_dir.mkdir(parents=True, exist_ok=True)
    for row in rows:
        src = source_dir / row["filename"]
        if src.exists():
            shutil.copy2(src, target_dir / row["filename"])


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare train/val/test CSV files and split images.")
    root = Path(__file__).resolve().parents[1]
    parser.add_argument("--input-dir", default=str(root / "data" / "raw"))
    parser.add_argument("--label-file", default=str(root / "data" / "labels_sample.csv"))
    parser.add_argument("--output-dir", default=str(root / "data"))
    parser.add_argument("--train-ratio", type=float, default=0.8)
    parser.add_argument("--val-ratio", type=float, default=0.1)
    parser.add_argument("--test-ratio", type=float, default=0.1)
    parser.add_argument("--max-text-length", type=int, default=0)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    if round(args.train_ratio + args.val_ratio + args.test_ratio, 6) != 1.0:
        raise ValueError("train_ratio + val_ratio + test_ratio must equal 1.0")

    input_dir = Path(args.input_dir)
    label_file = Path(args.label_file)
    output_dir = Path(args.output_dir)

    rows = read_labels(label_file)
    cleaned = []
    missing_files = 0
    for row in rows:
        image_path = input_dir / row["filename"]
        if image_path.suffix.lower() not in IMAGE_SUFFIXES or not image_path.exists():
            missing_files += 1
            continue
        if args.max_text_length and len(row["text"]) > args.max_text_length:
            continue
        cleaned.append(row)

    random.Random(args.seed).shuffle(cleaned)

    total = len(cleaned)
    train_end = int(total * args.train_ratio)
    val_end = train_end + int(total * args.val_ratio)
    splits = {
        "train": cleaned[:train_end],
        "val": cleaned[train_end:val_end],
        "test": cleaned[val_end:],
    }

    for split_name, split_rows in splits.items():
        split_dir = output_dir / split_name
        copy_split_images(split_rows, input_dir, split_dir)
        write_labels(split_rows, output_dir / f"labels_{split_name}.csv")

    print(f"total labeled rows: {len(rows)}")
    print(f"usable rows: {total}")
    print(f"missing or invalid files removed: {missing_files}")
    for split_name, split_rows in splits.items():
        print(f"{split_name}: {len(split_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
