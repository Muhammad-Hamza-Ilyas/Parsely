import json, os

def load_samples(images_dir, labels_path, limit=None):
    # Returns a list of (image_path, correct_answer) pairs.
    with open(labels_path, encoding="utf-8") as f:
        labels = json.load(f)
    samples = [(os.path.join(images_dir, name), gold) for name, gold in labels.items()]
    return samples[:limit] if limit else samples