import argparse
import platform
import sys
from importlib.metadata import PackageNotFoundError, version


def get_version(pkg_name: str, fallback: str = "unknown") -> str:
    try:
        return version(pkg_name)
    except PackageNotFoundError:
        return fallback


def main() -> int:
    parser = argparse.ArgumentParser(description="Check the CnOCR baseline environment.")
    parser.add_argument(
        "--rec-model-name",
        default="",
        help="Optional recognition model name. Leave empty to use cnocr default.",
    )
    args = parser.parse_args()

    print(f"Python version: {sys.version.split()[0]}")
    print(f"Platform: {platform.platform()}")

    try:
        import torch

        print(f"torch ok: {torch.__version__}")
        print(f"cuda available: {torch.cuda.is_available()}")
    except Exception as exc:
        print(f"torch failed: {exc}")
        return 1

    try:
        import cv2

        print(f"opencv ok: {cv2.__version__}")
    except Exception as exc:
        print(f"opencv failed: {exc}")
        return 1

    try:
        from cnocr import CnOcr

        print(f"cnocr ok: {get_version('cnocr')}")
        if args.rec_model_name:
            _ = CnOcr(rec_model_name=args.rec_model_name)
            print(f"model load ok: {args.rec_model_name}")
        else:
            _ = CnOcr()
            print("model load ok: cnocr default model")
    except Exception as exc:
        print(f"cnocr/model failed: {exc}")
        return 1

    print("environment check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
