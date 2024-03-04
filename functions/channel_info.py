import requests
from telethon import TelegramClient
from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.tl.functions.channels import GetMessagesRequest
from telethon.tl.functions.messages import GetHistoryRequest, ReadHistoryRequest
from telethon.utils import InputPeerChannel
from config import api_id, api_hash, phone_number, account

client = TelegramClient(account, api_id, api_hash)
client.connect()


def check_posts(chanel) -> None:
    username = chanel
    dp = client.get_entity(username)
    messages = client.get_message_history(dp, limit=1)


if __name__ == "__main__":
    pass
