import argparse
import csv
from io import BytesIO
from pathlib import Path

import lmdb
from PIL import Image


def sanitize_text(text: str) -> str:
    return text.replace("\t", " ").replace("\r", "").replace("\n", "")


def discover_lmdb_dirs(dataset_root: Path) -> dict[str, list[Path]]:
    groups = {"train": [], "val": [], "test": []}
    for lmdb_dir in dataset_root.rglob("*"):
        if not lmdb_dir.is_dir():
            continue
        if not (lmdb_dir / "data.mdb").exists():
            continue

        name = lmdb_dir.name.lower()
        parent = lmdb_dir.parent.name.lower()
        if "train" in name or parent == "training":
            groups["train"].append(lmdb_dir)
        elif "val" in name or parent == "validation":
            groups["val"].append(lmdb_dir)
        elif "test" in name or parent == "evaluation":
            groups["test"].append(lmdb_dir)
    return groups


def export_lmdb(
    lmdb_dir: Path,
    split: str,
    output_dir: Path,
    csv_rows: list[dict[str, str]],
    max_samples: int = 0,
    skip_existing_images: bool = False,
) -> int:
    env = lmdb.open(str(lmdb_dir), readonly=True, lock=False, readahead=False, meminit=False)
    exported = 0
    with env.begin(write=False) as txn:
        total = int((txn.get(b"num-samples") or b"0").decode("utf-8"))
        split_dir = output_dir / split
        split_dir.mkdir(parents=True, exist_ok=True)

        for idx in range(1, total + 1):
            if max_samples and exported >= max_samples:
                break

            image_key = f"image-{idx:09d}".encode("utf-8")
            label_key = f"label-{idx:09d}".encode("utf-8")
            image_bin = txn.get(image_key)
            label_bin = txn.get(label_key)
            if not image_bin or not label_bin:
                continue

            text = sanitize_text(label_bin.decode("utf-8", errors="ignore"))
            if not text:
                continue

            try:
                image = Image.open(BytesIO(image_bin)).convert("RGB")
            except Exception:
                continue

            filename = f"{lmdb_dir.name}_{idx:09d}.png"
            dst = split_dir / filename
            if not (skip_existing_images and dst.exists()):
                image.save(dst)
            csv_rows.append({"filename": filename, "text": text})
            exported += 1

    env.close()
    return exported


def write_csv(rows: list[dict[str, str]], output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["filename", "text"])
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Import MindOCR/Fudan Chinese recognition LMDB datasets into image+CSV format."
    )
    root = Path(__file__).resolve().parents[1]
    parser.add_argument(
        "--dataset-root",
        default=str(root / "data" / "raw" / "mindocr_chinese_text_recognition"),
        help="Root directory containing training/validation/evaluation LMDB folders.",
    )
    parser.add_argument("--output-dir", default=str(root / "data"))
    parser.add_argument(
        "--max-samples-per-lmdb",
        type=int,
        default=0,
        help="Optional cap per LMDB folder for quick experiments. 0 means export all.",
    )
    parser.add_argument(
        "--splits",
        default="train,val,test",
        help="Comma-separated splits to import: train,val,test",
    )
    parser.add_argument(
        "--skip-existing-images",
        action="store_true",
        help="Skip rewriting images that already exist while still regenerating CSV files.",
    )
    args = parser.parse_args()

    dataset_root = Path(args.dataset_root)
    output_dir = Path(args.output_dir)
    if not dataset_root.exists():
        raise FileNotFoundError(f"Dataset root not found: {dataset_root}")

    groups = discover_lmdb_dirs(dataset_root)
    selected_splits = {item.strip() for item in args.splits.split(",") if item.strip()}
    summary = {}
    for split, lmdb_dirs in groups.items():
        if split not in selected_splits:
            continue
        rows: list[dict[str, str]] = []
        total_exported = 0
        for lmdb_dir in sorted(lmdb_dirs):
            total_exported += export_lmdb(
                lmdb_dir=lmdb_dir,
                split=split,
                output_dir=output_dir,
                csv_rows=rows,
                max_samples=args.max_samples_per_lmdb,
                skip_existing_images=args.skip_existing_images,
            )

        write_csv(rows, output_dir / f"labels_{split}.csv")
        summary[split] = {"lmdb_dirs": len(lmdb_dirs), "samples": total_exported}

    sample_rows = []
    train_csv = output_dir / "labels_train.csv"
    if "train" in selected_splits and train_csv.exists():
        with train_csv.open("r", encoding="utf-8-sig", newline="") as f:
            for idx, row in enumerate(csv.DictReader(f)):
                if idx >= 50:
                    break
                sample_rows.append(row)
    write_csv(sample_rows, output_dir / "labels_sample.csv")

    sample_dir = output_dir / "sample"
    sample_dir.mkdir(parents=True, exist_ok=True)
    for row in sample_rows:
        src = output_dir / "train" / row["filename"]
        dst = sample_dir / row["filename"]
        if src.exists() and not dst.exists():
            dst.write_bytes(src.read_bytes())

    for split, info in summary.items():
        print(f"{split}: {info['lmdb_dirs']} lmdb dirs, {info['samples']} samples")
    print(f"sample set prepared: {len(sample_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
