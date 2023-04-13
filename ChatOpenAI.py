import openai
import random

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from dotenv import load_dotenv
load_dotenv()

class ChatOpenAI():
  openai.organization = os.getenv("OPENAI_ORGANIZATION")
  openai.api_key = os.getenv("OPENAI_API_KEY")
  openai.Model.list()
  
  def __init__(self) -> None:

    self.model = 'gpt-3.5-turbo'
    
    self.prompt_list = [
      "challeging and not easy",
      "an animal and a place",
      "a famous person and a place"
    ]

    self.prompt_art = [
      ", like a masterpiece of oil painting",
      ", like a work of art created with oil paints",
      ", like a canvas brought to life by oil colors",
      ", like a portrait made with oil-based pigments",
      ", like a classic oil painting that evokes emotion",
      ", like an old-world oil painting that captures the essence of a moment",
      ", like a skillfully crafted oil painting that stands the test of time",
      ", like a richly textured oil painting with depth and dimension",
      ", like an oil painting that captures the beauty of nature",
      ", like an oil painting that tells a story with every brushstroke",
      ", like a pencil sketch come to life",
      ", like a work of art created with graphite",
      ", like a simple yet powerful drawing that conveys emotion",
      ", like a detailed line drawing that captures every nuance",
      ", like a skillfully crafted drawing that evokes awe and wonder",
      ", like a black-and-white drawing with striking contrast",
      ", like a contour drawing that highlights the subject's form",
      ", like a quick sketch that captures the essence of a moment",
      ", like a stylized drawing that adds a unique perspective",
      ", like a monochromatic drawing that creates a mood and atmosphere",
      ", like a colorful scribble made by a child",
      ", like a whimsical drawing created with crayons",
      ", like a charming and innocent drawing by a child",
      ", like a simple yet heartwarming drawing that captures a child's imagination",
      ", like a playful and imaginative drawing that reflects a child's view of the world",
      ", like a joyous and carefree drawing that radiates with innocence",
      ", like a cheerful drawing with bright colors and bold strokes",
      ", like a drawing that tells a story only a child can imagine",
      ", like a drawing that inspires and celebrates a child's creativity",
    ]
  

  def generate_message(self, mode, text = None):

    if mode == 'THEME':
      content = random.choice(self.prompt_list) + ", with the theme " + text +random.choice(self.prompt_art) if text else \
                random.choice(self.prompt_list) + random.choice(self.prompt_art)
      
      messages=[
        {"role": "system", "content": f"you are a robot that writes random, small and simple texts to generate images to play guessing games with the theme {text}"},
        {"role": "user", "content": content},
      ]

    # if mode == 'THEME' and text:
    #   content = random.choice(self.prompt_list) + ", with the theme " + text +random.choice(self.prompt_art) 
    # elif mode == 'THEME' and not text:
    #   content = random.choice(self.prompt_list) + random.choice(self.prompt_art) 
    elif mode == 'TRANSLATE':
      content = f'Me retorne somente o texto entre aspas traduzido para o português: "{text}"'

      messages=[
        {"role": "system", "content": f"you are a robot that only returns a text translated from English to Portuguese"},
        {"role": "user", "content": content},
      ]

    print("content:", content)

    # messages=[
    #   {"role": "system", "content": f"you are a robot that writes random, small and simple texts to generate images to play guessing games with the theme {text}"},
    #   {"role": "user", "content": content},
    # ]

    return messages


  def make_text(self, theme):
    
    completion = openai.ChatCompletion.create(
      model = self.model,
      messages = self.generate_message(mode = 'THEME', text = theme),
      max_tokens = 100
    )

    return completion['choices'][0]['message']['content']
  
  def translate_text(self, text_en):
    completion = openai.ChatCompletion.create(
      model = self.model,
      messages = self.generate_message(mode = 'TRANSLATE', text = text_en),
      max_tokens = 20
    )

    return completion['choices'][0]['message']['content']

if __name__ == "__main__":
  chatopenai = ChatOpenAI()
  res = chatopenai.make_text()
  print(res)