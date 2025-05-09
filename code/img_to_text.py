from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch
import logging
from typing import Union
import requests

class GenerateImageDescription:
    def __init__(self, 
                 model="Salesforce/blip-image-captioning-base", 
                 device='cuda' if torch.cuda.is_available() else 'cpu',
                 use_fast=True):
        self.device = device   
        self.processor = BlipProcessor.from_pretrained(model, use_fast=use_fast)
        self.model = BlipForConditionalGeneration.from_pretrained(model).to(self.device)
        logging.info(f'Model: {model} loaded on {self.device}')

    def img_to_text(self, 
                    img_source: Union[str, Image.Image],
                    max_new_tokens=100,
                    temperature=0.2,
                    do_sample=True
                    ):
        try:
            if isinstance(img_source, str):
                if img_source.startswith(('http://', 'https://')):
                    img = Image.open(requests.get(img_source, stream=True).raw).convert('RGB')
                else:
                    img = Image.open(img_source).convert('RGB')
            elif isinstance(img_source, Image.Image):
                img = img_source.convert('RGB')
            else:
                raise ValueError('Unsupported image format.')

            inputs = self.processor(img, return_tensors="pt")
            output = self.model.generate(**inputs, 
                                         max_new_tokens=max_new_tokens, 
                                         temperature=temperature, 
                                         do_sample=do_sample)
            
            return self.processor.decode(output[0], skip_special_tokens=True)

        except Exception as e:
            logging.error(f'Error at image processing: {str(e)}')
            return None

    def __call__(self, img_source:Union[str, Image.Image], **kwargs):
        return self.img_to_text(img_source, **kwargs)

describer = GenerateImageDescription()
# Test with local path
description = describer('/Users/Owner/gallery-search/Gallery-Search/images/dog4.jpg') 
print(description)