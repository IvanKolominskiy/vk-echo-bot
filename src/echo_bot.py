import vk_api
import os

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from dotenv import load_dotenv


class EchoBot:
    def __init__(self) -> None:
        load_dotenv()

        self.session = vk_api.VkApi(token=os.getenv('TOKEN'))

        self.long_poll = VkBotLongPoll(self.session, os.getenv('GROUP_ID'))

    def run_long_pool(self) -> None:
        for event in self.long_poll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                attachments = []

                if event.raw['object']['message']['attachments']:
                    for attachment in event.raw['object']['message']['attachments']:
                        attachment_type = attachment['type']

                        attachment_id = attachment[attachment_type]['id']
                        owner_id = attachment[attachment_type]['owner_id']

                        match attachment_type:
                            case 'photo':
                                access_key = attachment[attachment_type]['access_key']

                                attachments.append(f"{attachment_type}{owner_id}_{attachment_id}_{access_key}")

                            case 'audio' | 'video':
                                attachments.append(f"{attachment_type}{owner_id}_{attachment_id}")

                sender_id = event.raw['object']['message']['from_id']

                message_text = event.raw['object']['message']['text']

                self.session.method("messages.send", {
                    'peer_id': sender_id,
                    'message': message_text if message_text else '',
                    'attachment': ','.join(attachments),
                    'forward_messages': ','.join(
                        [str(message_data['id']) for message_data in event.raw['object']['message']['fwd_messages']]),
                    'random_id': 0
                })
