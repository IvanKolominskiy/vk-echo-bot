import vk_api
import os

from vk_api.bot_longpoll import VkBotLongPoll
from dotenv import load_dotenv


class EchoBot:
    def __init__(self):
        load_dotenv()

        self.session = vk_api.VkApi(token=os.getenv('TOKEN'))

        self.long_poll = VkBotLongPoll(self.session, os.getenv('GROUP_ID'))
