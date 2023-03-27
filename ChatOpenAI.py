import os
from dotenv import load_dotenv
import openai
import random

load_dotenv()

class ChatOpenAI():
  openai.organization = os.getenv("OPENAI_ORGANIZATION")
  openai.api_key = os.getenv("OPENAI_API_KEY")
  openai.Model.list()
  
  def __init__(self, model: str = 'gpt-3.5-turbo') -> None:
    self.prompt_list = [
      "create a very random phrase simply and directly over an image.",
      "create a short and simple sentence with a random animal, year and historical place with easy words."
    ]

    self.model = model
    self.message_image_generator = [
        {"role": "system", "content": "you are a system that writes random and small texts to generate images to play guessing games. you send the answer as two strings: the first is the sentence in english and the second is in portuguese."}
      , {"role": "user", "content": random.choice(self.prompt_list) + " It could be an oil painting, or a drawing or funny"}
    ]

  def make_text(self):
    completion = openai.ChatCompletion.create(
    model = self.model,
    messages = self.message_image_generator
    )

    return completion['choices'][0]['message']['content']

if __name__ == "__main__":
  chatopenai = ChatOpenAI()
  res = chatopenai.make_text()
  print(res)