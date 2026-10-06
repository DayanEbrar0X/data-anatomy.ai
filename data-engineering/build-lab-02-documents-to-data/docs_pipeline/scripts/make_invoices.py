"""Draw 10 scanned-looking invoice PNGs into invoices/ (deterministic).

Run from the project folder: python scripts/make_invoices.py
"""
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

INVOICES = [
    ("Northwind Office Supply", "INV-2041", "2026-09-02",
     [("Printer toner cartridge", 4, 89.00),
      ("Copy paper, 10 reams", 2, 54.50)]),
    ("Cobalt Cloud Hosting", "INV-2042", "2026-09-03",
     [("Virtual servers, September", 1, 640.00),
      ("Backup storage 2 TB", 1, 46.00)]),
    ("Harbor Coffee Roasters", "INV-2043", "2026-09-05",
     [("Espresso beans 5 kg", 3, 72.00),
      ("Oat milk, case of 12", 2, 31.50)]),
    ("Brightline Cleaning Co", "INV-2044", "2026-09-08",
     [("Office deep clean", 1, 380.00),
      ("Window washing", 1, 120.00)]),
    ("Summit Freight", "INV-2045", "2026-09-10",
     [("Pallet shipping, Denver", 2, 215.00),
      ("Liftgate fee", 1, 45.00)]),
    ("Pixel Print Shop", "INV-2046", "2026-09-12",
     [("Business cards, 500", 6, 38.00),
      ("Event posters A2", 20, 6.50)]),
    ("Northwind Office Supply", "INV-2047", "2026-09-15",
     [("Ergonomic desk chair", 3, 249.00),
      ("Monitor arm", 3, 79.00)]),
    ("Cobalt Cloud Hosting", "INV-2048", "2026-09-18",
     [("Managed database", 1, 410.00),
      ("Data transfer 800 GB", 1, 72.00)]),
    ("Harbor Coffee Roasters", "INV-2049", "2026-09-22",
     [("Cold brew kegs", 2, 96.00),
      ("Paper cups, 1000", 1, 58.00)]),
    ("Summit Freight", "INV-2050", "2026-09-26",
     [("Courier, same day", 5, 32.00),
      ("Packing crates", 4, 27.50)]),
]

W, H = 760, 980
INK = (28, 30, 36)


def font(size):
    return ImageFont.load_default(size=size)


def draw_invoice(vendor, number, date, items, seed):
    rng = random.Random(seed)
    img = Image.new("RGB", (W, H), (250, 248, 242))
    d = ImageDraw.Draw(img)
    d.text((60, 60), vendor, font=font(40), fill=INK)
    d.text((60, 160), "INVOICE", font=font(30), fill=INK)
    d.text((60, 215), f"Invoice No: {number}", font=font(26), fill=INK)
    d.text((60, 255), f"Date: {date}", font=font(26), fill=INK)
    d.line((60, 320, W - 60, 320), fill=INK, width=2)
    d.text((60, 340), "Description", font=font(24), fill=INK)
    d.text((480, 340), "Qty", font=font(24), fill=INK)
    d.text((570, 340), "Amount", font=font(24), fill=INK)
    y, total = 395, 0.0
    for desc, qty, price in items:
        amount = qty * price
        total += amount
        d.text((60, y), desc, font=font(24), fill=INK)
        d.text((480, y), str(qty), font=font(24), fill=INK)
        d.text((570, y), f"${amount:,.2f}", font=font(24), fill=INK)
        y += 50
    d.line((60, y + 20, W - 60, y + 20), fill=INK, width=2)
    d.text((60, y + 45), f"TOTAL ${total:,.2f}", font=font(30), fill=INK)
    # a little scanner realism: tilt, blur and paper noise
    img = img.rotate(rng.uniform(-0.6, 0.6), fillcolor=(250, 248, 242))
    img = img.filter(ImageFilter.GaussianBlur(0.6))
    px = img.load()
    for _ in range(4000):
        x, yy = rng.randrange(W), rng.randrange(H)
        g = rng.randint(200, 235)
        px[x, yy] = (g, g, g - 6)
    return img


if __name__ == "__main__":
    out = Path("invoices")
    out.mkdir(exist_ok=True)
    for i, (vendor, number, date, items) in enumerate(INVOICES, 1):
        img = draw_invoice(vendor, number, date, items, seed=i)
        img.save(out / f"invoice_{i:02d}.png")
    print(f"wrote {len(INVOICES)} invoices to {out}/")
