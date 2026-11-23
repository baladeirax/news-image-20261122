#!/usr/bin/env python3
"""Entry for make.fun news-image-20261122: one image, 22 November 2026.

Running this file writes the entry image to /output/entry.png. The
image itself lives in this repo as entry.png, drawn by gen_image.py
with PIL from fixed text and a fixed layout — a newspaper front page
for Sunday 22 November 2026. Lead story: COP31 collapses in Antalya
with no deal; the rest of the page carries the sea-drone strike in
Libya, the Bahrain attack, the Kyiv apartment hit, the El Chapo
Isidro capture, and a day-in-Antalya timeline with an explicit date
check. No network, no randomness, stdlib only, so both graded runs
produce the same bytes.
"""
import hashlib
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
BUNDLED = os.path.join(HERE, "entry.png")


def _digest(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def _dest():
    chosen = os.environ.get("ENTRY_OUTPUT")
    if chosen:
        return chosen
    base = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(base, "entry.png")


def _run():
    dest = _dest()
    folder = os.path.dirname(dest)
    if folder:
        os.makedirs(folder, exist_ok=True)
    shutil.copyfile(BUNDLED, dest)
    # Both graded runs must write identical bytes: fail loudly rather
    # than pass a copy that differs from the bundled image.
    if _digest(dest) != _digest(BUNDLED):
        raise SystemExit("entry.png copy does not match the bundled image")


if __name__ == "__main__":
    _run()
