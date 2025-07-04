import clip
import torch
import logging
import requests
from PIL import Image
from io import BytesIO
from typing import Union
from transformers import BlipProcessor, BlipForConditionalGeneration

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
                    img_source: Union[str, bytes, Image.Image],
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
            elif isinstance(img_source, bytes):
                img = Image.open(BytesIO(img_source)).convert('RGB')
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

class GetTextEmbedding:
    def __init__(self, model_name=("ViT-B/16"), device='cpu'):
        self.device = device
        self.model, self.preprocess = clip.load(model_name, device=device)

    def get_embedding(self, img_path):
        img = self.preprocess(Image.open(img_path)).unsqueeze(0).to(self.device)
        with torch.no_grad():
            return self.model.encode_image(img).numpy()