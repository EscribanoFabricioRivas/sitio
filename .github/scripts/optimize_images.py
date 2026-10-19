"""Compress oversized images so pages stay light on mobile.

Any JPG/PNG/WebP over MAX_KB or wider/taller than MAX_PX is resized and
re-encoded in place (same file name, so no HTML changes are needed).
"""
import pathlib
import sys

from PIL import Image

MAX_KB = 300
MAX_PX = 1600
changed = []

for path in pathlib.Path(".").rglob("*"):
    if ".git" in path.parts or path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
        continue
    size_kb = path.stat().st_size / 1024
    with Image.open(path) as im:
        if size_kb <= MAX_KB and max(im.size) <= MAX_PX:
            continue
        im.thumbnail((MAX_PX, MAX_PX))
        suffix = path.suffix.lower()
        if suffix in {".jpg", ".jpeg"}:
            im.convert("RGB").save(path, quality=82, optimize=True, progressive=True)
        elif suffix == ".webp":
            im.save(path, quality=80, method=6)
        else:
            im.save(path, optimize=True)
    changed.append(f"{path}: {size_kb:.0f}KB -> {path.stat().st_size / 1024:.0f}KB")

print("\n".join(changed) or "No oversized images.")
sys.exit(0)
