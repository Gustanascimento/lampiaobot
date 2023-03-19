import os
import dotenv
from dotenv import load_dotenv
import replicate
import requests

load_dotenv()

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

class StableDiffusion ():
    def __init__(self) -> None:
        self.model = replicate.models.get("stability-ai/stable-diffusion")
        self.version = self.model.versions.get("db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf")
        
    def predict(self, text: str, image_name: str):
        output_url = self.version.predict(prompt=f"{text}, pencil drawing, oil painting, watercolor painting, digital painting")[0]
        response = requests.get(output_url)
        if response.status_code == 200:
            content = response.content
            with open(image_name, 'wb') as f:
                f.write(content)
            return True
        return False


sd = StableDiffusion()

res = sd.predict(text = 'man running on Boa Viagem beach with a shark', image_name = 'image002.jpg')
print(res)