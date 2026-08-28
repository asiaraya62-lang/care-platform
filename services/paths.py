from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
IMAGE_DIR = ROOT / "static" / "products"
BANNER_DIR = ROOT / "static" / "banners"
PRODUCTS_CSV = DATA_DIR / "products.csv"
VENDORS_CSV = DATA_DIR / "vendors.csv"
PROGRAMS_CSV = DATA_DIR / "support_programs.csv"
