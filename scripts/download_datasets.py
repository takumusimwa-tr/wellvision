"""
WellVision — Dataset Download Script
======================================
Downloads the FORCE 2020 well log lithofacies dataset from Zenodo.

Dataset: 118 wells, Norwegian Sea, 12 lithofacies classes
Source : https://zenodo.org/records/4351156
License: NOLD 2.0

Usage:
    python scripts/download_datasets.py
"""

import sys
import zipfile
from pathlib import Path

import requests
from tqdm import tqdm

ROOT    = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw" / "force2020"
RAW_DIR.mkdir(parents=True, exist_ok=True)

ZIP_URL  = "https://zenodo.org/records/4351156/files/LAS_files_Force_2020_all_wells_train_test_blind_hidden_final.zip?download=1"
ZIP_NAME = "force2020_las.zip"


def download_file(url: str, dest: Path) -> bool:
    if dest.exists():
        print(f"  Already exists: {dest.name} ({dest.stat().st_size / 1e6:.1f} MB)")
        return True

    print(f"  Downloading: {dest.name}")
    try:
        r = requests.get(url, stream=True, timeout=120)
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        with open(dest, "wb") as f, tqdm(
            total=total, unit="B", unit_scale=True,
            desc=dest.name, ncols=80
        ) as bar:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
                bar.update(len(chunk))
        print(f"  Saved: {dest.name} ({dest.stat().st_size / 1e6:.1f} MB)")
        return True
    except Exception as e:
        print(f"  Failed: {e}")
        if dest.exists():
            dest.unlink()
        return False


def extract_zip(zip_path: Path, dest_dir: Path):
    print(f"\n  Extracting {zip_path.name}...")
    with zipfile.ZipFile(zip_path, "r") as z:
        members = z.namelist()
        print(f"  Found {len(members)} files in archive")
        for member in tqdm(members, desc="Extracting", ncols=80):
            z.extract(member, dest_dir)
    print(f"  Extracted to: {dest_dir}")


def verify_dataset():
    las_files = list(RAW_DIR.rglob("*.las")) + list(RAW_DIR.rglob("*.LAS"))
    print(f"\n  LAS files found: {len(las_files)}")
    if las_files:
        print(f"  Sample files  : {[f.name for f in las_files[:5]]}")
    return len(las_files)


def main():
    print("=" * 60)
    print("WellVision — FORCE 2020 Dataset Download")
    print("=" * 60)
    print(f"Destination: {RAW_DIR}\n")

    zip_path = RAW_DIR / ZIP_NAME

    # Download
    if not download_file(ZIP_URL, zip_path):
        print("Download failed.")
        sys.exit(1)

    # Extract
    las_files = list(RAW_DIR.rglob("*.las")) + list(RAW_DIR.rglob("*.LAS"))
    if len(las_files) < 10:
        extract_zip(zip_path, RAW_DIR)
    else:
        print(f"  Already extracted ({len(las_files)} LAS files found)")

    # Verify
    n = verify_dataset()
    if n >= 50:
        print("\n" + "=" * 60)
        print(f"Download complete — {n} LAS files ready.")
        print(f"Data: {RAW_DIR}")
        print("=" * 60)
    else:
        print(f"\nWarning: only {n} LAS files found. Expected ~118.")


if __name__ == "__main__":
    main()
