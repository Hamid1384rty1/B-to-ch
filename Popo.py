# -*- coding: utf-8 -*-
# Jojo Auto Reply Advanced Version for BombSquad

import bs
import _ba
import time

# ==============================
# SETTINGS
# ==============================

AUTO_REPLY_ENABLED = True

# Any word here will trigger a reply if it appears inside a message
TRIGGERS = {
    "cu": "h",
    "hi": "hello",
    "ping": "pong"
}

# Cooldown to prevent spam (seconds)
REPLY_COOLDOWN = 3

last_reply_time = 0


# ==============================
# CHECK MESSAGE FUNCTION
# ==============================

def should_reply(message):
    global last_reply_time
    
    if not AUTO_REPLY_ENABLED:
        return None

    if not message:
        return None

    now = time.time()
    if now - last_reply_time < REPLY_COOLDOWN:
        return None

    message_lower = message.lower()

    for trigger, reply in TRIGGERS.items():
        if trigger.lower() in message_lower:
            last_reply_time = now
            return reply

    return None


# ==============================
# CHAT HOOK
# ==============================

_original_chat = _ba.chatmessage


def new_chat(message, clients=None, sender_override=None):
    result = _original_chat(message, clients, sender_override)

    reply = should_reply(message)

    if reply:
        _ba.chatmessage(reply)

    return result


_ba.chatmessage = new_chat
