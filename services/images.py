from __future__ import annotations

from pathlib import Path

from services.paths import BANNER_DIR, IMAGE_DIR


def product_image_path(product_id: str) -> Path | None:
    path = IMAGE_DIR / f"{product_id}.jpg"
    return path if path.exists() else None


def banner_image_path(name: str) -> Path | None:
    path = BANNER_DIR / f"{name}.jpg"
    return path if path.exists() else None
