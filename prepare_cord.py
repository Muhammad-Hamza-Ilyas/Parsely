import json, os
from datasets import load_dataset
from src.numbers import parse_amount

def as_list(menu):
    if menu is None:
        return []
    return menu if isinstance(menu, list) else [menu]   # single item = one block

def cord_to_schema(gt):
    items = []
    for m in as_list(gt.get("menu")):
        if not isinstance(m, dict):
            continue
        items.append({"description": str(m.get("nm", "")),
                      "quantity": parse_amount(m.get("cnt")),
                      "unit_price": parse_amount(m.get("unitprice")),
                      "amount": parse_amount(m.get("price"))})
    total = gt.get("total", {})
    if isinstance(total, list):
        total = total[0] if total else {}
        return {"vendor": None, "date": None,
            "total": parse_amount(total.get("total_price")),
            "currency": "IDR",
            "line_items": items}

ds = load_dataset("naver-clova-ix/cord-v2")
os.makedirs("data/cord/images", exist_ok=True)

# validation split = our DEV set (we may tune against it)
# test split       = our TEST set (touch only for the final results)
for split, outfile in [("validation", "labels_dev.json"), ("test", "labels_test.json")]:
    gold = {}
    for i, row in enumerate(ds[split]):
        name = f"{split}_{i:03d}.png"
        row["image"].save(f"data/cord/images/{name}")
        gold[name] = cord_to_schema(json.loads(row["ground_truth"])["gt_parse"])
    with open(f"data/cord/{outfile}", "w", encoding="utf-8") as f:
        json.dump(gold, f, indent=1)
    print(split, len(gold), "receipts saved")