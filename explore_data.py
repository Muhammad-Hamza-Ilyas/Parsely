from datasets import load_dataset
import json

ds = load_dataset("naver-clova-ix/cord-v2")
sample = ds["train"][0]
sample["image"].save("sample.png")
print(json.loads(sample["ground_truth"])["gt_parse"])