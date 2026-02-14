# BombSquad Auto Message Plugin
# Clean Version - No Hidden Characters

from __future__ import annotations

import babase
import bauiv1 as bui
from bauiv1lib import chatmessage as CM


# =========================
# Helper: Clean Text
# =========================
def clean_text(text: str) -> str:
    zero_chars = [
        "\u200b",
        "\u200c",
        "\u200d",
        "\ufeff",
    ]
    for z in zero_chars:
        text = text.replace(z, "")
    return text.strip()


# =========================
# Auto Message System
# =========================
class AutoMessenger:

    def __init__(self):
        self.enabled = False
        self.interval = 3.0
        self.message = "Hello!"
        self.timer: babase.AppTimer | None = None

    # Start
    def start(self):
        if self.enabled:
            bui.screenmessage("Auto already running", color=(1, 1, 0))
            return

        self.enabled = True
        bui.screenmessage("Auto Message Started", color=(0, 1, 0))
        self._loop()

    # Stop
    def stop(self):
        self.enabled = False
        bui.screenmessage("Auto Message Stopped", color=(1, 0, 0))

    # Loop
    def _loop(self):
        if not self.enabled:
            return

        try:
            msg = clean_text(self.message)
            CM(msg)
        except Exception as e:
            bui.screenmessage(f"Error: {e}", color=(1, 0, 0))

        self.timer = babase.AppTimer(self.interval, self._loop)

    # Setters
    def set_message(self, text: str):
        self.message = clean_text(text)
        bui.screenmessage(f"Msg: {self.message}", color=(0, 1, 1))

    def set_interval(self, seconds: float):
        self.interval = max(0.5, seconds)
        bui.screenmessage(f"Interval: {self.interval}", color=(0, 1, 1))


# Global instance
auto = AutoMessenger()


# =========================
# Chat Command Hook
# =========================
def handle_command(msg: str):
    if not msg.startswith("/auto"):
        return False

    parts = msg.split(" ", 2)

    if len(parts) < 2:
        bui.screenmessage("/auto start | stop | msg | time")
        return True

    cmd = parts[1].lower()

    if cmd == "start":
        auto.start()

    elif cmd == "stop":
        auto.stop()

    elif cmd == "msg" and len(parts) >= 3:
        auto.set_message(parts[2])

    elif cmd == "time" and len(parts) >= 3:
        try:
            auto.set_interval(float(parts[2]))
        except Exception:
            bui.screenmessage("Invalid time")

    else:
        bui.screenmessage("Unknown command")

    return True


# =========================
# Plugin Entry
# =========================
class Plugin(babase.Plugin):

    def on_app_running(self) -> None:
        old = bui.chatmessage

        def new_chat(msg: str, *args, **kwargs):
            if handle_command(msg):
                return
            return old(msg, *args, **kwargs)

        bui.chatmessage = new_chat