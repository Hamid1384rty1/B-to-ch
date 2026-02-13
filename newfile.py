# auto_chat_reply.py
# Put inside BombSquad mods folder

from __future__ import annotations

import bascenev1 as bs
import babase


class AutoChatPlugin(babase.Plugin):
    def on_app_running(self) -> None:
        # هوک کردن تابع چت
        original_chat = bs.chatmessage

        def chat_interceptor(msg: str, clients: list[int] | None = None):
            text = msg.strip().lower()

            # پاسخ‌های خودکار
            if text == "cu":
                original_chat("h")
            elif text == "fr":
                original_chat("u")

            # اجرای پیام اصلی
            original_chat(msg, clients)

        bs.chatmessage = chat_interceptor

        bs.chatmessage("Auto Chat Reply Mod Loaded ✅")