import vk_api
import os

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.exceptions import ApiError
from dotenv import load_dotenv


class EchoBot:
    def __init__(self) -> None:
        load_dotenv()

        self.session = vk_api.VkApi(token=os.getenv('TOKEN'))

        try:
            self.long_poll = VkBotLongPoll(self.session, os.getenv('GROUP_ID'))
        except ApiError as err:
            print(err)
            exit(-1)
        else:
            print('Bot has been successfully launched')

    def run_long_pool(self) -> None:
        for event in self.long_poll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                sender_id = event.raw['object']['message']['from_id']

                if ('reply_message' in event.raw['object']['message'] or
                        len(event.raw['object']['message']['fwd_messages']) != 0 or
                        {attachment['type'] for attachment in event.raw['object']['message']['attachments']} != {
                            'photo'} or
                        len(event.raw['object']['message']['text']) != 0):
                    self.session.method("messages.send", {
                        'peer_id': sender_id,
                        'message': 'Я умею отвечать только на картинки',
                        'random_id': 0
                    })

                    continue

                attachments = []

                if event.raw['object']['message']['attachments']:
                    for attachment in event.raw['object']['message']['attachments']:
                        attachment_type = attachment['type']

                        attachment_id = attachment[attachment_type]['id']
                        owner_id = attachment[attachment_type]['owner_id']
                        access_key = attachment[attachment_type]['access_key']

                        attachments.append(f"{attachment_type}{owner_id}_{attachment_id}_{access_key}")

                self.session.method("messages.send", {
                    'peer_id': sender_id,
                    'attachment': ','.join(attachments),
                    'random_id': 0
                })
