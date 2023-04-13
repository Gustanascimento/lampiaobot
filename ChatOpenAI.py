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
      "generate a challeging and not easy text",
      "generate a text about an animal and a place",
      "generate a text about a famous person and a place"
      ''
    ]

  def generate_message(self, mode, text = None):

    if mode == 'THEME':
      content = random.choice(self.prompt_list) + ", with the theme " + text if text else \
                random.choice(self.prompt_list) #+ random.choice(self.prompt_art)
      
      messages=[
        {"role": "system", "content": f"you are a robot that writes random, small, tiny and simple texts to generate images to play guessing games"}, #  with the theme: {text}
        {"role": "user", "content": content},
      ]
    
    elif mode == 'TRANSLATE':
      content = f'Me retorne somente o texto entre aspas traduzido para o português: "{text}"'

      messages=[
        {"role": "system", "content": f"you are a robot that only returns a text translated from English to Portuguese"},
        {"role": "user", "content": content},
      ]

    # print("content:", content)

    return messages


  def make_text(self, mode, text):
    
    completion = openai.ChatCompletion.create(
      model = self.model,
      messages = self.generate_message(mode = mode, text = text),
      # max_tokens = 100
    )

    return completion['choices'][0]['message']['content']

if __name__ == "__main__":
  chatopenai = ChatOpenAI()
  res = chatopenai.make_text()
  print(res)