import os

# Set these in Railway project settings

BACKEND_URL = os.environ["BACKEND_URL"] # service activation on website
BACKEND_KEY = os.environ["BACKEND_KEY"] # a key for preventing non auth access

TRIBUTE_ID = int(os.environ["TRIBUTE_ID"]) # your tribute api id
TRIBUTE_HASH = os.environ["TRIBUTE_HASH"] # your tribute api hash
TG_HASH = os.environ["TG_HASH"] # your session hash

CHAT_TRIBUTE = os.environ["CHAT_TRIBUTE"] # tribute
CHAT_ADMIN = int(os.environ["CHAT_ADMIN"]) # admin chat id for error notifications

