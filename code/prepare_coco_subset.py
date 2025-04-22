import os
import json
import requests             # download file from internet
import zipfile              # unzip file
import shutil               # to copy/delete files and folders
from tqdm import tqdm       # add progress bar to loops


OUTPUT_DIR = "data/images"
CAPTIONS_FILE = "data/captions.json"
COCO_URLS = {
    "images": "http://images.cocodataset.org/zips/val2014.zip",
    "annotations": "http://images.cocodataset.org/annotations/annotations_trainval2014.zip"
}
NUM_IMAGES = 100


def download_file(url, output_path):
    print(f"Downloading {url}...")
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get("content-length", 0))
    with open(output_path, "wb") as f, tqdm(total=total_size, unit="B", unit_scale=True) as pbar:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            pbar.update(len(chunk))
       

def unzip_file(zip_path, extract_path):
    print(f"Unzipping {zip_path}...")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_path)


def prepare_coco_subset():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    temp_dir = "coco_temp"
    os.makedirs(temp_dir, exist_ok=True)

    img_zip = os.path.join(temp_dir, "val2014.zip")
    ann_zip = os.path.join(temp_dir, "annotations.zip")
    
    if not os.path.exists(img_zip):
        download_file(COCO_URLS["images"], img_zip)
    if not os.path.exists(ann_zip):
        download_file(COCO_URLS["annotations"], ann_zip)
    
    unzip_file(img_zip, temp_dir)
    unzip_file(ann_zip, temp_dir)
    
    caption_file = os.path.join(temp_dir, "annotations/captions_val2014.json")
    with open(caption_file, "r") as f:
        annotations = json.load(f)
    
    image_ids = set()
    selected_captions = []
    for ann in annotations["annotations"]:
        if len(image_ids) >= NUM_IMAGES:
            break
        image_ids.add(ann["image_id"])
        selected_captions.append({
            "image_id": ann["image_id"],
            "caption": ann["caption"]
        })
    
    image_dir = os.path.join(temp_dir, "val2014")
    for img_info in annotations["images"]:
        if img_info["id"] in image_ids:
            src_path = os.path.join(image_dir, img_info["file_name"])
            dst_path = os.path.join(OUTPUT_DIR, img_info["file_name"])
            shutil.copy(src_path, dst_path)
    
    with open(CAPTIONS_FILE, "w") as f:
        json.dump(selected_captions, f, indent=4)
    
    # shutil.rmtree(temp_dir)
    print(f"Prepared {NUM_IMAGES} images in {OUTPUT_DIR} and captions in {CAPTIONS_FILE}")

if __name__ == "__main__":
    prepare_coco_subset()








#  add filetr for specific category