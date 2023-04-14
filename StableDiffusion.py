from dotenv import load_dotenv
import replicate
import requests
import random


import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from dotenv import load_dotenv
load_dotenv()

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

class StableDiffusion ():
    PROMPT_ART = [
      ", chakra colors",
      ", realistic, full hd",
      ", funny drawing, think like a children",
      ", chakra colors",
      ", pencil drawing",
      ", cute children's drawing, amazingly good art, very detailed",
      ", ultra detailed digital art, fine drawing, grunge, hyper real, 4 k, moody lighting, warm colors, shaded",
      ", book illustration"
    ] 

    def __init__(self) -> None:
        self.model = replicate.models.get("stability-ai/stable-diffusion")
        self.version = self.model.versions.get("db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf")
        
    def predict(self, text: str):
        output_url = self.version.predict(prompt=f"{text}{random.choice(self.PROMPT_ART)}")[0]
        print(f"{text}{random.choice(self.PROMPT_ART)}")
        response = requests.get(output_url)
        if response.status_code == 200:
            return response.content
        return False

if __name__ == "__main__":
    sd = StableDiffusion()

    res = sd.predict(text = 'man running on Boa Viagem beach with a shark', image_name = 'image002.jpg')
    print(res)