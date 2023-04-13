from dotenv import load_dotenv
from telebot import TeleBot, apihelper
from loguru import logger
from time import sleep
from traceback import print_exc, format_exc

from ChatOpenAI import ChatOpenAI
from StableDiffusion import StableDiffusion
from Pinecone import PineconeEmbedder

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


class TelegramBot:
    def __init__(self, token):
        self.logger = logger
        self.bot = TeleBot(token)
        self.players_answers = {}
        self.chat_id = None
        self.has_started = False
        self.accepting_answers = False
        self.chatopenai = None
        self.stablediffusion = None
        self.embedder = None

    
    def send_help_message(self, message):
        reply = "Olá\! Eu sou o *Lampião* 😃\n\(_Linguagem Automatizada de Mensagens Processadas em Interface Ágil Online_\)\n\nAqui está uma lista de comandos que suporto:\n\
\- */help* \- exibe esta mensagem de ajuda\n\
\- */status* \- retorno com o status do servidor onde estou executando\n\
\- */start* \- inicia uma nova rodada\n\n\
_Disciplina de Criatividade Computacional \- IF866_ 👨‍🎓"
        self.bot.reply_to(message, reply, parse_mode='MarkdownV2')
        self.logger.debug(f'Sent help message')
        

    def run_bot(self):
        @self.bot.message_handler(commands=['status'])
        def status(message):
            self.bot.reply_to(message, "Tô aqui, meu patrão!")
            self.logger.debug(f'Sent status message')
        
        @self.bot.message_handler(commands=['help'])
        def help(message):
            self.send_help_message(message)        

        @self.bot.message_handler(commands=['start'])
        def start_game(message):
            theme = message.text.split()[1] if len(message.text.split()) > 1 else None
            self.chat_id = message.chat.id

            if self.has_started:
                self.bot.reply_to(message, f"Uma partida já está em andamento! Aguarde sua finalização antes de iniciar outra :)")
                #self.bot.send_message(self.chat_id, f"Uma partida já está em andamento! Aguarde sua finalização antes de iniciar outra :)")
            else:
                self.has_started = True
                self.players_answers = {}
                self.chatopenai = ChatOpenAI()
                self.stablediffusion = StableDiffusion()
                self.embedder = PineconeEmbedder()

                while self.has_started:
                    self.logger.info(f"Round has been started!")
                    self.bot.send_message(self.chat_id, f"Prepare-se! Inciando uma nova partida em 5 segundos! ⏰")
                    sleep(5)
                    self.bot.send_message(self.chat_id, f"Aguarde... o ChatGPT está gerando um prompt 💬")

                    try:
                        chatgpt_prompt = self.chatopenai.make_text(theme)
                        chatgpt_prompt_ptbr = self.chatopenai.translate_text(chatgpt_prompt)
                        self.logger.debug(f"Prompt gerado (EN): {chatgpt_prompt}")
                        self.logger.debug(f"Prompt gerado (PT-BR): {chatgpt_prompt_ptbr}")
                    except Exception as e:
                        print_exc()
                        self.bot.send_message(self.chat_id, f"Ocorreu um erro: {format_exc()}")
                        self.has_started = False
                        break

                    self.bot.send_message(self.chat_id, f"Gerando imagem via stable diffusion... 🖼️")

                    try:
                        imagem = self.stablediffusion.predict(text=chatgpt_prompt)
                    except Exception as e:
                        print_exc()
                        self.bot.send_message(self.chat_id, f"Ocorreu um erro: {e}")
                        self.has_started = False
                        break

                    try:
                        self.bot.send_photo(self.chat_id, imagem, caption="Aqui está! Qual prompt você acredita que o ChatGPT enviou ao Stable Diffusion para que essa imagem fosse gerada?")
                    except Exception as e:
                        print_exc()
                        self.bot.send_message(self.chat_id, f"Ocorreu um erro: {e}")
                        self.has_started = False
                        break
                    
                    self.accepting_answers = True
                    sleep(3)

                    for seconds in reversed(range(30)):
                        if seconds == 29:
                            self.bot.send_message(self.chat_id, f"30 segundos restantes ⏰")

                        if seconds == 14:
                            self.bot.send_message(self.chat_id, f"15 segundos restantes ⏰")
                        
                        if seconds == 4:
                            self.bot.send_message(self.chat_id, f"5 segundos restantes!")

                        self.logger.debug(f"Timer: {seconds}s")
                        sleep(1)
                    
                    self.bot.send_message(self.chat_id, f"Tempo esgotado! 🍃 Prompt original: *{chatgpt_prompt_ptbr}*", parse_mode="Markdown")
                    self.bot.send_message(self.chat_id, f"Calculando pontuações...")
                    self.accepting_answers = False

                    if self.players_answers == {}:
                        self.bot.send_message(self.chat_id, f"Nenhum jogador submeteu uma resposta a tempo! 😥")
                    else:
                        try:
                            answers = self.embedder.embed_sentences(original_prompt=chatgpt_prompt_ptbr, answers=self.players_answers)
                        except Exception as e:
                            print_exc()
                            self.bot.send_message(self.chat_id, f"Ocorreu um erro: {e}")
                            self.has_started = False
                            break

                        reply = "*Ranking:*\n"
                        
                        for index, answer in enumerate(answers):

                            if not index:
                                reply += f'O jogador *{answer[0]}* obteve a maior pontuação ({round(answer[2]*100,2)}%) com a resposta: *"{answer[1]}"*. Parabéns! 🥳\n' 
                                reply += f"\nDemais colocações:\n"
                            else:
                                reply += f"*{index+1}*º - {answer[0]}: {round(answer[2]*100,2)}%\n"

                
                        self.bot.send_message(self.chat_id, reply, parse_mode='Markdown')
                    
                    self.logger.success(f'Round has finished successfully!')
                    self.has_started = False
                    self.chatopenai = None
                    self.stablediffusion = None

                self.bot.send_message(self.chat_id, f"Obrigado por jogar! Caso deseje jogar novamente, basta enviar o comando /start")
                self.players_answers = {}

        # Read all mesages sent at the chat
        # Bot needs to be admin in order to read them all or be in a private chat
        # If not, you need to reply to its message for your message to be seen
        @self.bot.message_handler(func=lambda message: True)
        def handle_messages(message):
            chat_id = message.chat.id
            username = message.from_user.full_name
            self.logger.info(f"Received message '{message.text}' from user: '{username}' | ID: '{message.from_user.id}' in chat '{chat_id}'")

            if self.accepting_answers:
                if chat_id != self.chat_id:
                    self.logger.warning(f"Received message from another chat while match is in progress, ignoring it...")
                else:
                    player_id = username if username else message.from_user.id

                    if player_id not in self.players_answers:
                        self.players_answers[player_id] = message.text
                        self.logger.debug(f"Saved answer for {player_id}")
                    else:
                        self.logger.warning(f"Player {player_id} already submitted an answer! Ignoring it...")
        # main                
        while True:
            try:
                self.logger.success("Bot has started. Listening for messages...")
                self.bot.infinity_polling()
            except apihelper.ApiTelegramException as e:
                # If the polling times out, wait for a few seconds and retry
                self.logger.warning(f"Timeout! {e}")
                sleep(2)
                continue
            except Exception as e:
                # Handle any other exceptions here
                print_exc()
                break


if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("TELEGRAM_TOKEN")
    logger.critical(f'token: {token}')

    bot = TelegramBot(token)
    bot.run_bot()
