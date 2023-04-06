from dotenv import load_dotenv
import replicate
import requests


import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from dotenv import load_dotenv
load_dotenv()

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

class StableDiffusion ():
    def __init__(self) -> None:
        self.model = replicate.models.get("stability-ai/stable-diffusion")
        self.version = self.model.versions.get("db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf")
        
    def predict(self, text: str):
        output_url = self.version.predict(prompt=f"{text}")[0]
        response = requests.get(output_url)
        if response.status_code == 200:
            return response.content
        return False

if __name__ == "__main__":
    sd = StableDiffusion()

    res = sd.predict(text = 'man running on Boa Viagem beach with a shark', image_name = 'image002.jpg')
    print(res)