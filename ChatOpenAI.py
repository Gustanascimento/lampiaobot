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
        {"role": "system", "content": "você é um sistema que escreve pequenos textos para gerar imagens para jogar jogos de adivinhação"}
      , {"role": "user", "content": 'Escreva um texto para gerar uma imagem no jogo'}
    ]

  def make_text(self):
    completion = openai.ChatCompletion.create(
    model = self.model,
    messages = self.message_image_generator
    )

    return completion['choices'][0]['message']['content']


chatopenai = ChatOpenAI()

res = chatopenai.make_text()
print(res)