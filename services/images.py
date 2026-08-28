from __future__ import annotations

from pathlib import Path

from services.paths import BANNER_DIR, IMAGE_DIR


PROGRAM_PHOTOS = {
    "G001": "P016.jpg",
    "G002": "P003.jpg",
    "G003": "P001.jpg",
    "G004": "P008.jpg",
    "G005": "P010.jpg",
    "G006": "P016.jpg",
    "G007": "P015.jpg",
    "G008": "P017.jpg",
    "G009": "P023.jpg",
    "G010": "P013.jpg",
}


def product_image_path(product_id: str) -> Path | None:
    path = IMAGE_DIR / f"{product_id}.jpg"
    return path if path.exists() else None


def program_image_path(program_id: str) -> Path | None:
    name = PROGRAM_PHOTOS.get(program_id)
    if not name:
        return None
    path = IMAGE_DIR / name
    return path if path.exists() else None


def banner_image_path(name: str) -> Path | None:
    path = BANNER_DIR / f"{name}.jpg"
    return path if path.exists() else None
