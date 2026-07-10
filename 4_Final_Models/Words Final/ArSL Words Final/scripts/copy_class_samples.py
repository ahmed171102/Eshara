"""Copy one KARSL .mp4 per SignID 71-170 into sample_videos/by_class/."""
from __future__ import annotations

import csv
import shutil
from pathlib import Path

import pandas as pd

BUNDLE = Path(__file__).resolve().parent.parent
DATASET_ROOT = Path(r"E:/Downloads/Arabic Words Dataset")
LABELS_XLSX = BUNDLE / "KARSL-502_Labels.xlsx"
OUT_DIR = BUNDLE / "sample_videos" / "by_class"
MANIFEST = BUNDLE / "sample_videos" / "manifest.csv"

KARSL_RANGES = ["0001-0070", "0071-0170", "0171-0190", "0191-0300", "0301-0502"]


def find_first_video(sign_id: int) -> Path | None:
    folder = f"{int(sign_id):04d}"
    for split in ("train", "test"):
        for rng in KARSL_RANGES:
            for base in (
                DATASET_ROOT / split / rng / folder,
                DATASET_ROOT / split / rng / rng / folder,
            ):
                if base.is_dir():
                    for ext in ("*.mp4", "*.avi"):
                        hits = sorted(base.glob(ext))
                        if hits:
                            return hits[0]
    return None


def main() -> None:
    if not DATASET_ROOT.exists():
        raise SystemExit(f"Dataset not found: {DATASET_ROOT}")
    if not LABELS_XLSX.exists():
        raise SystemExit(f"Labels not found: {LABELS_XLSX}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_excel(LABELS_XLSX).iloc[70:170].reset_index(drop=True)

    rows = []
    missing = []
    for i, row in df.iterrows():
        sid = int(row["SignID"])
        en = str(row["Sign-English"]).strip()
        ar = str(row["Sign-Arabic"]).strip()
        src = find_first_video(sid)
        dst_name = f"SignID{sid:04d}.mp4"
        dst = OUT_DIR / dst_name
        if src is None:
            missing.append(sid)
            rows.append(
                {
                    "class_index": i,
                    "sign_id": sid,
                    "english": en,
                    "arabic": ar,
                    "filename": "",
                    "source": "",
                    "copied": False,
                }
            )
            continue
        if not dst.exists() or dst.stat().st_size != src.stat().st_size:
            shutil.copy2(src, dst)
        rows.append(
            {
                "class_index": i,
                "sign_id": sid,
                "english": en,
                "arabic": ar,
                "filename": dst_name,
                "source": str(src),
                "copied": True,
            }
        )

    with MANIFEST.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    copied = sum(1 for r in rows if r["copied"])
    print(f"Copied {copied}/{len(rows)} videos -> {OUT_DIR}")
    print(f"Manifest -> {MANIFEST}")
    if missing:
        print(f"Missing SignIDs ({len(missing)}): {missing[:10]}{'...' if len(missing) > 10 else ''}")


if __name__ == "__main__":
    main()
