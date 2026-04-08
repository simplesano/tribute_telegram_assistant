from telethon.tl.custom.message import Message
from telethon.tl.types import PeerUser, PeerChat, PeerChannel

"""
Parse Tribute messages

- parse_message             message -> dict
- get_message_type          order / button / confirmation
- get_send_product_button   get 'Send product' button from message

The parsed fields:
    - message       text
    - quoted_text   text of original message (contains order text)
    - quoted_user   author of original message (tg id)
"""

# Get message metadata
async def parse_message(message: Message, client) -> dict:
    msg = {
        "message": message.text or "", # rich text: **bold** [label](link)
        "buttons": "", # list of button [Labels] as text
        "quoted_text": "", # original message text
        "quoted_user": "", # original message autor
    }

    # Get button labels
    buttons = message.buttons or None # get buttons
    if buttons:
        for row in buttons:
            for btn in row:
                msg["buttons"] += "[" + (btn.text or "") + "] " # add [label]

    # If the message is a reply, fetch the original
    if getattr(message, "reply_to", None) and getattr(message.reply_to, "reply_to_msg_id", None):    
        try:
            original = await client.get_messages(
                message.chat_id,
                ids=message.reply_to.reply_to_msg_id
            )

            if original:
                msg["quoted_text"] = original.text or ""

                # Extract author ID
                from_id = getattr(original, "from_id", None)                
                if isinstance(from_id, PeerUser):
                    msg["quoted_user"] = from_id.user_id
                elif isinstance(from_id, PeerChannel):
                    msg["quoted_user"] = from_id.channel_id
                elif isinstance(from_id, PeerChat):
                    msg["quoted_user"] = from_id.chat_id
                elif from_id:
                    msg["quoted_user"] = str(from_id)                    

        except Exception as e:
            msg["quoted_text_error"] = str(e)

    return msg


# Get message type
def get_message_type(msg_dict) -> str:
    text = (msg_dict["message"] or "").lower() # text
    buttons = (msg_dict["buttons"] or "").lower() # button [labels]
    # return message type
    if any(s in text for s in ["🆕", "product order", "заказ товара"]):
        return "order"
    elif any(s in buttons for s in ["send product", "отправить товар"]):
        return "button"    
    elif any(s in text for s in ["great!", "отлично!"]):
        return "confirmation"
    return None
    

# Ger 'Send product' button
def get_send_product_button(message):
    buttons = message.buttons or None # get buttons
    if buttons:
        for row in buttons:
            for btn in row:
                label = (btn.text or "").lower() # get button label
                if any(s in label for s in ["send product", "отправить товар"]):
                    return btn
    return None
