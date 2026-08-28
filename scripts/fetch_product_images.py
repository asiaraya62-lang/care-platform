"""Download Wikimedia Commons thumbnails for PoC product photos."""

from __future__ import annotations

import csv
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "products.csv"
IMG_DIR = ROOT / "data" / "images"

# Commons file titles chosen as product-like photos (not brand packaging).
FILES: dict[str, str] = {
    "P001": "Walker. frame.jpg",
    "P002": "A woman supporting herself with a walking frame.jpg",
    "P003": "Stryker Prime TC wheelchair.jpg",
    "P004": "Pride Jazzy Select power chair 001.JPG",
    "P005": "Hospital Bed 2011.JPG",
    "P006": "Douchestoel.JPG",
    "P007": "Overbed table in hospital.jpg",
    "P008": "Grab bar.jpg",
    "P009": "Bath mat.jpg",
    "P010": "Modular Wheelchair Ramp - Upside Innovations.jpg",
    "P011": "Pressure mat.jpg",
    "P012": "Transfer bench.jpg",
    "P013": "Incontinence products.jpg",
    "P014": "Air Fluidised Bed, bzw. Clinitron-Bett, Universitätsklinikum Lübeck, 2019.jpg",
    "P015": "Digital blood pressure monitor.jpg",
    "P016": "Home care nurse.jpg",
    "P017": "Hospital corridor.jpg",
    "P018": "IRobot Roomba 530.jpg",
    "P019": "Vacuum cleaner.jpg",
    "P020": "Pest control.jpg",
    "P021": "Cockroach.jpg",
    "P022": "Wheelchair.jpg",
    "P023": "Medical alert bracelet.jpg",
    "P024": "Emergency button.jpg",
    "P025": "Smoke detector.jpg",
    "P026": "Rollator.jpg",
    "P027": "Shower wheelchair.jpg",
    "P028": "Night light.jpg",
    "P029": "Hospital bed sheet.jpg",
    "P030": "Glucose meter.jpg",
    "P031": "Duvet.jpg",
    "P032": "Smartphone.jpg",
}

FALLBACKS: dict[str, list[str]] = {
    "P007": ["Hospital overbed table.jpg", "Hospital Bed 2011.JPG", "Bedside table.jpg"],
    "P009": ["Rubber bath mat.jpg", "Bathroom.jpg", "Pink bathroom suite, Skaill House, Orkney.jpg"],
    "P011": ["Floor mat.jpg", "Yoga mat.jpg", "Doormat.jpg"],
    "P013": ["Adult diaper.jpg", "Diapers.jpg", "Incontinence.jpg"],
    "P015": ["Blood pressure monitor.jpg", "Sphygmomanometer.jpg", "Omron.jpg"],
    "P016": ["Nurse.jpg", "Visiting nurse.jpg", "Caregiver.jpg"],
    "P017": ["Patient in wheelchair.jpg", "Hospital.jpg", "Ambulance stretcher.jpg"],
    "P018": ["Roomba.jpg", "Robot vacuum.jpg", "Robotic vacuum cleaner.jpg"],
    "P019": ["House cleaning.jpg", "Mop.jpg", "Cleaning floor.jpg"],
    "P020": ["Exterminator.jpg", "Insecticide.jpg", "Pest.jpg"],
    "P021": ["Pest control.jpg", "Ant.jpg"],
    "P022": ["Bicycle repair.jpg", "Maintenance.jpg", "Toolbox.jpg"],
    "P023": ["Personal alarm.jpg", "Panic button.jpg", "Emergency pendant.jpg"],
    "P024": ["Panic button.jpg", "Doorbell.jpg", "Red button.jpg"],
    "P025": ["Smoke alarm.jpg", "Carbon monoxide detector.jpg", "Fire alarm.jpg"],
    "P027": ["Douchestoel.JPG", "Shower and toilet wheelchair.jpg", "Commode chair.jpg"],
    "P028": ["LED night light.jpg", "Nightlight.jpg", "Bedside lamp.jpg"],
    "P029": ["Incontinence pad.jpg", "Underpad.jpg", "Bed pad.jpg"],
    "P030": ["Glucometer.jpg", "Blood glucose meter.jpg", "Diabetes test.jpg"],
    "P031": ["Bedding.jpg", "Quilt.jpg", "Mattress.jpg"],
    "P032": ["Mobile phone.jpg", "Telephone.jpg", "Cell phone.jpg"],
}

