from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

class GenerateImageDescription:
    def __init__(self, img_path):
        self.img_path = img_path
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base", use_fast=True)
        self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

    def img_to_text(self):
        raw_img = Image.open((self.img_path))
        #raw_img = Image.open(requests.get(img_url, stream=True).raw).convert('RGB')  #For images from URL TODO: Implement later
        inputs = self.processor(raw_img, return_tensors="pt")
        output = self.model.generate(**inputs, max_new_tokens=100)
        description = self.processor.decode(output[0], skip_special_tokens=True)

        return description


img_path = '/Users/Admin/Documents/Gallery-Search/data/images/dog4.jpg'
img_to_txt = GenerateImageDescription(img_path)
desc = img_to_txt.img_to_text()
print(desc)
    