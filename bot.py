import os
from dotenv import load_dotenv
from telebot import TeleBot
import openai
from loguru import logger
import requests
from time import sleep
import traceback
from ChatOpenAI import ChatOpenAI
from StableDiffusion import StableDiffusion

class TelegramBot:
    def __init__(self, token):
        self.logger = logger
        self.bot = TeleBot(token)
        self.players = []
        self.chat_id = None
        self.has_started = False
        self.chatopenai = ChatOpenAI()
        self.stablediffusion = StableDiffusion()

    def run_bot(self):
        @self.bot.message_handler(commands=['status'])
        def status(message):
            self.bot.reply_to(message, "Tô aqui, meu patrão!")
            self.logger.debug(f'Sent status message')
        
        @self.bot.message_handler(commands=['help'])
        def help(message):
            reply = "Olá! Eu sou o *Lampião* 😃\n(_Linguagem Automatizada de Mensagens Processadas em Interface Ágil Online_)\n\nAqui está uma lista de comandos que suporto:\n\
- */help* - exibe esta mensagem de ajuda\n\
- */status* - retorno com o status do servidor onde estou executando\n\
- */start* - inicia uma nova rodada\n\n\
_Disciplina de Criatividade Computacional - IF866_ 👨‍🎓"
            self.bot.reply_to(message, reply, parse_mode='Markdown')
            self.logger.debug(f'Sent help message')

        @self.bot.message_handler(commands=['start'])
        def start_game(message):
            self.chat_id = message.chat.id

            if self.has_started:
                self.bot.reply_to(message, f"Uma partida já está em andamento! Aguarde sua finalização antes de iniciar outra :)")
                #self.bot.send_message(self.chat_id, f"Uma partida já está em andamento! Aguarde sua finalização antes de iniciar outra :)")
            else:
                self.has_started = True
                self.players = []

                self.bot.send_message(self.chat_id, f"Get ready! Inciando uma nova partida em 5 segundos!")
                sleep(5)
                self.bot.send_message(self.chat_id, f"Aguarde... o ChatGPT está gerando um prompt")

                try:
                    texto = self.chatopenai.make_text()
                except Exception as e: 
                    self.bot.send_message(self.chat_id, f"Ocorreu um erro: {e}")

                self.logger.debug(f"Texto gerado: {texto}")

                self.bot.send_message(self.chat_id, f"Gerando imagem via stable diffusion...")

                try:
                    imagem = self.stablediffusion.predict(text=texto)
                except Exception as e:
                    self.bot.send_message(self.chat_id, f"Ocorreu um erro: {e}")

                try:
                    self.bot.send_photo(self.chat_id, imagem, caption="Aqui está! Qual prompt você acredita que o ChatGPT enviou ao Stable Diffusion para que essa imagem fosse gerada?")
                except Exception as e:
                    self.bot.send_message(self.chat_id, f"Ocorreu um erro: {e}")

                sleep(10)
                
                self.bot.send_message(self.chat_id, f"Tempo esgotado! Calculando pontuações...")
                sleep(1)

                if self.players == []:
                    self.bot.send_message(self.chat_id, f"Nenhum jogador submeteu uma resposta a tempo! 😥")
                else:
                    pass
                    #embeddeds
                    #self.players
                    self.bot.send_message(self.chat_id, f"Ranking:")
                    for player in self.players:
                        print(player)

                self.bot.send_message(self.chat_id, f"Obrigado por jogar! Caso deseje jogar novamente, basta enviar o comando /start")
                self.has_started = False
                self.players = []

        # Read all mesages sent at the chat
        # Bot needs to be admin in order to read them all or be in a private chat
        # If not, you need to reply to its message for your message to be seen
        @self.bot.message_handler(func=lambda message: True)
        def handle_messages(message):
            chat_id = message.chat.id
            text = message.text
            username = message.from_user.username
            self.logger.info(f"Received message '{text}' from user '{username}' in chat '{chat_id}'")
            self.players.append(f"")
            # self.bot.send_message(message.chat.id, f"User {username} said: '{text}'")

        self.logger.success("Bot has started. Listening for messages...")
        self.bot.infinity_polling()



if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("TELEGRAM_TOKEN")
    logger.critical(f'token: {token}')

    bot = TelegramBot(token)
    bot.run_bot()
