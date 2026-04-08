import json, time, sys, asyncio, signal
#from telethon import TelegramClient, StringSession, events # type: ignore
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from backend import send_to_backend
from parser import parse_message, get_message_type, get_send_product_button
from locale import RESPONSE
from env import TRIBUTE_ID, TRIBUTE_HASH, TG_HASH, CHAT_TRIBUTE, CHAT_ADMIN  # type: ignore


client = TelegramClient(StringSession(TG_HASH), TRIBUTE_ID, TRIBUTE_HASH, system_lang_code="en")

# Notify admin and log
def log(text):
    print(text, flush=True)

async def notify_admin(text):
    log(text)
    await client.send_message(CHAT_ADMIN, f"Payment processing error: {text}")


# Get success response text
def create_success_response(reply) -> str:
    # make sure returned lang supported
    lang = reply["lang"] if reply["lang"] in RESPONSE else "en"
    # get product specific answer, if product exists
    if reply.get("product"):
        product = reply["product"] if reply["product"] in RESPONSE[lang] else None            
    else:
        product = None
    # get reply text based on: lang, product    
    return RESPONSE[lang][product or "default"]


# Click "Send Product" button in the message
async def click_send_product(reply) -> bool:
    button = get_send_product_button(reply)
    if button:
        try:
            await button.click()                    
            return True    
        except:
            return False        
    return False


# GET new order from Tribute
@client.on(events.NewMessage(chats=CHAT_TRIBUTE))#, from_users=chat_name))
async def new_message(event):
    # Parse message -> dict
    msg_dict = await parse_message(event.message, client)
    # Log message as json string
    log(f"Message: {json.dumps(msg_dict, ensure_ascii=False)}")
    # Get message type
    mtype = get_message_type(msg_dict)

    # Order: process and reply
    if (mtype == "order"):
        # SEND to server
        reply = await send_to_backend(msg_dict, msg_dict["message"])
        # Server error
        if reply.get("success") is not True:
            await notify_admin("Error activating product at backend")
            return
        # Server success
        success_response = create_success_response(reply)
        # REPLY to the order
        await event.reply(success_response)
        log(f"Re: {success_response}")

    # Button "Send product": click
    elif (mtype == "button"):
        if await click_send_product(event.message):           
            log("Clicked 'Send product'")
        else:
            await notify_admin("Error clicking 'Send product' button")            

    # Confirmation: log
    elif (mtype == "confirmation"):
        log("Tribute confirmed sending product")

# Connect the client to TG, reconnect if disconnected
def main():
    log("Connecting...")
    client.start()
    log("(v) CONNECTED")
    client.run_until_disconnected()
    log("(x) DISCONNECTED")

if __name__ == "__main__":
    main()

# Correct shutdown
def shutdown(sig, frame):
    log("Shutting down gracefully...")
    sys.exit(0)

# Handling duplicated sessions or connections
signal.signal(signal.SIGTERM, shutdown)
signal.signal(signal.SIGINT, shutdown)
