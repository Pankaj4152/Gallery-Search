import sqlite3
import os
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import json


# Paths
IMAGE_DIR = "data\\images"
CAPTIONS_FILE = "data/captions.json"
DB_PATH = "data/gallery.db"


model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def describe_image(image_path):
    try:
        image = Image.open(image_path).convert("RGB")
        labels = ["dog on beach", "cat on couch", "sunset", "person in park"]
        inputs = processor(text=labels, images=image, return_tensors="pt", padding=True)
        outputs = model(**inputs)
        probs = outputs.logits_per_image.softmax(dim=1)
        return labels[probs.argmax()]
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return "Unknown"

def populate_database():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS images (path TEXT, description TEXT)")
    
    # Load COCO captions
    with open(CAPTIONS_FILE, "r") as f:
        captions = json.load(f)
    
    # Map image IDs to captions (use first caption per image for simplicity)
    id_to_caption = {}
    for caption in captions:
        if caption["image_id"] not in id_to_caption:
            id_to_caption[caption["image_id"]] = caption["caption"]

    
    # Store in database
    for img in os.listdir(IMAGE_DIR):
        if img.endswith(".jpg"):
            img_id = int(img.split("_")[-1].split(".")[0])
            desc = id_to_caption.get(img_id, "Unknown")
            # Optional: Use CLIP instead
            # desc = describe_image(f"{IMAGE_DIR}/{img}")
            c.execute("INSERT INTO images VALUES (?, ?)", (f"{IMAGE_DIR}/{img}", desc))
    
    conn.commit()
    conn.close()
    print(f"Populated database at {DB_PATH}")

if __name__ == "__main__":
    populate_database()