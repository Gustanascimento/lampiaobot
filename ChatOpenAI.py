import os
from dotenv import load_dotenv
import openai

load_dotenv()

class ChatOpenAI():
  openai.organization = os.getenv("OPENAI_ORGANIZATION")
  openai.api_key = os.getenv("OPENAI_API_KEY")
  openai.Model.list()
  
  def __init__(self, model: str = 'gpt-3.5-turbo') -> None:
    self.model = model
    self.message_image_generator = [
        {"role": "system", "content": "you are a system that writes small texts to generate images to play guessing games"}
      , {"role": "user", "content": "create a sentence in a simple and descriptive way about an image that is difficult to get right but contextualized and realistic"}
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