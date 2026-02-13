# ba_meta require api 9
# ba_meta export babase.Plugin

import babase
from babase import Plugin
from bascenev1 import get_foreground_host_activity

class AutoChatPlugin(Plugin):
    def __init__(self):
        babase.apptimer(0.5, self._hook_chat, repeat=True)

    def _hook_chat(self):
        activity = get_foreground_host_activity()
        if not hasattr(activity, "chat_messages"):
            return

        messages = list(activity.chat_messages)
        for m in messages[-5:]:
            text = m["text"].lower()
            if getattr(m, "_replied", False):
                continue

            if text == "cu":
                self._send_chat("h")
                m._replied = True

            elif text == "fr":
                self._send_chat("u")
                m._replied = True

    def _send_chat(self, msg: str):
        activity = get_foreground_host_activity()
        if activity:
            activity.send_chat_message(msg)
            babase.screenmessage(f"AutoChat: {msg}", color=(0, 1, 0))