import argparse
import csv
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def load_font(font_size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/simhei.ttf"),
        Path("C:/Windows/Fonts/simsun.ttc"),
    ]
    for font_path in candidates:
        if font_path.exists():
            return ImageFont.truetype(str(font_path), font_size)
    return ImageFont.load_default()


def wrap_text(text: str, max_chars: int = 28) -> list[str]:
    return [text[i : i + max_chars] for i in range(0, len(text), max_chars)] or [""]


def save_annotated_image(src_image: Path, dst_image: Path, title_lines: list[str]) -> None:
    image = Image.open(src_image).convert("RGB")
    font = load_font(24)
    padding = 20
    line_height = 34
    panel_height = padding * 2 + line_height * len(title_lines)

    canvas = Image.new("RGB", (image.width, image.height + panel_height), color="white")
    canvas.paste(image, (0, 0))
    draw = ImageDraw.Draw(canvas)

    y = image.height + padding
    for line in title_lines:
        draw.text((padding, y), line, fill="black", font=font)
        y += line_height

    dst_image.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(dst_image)


def export_case_images(rows: list[dict[str, str]], input_dir: Path, output_dir: Path, limit: int) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    for old_file in output_dir.iterdir():
        if old_file.is_file():
            old_file.unlink()

    for row in rows[:limit]:
        src = input_dir / row["filename"]
        if not src.exists():
            continue
        lines = [f"file: {row['filename']}"]
        lines.extend(f"gt: {part}" for part in wrap_text(row.get("gt_text", "")))
        lines.extend(f"pred: {part}" for part in wrap_text(row.get("pred_text", "")))
        save_annotated_image(src, output_dir / row["filename"], lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Visualize correct and incorrect OCR cases.")
    root = Path(__file__).resolve().parents[1]
    parser.add_argument("--pred-file", default=str(root / "outputs" / "preds" / "baseline_preds.csv"))
    parser.add_argument("--input-dir", default=str(root / "data" / "sample"))
    parser.add_argument("--output-dir", default=str(root / "outputs" / "figures"))
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    pred_file = Path(args.pred_file)
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)

    with pred_file.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    correct_rows = [row for row in rows if row.get("exact_match") == "1"]
    error_rows = [row for row in rows if row.get("exact_match") != "1"]

    export_case_images(correct_rows, input_dir, output_dir / "correct_cases", args.limit)
    export_case_images(error_rows, input_dir, output_dir / "error_cases", args.limit)

    print(f"correct cases exported: {min(len(correct_rows), args.limit)}")
    print(f"error cases exported: {min(len(error_rows), args.limit)}")
    print(f"figures saved to: {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
