from telethon import TelegramClient
from telethon.sessions import StringSession

# Initiate a Telethon session and copy session hash for authorisation on Railway
# ! Railway does not support SSH

TG_ID = 0
TG_HASH = ""

with TelegramClient(StringSession(), TG_ID, TG_HASH) as client:
    print("SESSION:")
    print(client.session.save())