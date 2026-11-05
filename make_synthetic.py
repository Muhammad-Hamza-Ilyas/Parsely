import json, os, random
from datetime import date, timedelta
from PIL import Image, ImageDraw, ImageFont, ImageFilter

random.seed(42)
os.makedirs("data/own/images", exist_ok=True)

VENDORS = ["Green Supermarket", "Al-Noor Mart", "City Pharmacy", "Fresh Bakery",
           "Star Cafe", "Metro Grocers", "Daily Needs Store", "Blue Moon Restaurant"]
ITEMS = ["Milk", "Bread", "Eggs", "Rice", "Sugar", "Tea", "Apples", "Chicken",
         "Cooking Oil", "Yogurt", "Soap", "Shampoo", "Biscuits", "Juice", "Cheese"]
INK = (25, 25, 25)
CODES = {"$": "USD", "Rs.": "PKR", "": None}

def get_font(size):
    for name in ("cour.ttf", "couri.ttf", "DejaVuSansMono.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()

def make_receipt():
    vendor = random.choice(VENDORS)
    cur = random.choice(["$", "Rs.", ""])
    scale = 100 if cur == "Rs." else 1
    items = []
    for name in random.sample(ITEMS, random.randint(3, 10)):
        qty = random.randint(1, 3)
        unit = round(random.uniform(0.5, 6) * scale, 2)
        items.append((name, qty, round(qty * unit, 2)))
    total = round(sum(a for _, _, a in items), 2)
    d = date.today() - timedelta(days=random.randint(0, 700))
    date_text = d.strftime(random.choice(["%d/%m/%Y", "%Y-%m-%d", "%d-%b-%Y"]))

    font, big = get_font(22), get_font(30)
    W, H = 460, 260 + 34 * len(items)
    img = Image.new("RGB", (W, H), (245, 243, 235))
    dr = ImageDraw.Draw(img)

    y = 25
    dr.text(((W - dr.textlength(vendor, font=big)) / 2, y), vendor, fill=INK, font=big)
    y += 55
    dr.text((30, y), "Date: " + date_text, fill=INK, font=font)
    y += 40
    dr.line((30, y, W - 30, y), fill=INK)
    y += 15
    for name, qty, amount in items:
        dr.text((30, y), f"{qty} {name.upper()}", fill=INK, font=font)
        txt = f"{cur}{amount:,.2f}"
        dr.text((W - 30 - dr.textlength(txt, font=font), y), txt, fill=INK, font=font)
        y += 34
    dr.line((30, y, W - 30, y), fill=INK)
    y += 15
    txt = f"{cur}{total:,.2f}"
    dr.text((30, y), "TOTAL", fill=INK, font=big)
    dr.text((W - 30 - dr.textlength(txt, font=big), y), txt, fill=INK, font=big)

    # make some of them harder: tilt and blur
    if random.random() < 0.5:
        img = img.rotate(random.uniform(-6, 6), expand=True, fillcolor=(90, 90, 90))
    if random.random() < 0.3:
        img = img.filter(ImageFilter.GaussianBlur(random.uniform(1, 2.2)))

    gold = {"vendor": vendor, "date": d.isoformat(), "total": total,
            "currency": CODES[cur],
            "line_items": [{"description": n.upper(), "quantity": q, "amount": a}
                           for n, q, a in items]}
    return img, gold

dev, test = {}, {}
for i in range(1, 41):
    name = f"s{i:03d}.jpg"
    img, gold = make_receipt()
    img.save(f"data/own/images/{name}", quality=random.randint(60, 90))
    (dev if i <= 28 else test)[name] = gold

for fname, data in [("labels_synthetic_dev.json", dev), ("labels_synthetic_test.json", test)]:
    with open(f"data/own/{fname}", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1)
print("created", len(dev), "dev and", len(test), "test receipts")