UA = "CarePlatformPoC/1.0 (https://github.com/asiaraya62-lang/care-platform)"


def opener() -> urllib.request.OpenerDirector:
    o = urllib.request.build_opener()
    o.addheaders = [("User-Agent", UA)]
    return o


def imageinfo(titles: list[str]) -> dict[str, str]:
    found: dict[str, str] = {}
    o = opener()
    chunk = titles[:]
    while chunk:
        batch = chunk[:40]
        chunk = chunk[40:]
        q = urllib.parse.urlencode(
            {
                "action": "query",
                "titles": "|".join(f"File:{t}" for t in batch),
                "prop": "imageinfo",
                "iiprop": "url|mime",
                "iiurlwidth": "640",
                "format": "json",
            }
        )
        url = f"https://commons.wikimedia.org/w/api.php?{q}"
        with o.open(url, timeout=30) as resp:
            data = json_load(resp.read())
        pages = data.get("query", {}).get("pages", {})
        for page in pages.values():
            title = str(page.get("title") or "").replace("File:", "")
            infos = page.get("imageinfo") or []
            if not infos:
                continue
            thumb = infos[0].get("thumburl") or infos[0].get("url")
            if thumb:
                found[title] = thumb
        time.sleep(0.4)
    return found


def json_load(raw: bytes):
    import json

    return json.loads(raw.decode("utf-8"))


def resolve_title(pid: str, info: dict[str, str]) -> tuple[str, str] | None:
    primary = FILES[pid]
    for title in [primary, *FALLBACKS.get(pid, [])]:
        if title in info:
            return title, info[title]
        # Commons may normalize spaces/underscores
        for key, url in info.items():
            if key.replace("_", " ").lower() == title.replace("_", " ").lower():
                return key, url
    return None


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    o = opener()
    with o.open(url, timeout=30) as resp:
        dest.write_bytes(resp.read())


def main() -> None:
    titles: list[str] = []
    for pid, title in FILES.items():
        titles.append(title)
        titles.extend(FALLBACKS.get(pid, []))
    # unique preserve order
    seen: set[str] = set()
    uniq: list[str] = []
    for t in titles:
        if t not in seen:
            seen.add(t)
            uniq.append(t)
    print("querying", len(uniq), "titles")
    info = imageinfo(uniq)
    print("resolved", len(info), "files")
    missing = []
    mapping: dict[str, tuple[str, str]] = {}
    for pid in FILES:
        hit = resolve_title(pid, info)
        if not hit:
            missing.append((pid, FILES[pid]))
            continue
        mapping[pid] = hit
        print(pid, "->", hit[0])
    if missing:
        print("MISSING", missing)

    rows = []
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        if "image" not in fieldnames:
            fieldnames.append("image")
        if "image_source" not in fieldnames:
            fieldnames.append("image_source")
        for row in reader:
            pid = row["id"]
            if pid in mapping:
                title, url = mapping[pid]
                ext = ".jpg"
                if url.lower().endswith(".png"):
                    ext = ".png"
                elif url.lower().endswith(".gif"):
                    ext = ".gif"
                local = IMG_DIR / f"{pid}{ext}"
                print("download", pid, url[:80])
                try:
                    download(url, local)
                    row["image"] = f"data/images/{local.name}"
                    row["image_source"] = f"https://commons.wikimedia.org/wiki/File:{urllib.parse.quote(title)}"
                    time.sleep(0.25)
                except Exception as exc:
                    print("fail", pid, exc)
                    row["image"] = url
                    row["image_source"] = f"https://commons.wikimedia.org/wiki/File:{urllib.parse.quote(title)}"
            else:
                row["image"] = row.get("image") or ""
                row["image_source"] = row.get("image_source") or ""
            rows.append(row)

    with CSV_PATH.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print("wrote", CSV_PATH)


if __name__ == "__main__":
    main()
