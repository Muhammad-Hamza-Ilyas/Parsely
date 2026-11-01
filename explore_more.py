from datasets import load_dataset
import json, os

ds = load_dataset("naver-clova-ix/cord-v2")
os.makedirs("data/cord_preview", exist_ok=True)

for i in range(20):
    sample = ds["train"][i]
    sample["image"].save(f"data/cord_preview/receipt_{i:02d}.png")
    truth = json.loads(sample["ground_truth"])["gt_parse"]
    print("-" * 40)
    print("receipt", i)
    print("menu :", truth.get("menu"))
    print("total:", truth.get("total"))