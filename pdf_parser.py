import pdfplumber
import re
from core.models import Product

PRICE_RE = re.compile(r"(.+?)\s+(\d+[,.]\d+)\s*€")

def parse_flyer(pdf_path: str, shop: str) -> list[Product]:
    products = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            for line in text.splitlines():
                match = PRICE_RE.search(line)
                if match:
                    products.append(Product(
                        shop=shop,
                        name=match.group(1).lower().strip(),
                        price=float(match.group(2).replace(",", ".")),
                        quantity=1,
                        unit="item"
                    ))

    return products
