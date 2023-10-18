import vk_api
import os
import json

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

                        match attachment_type:
                            case 'photo':
                                attachment_id = attachment[attachment_type]['id']
                                owner_id = attachment[attachment_type]['owner_id']

                                access_key = attachment[attachment_type]['access_key']

                                attachments.append(f"{attachment_type}{owner_id}_{attachment_id}_{access_key}")

                            case 'audio' | 'video':
                                attachment_id = attachment[attachment_type]['id']
                                owner_id = attachment[attachment_type]['owner_id']

                                attachments.append(f"{attachment_type}{owner_id}_{attachment_id}")

                            case 'link':
                                attachments.append(f"{attachment[attachment_type]['url']}")

                sender_id = event.raw['object']['message']['from_id']

                message_text = event.raw['object']['message']['text']

                send_values = {
                    'peer_id': sender_id,
                    'message': message_text if message_text else '',
                    'attachment': ','.join(attachments),
                    'random_id': 0
                }

                if 'reply_message' in event.raw['object']['message']:
                    send_values['reply_to'] = event.raw['object']['message']['reply_message']['id']

                if event.raw['object']['message']['fwd_messages']:
                    send_values['forward_messages'] = ','.join(
                        [str(message_data['id']) for message_data in event.raw['object']['message']['fwd_messages']])

                self.session.method("messages.send", send_values)
