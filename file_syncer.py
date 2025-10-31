"""
file_syncer.py
----------------
Features:
- Verifies file integrity using SHA256
- Skips unchanged files automatically
- Logs all operations with timestamps
- CLI support for easy use

Usage:
    python file_syncer.py --src ./source --dst ./backup
"""

import os
import shutil
import hashlib
import logging
import argparse
from pathlib import Path


def setup_logger():
    """Configure logging with timestamp and level."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def sha256sum(file_path: Path) -> str:
    """Compute SHA256 hash for a file."""
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def sync_files(src_dir: Path, dst_dir: Path):
    """Synchronize files from src to dst with hash comparison."""
    if not src_dir.exists():
        logging.error(f"Source directory not found: {src_dir}")
        return

    dst_dir.mkdir(parents=True, exist_ok=True)
    count_copied, count_skipped = 0, 0

    for file in src_dir.rglob("*"):
        if file.is_file():
            relative = file.relative_to(src_dir)
            dest_file = dst_dir / relative
            dest_file.parent.mkdir(parents=True, exist_ok=True)

            # Check if destination file exists and compare hashes
            if dest_file.exists() and sha256sum(file) == sha256sum(dest_file):
                count_skipped += 1
                logging.debug(f"Skipped (unchanged): {relative}")
                continue

            shutil.copy2(file, dest_file)
            count_copied += 1
            logging.info(f"Copied: {relative}")

    logging.info(f"✅ Sync complete — {count_copied} files copied, {count_skipped} skipped.")


def main():
    setup_logger()

    parser = argparse.ArgumentParser(description="Sync files between folders.")
    parser.add_argument("--src", required=True, help="Source directory")
    parser.add_argument("--dst", required=True, help="Destination directory")
    args = parser.parse_args()

    sync_files(Path(args.src), Path(args.dst))


if __name__ == "__main__":
    main()
