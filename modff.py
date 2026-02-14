from babase import (
    clipboard_is_supported as CIS,
    clipboard_get_text as CGT,
    clipboard_has_text as CHT,
    Plugin
)
from bauiv1 import (
    get_special_widget as gsw,
    containerwidget as cw,
    screenmessage as push,
    checkboxwidget as chk,
    scrollwidget as sw,
    buttonwidget as bw,
    SpecialChar as sc,
    textwidget as tw,
    checkboxwidget as cb,
    gettexture as gt,
    apptimer as teck,
    getsound as gs,
    UIScale as uis,
    charstr as cs,
    app as APP,
    Call
)
from bascenev1 import (
    get_chat_messages as GCM,
    chatmessage as CM,
    get_connection_to_host_info_2 as get_connection_info,
    connect_to_party as original_connect,
    disconnect_from_host as original_disconnect,
    get_foreground_host_activity
)
from _babase import get_string_width as strw
from datetime import datetime as DT
from bauiv1lib import party
from babase import apptimer as teck
from bauiv1lib.popup import PopupWindow, PopupMenu
from typing import Sequence, Tuple, Optional, Callable
from bauiv1lib.colorpicker import ColorPicker
import random
from bauiv1lib.party import PartyWindow
from bauiv1lib.ingamemenu import InGameMenuWindow
import math
import json
import os
import socket
import threading
import time
import re
import bascenev1 as bs
import bauiv1 as bui
import _babase
import babase
import bascenev1 as bs
import bauiv1 as bui

# --- Import های جدید برای Account Switcher ---
from bauiv1lib.confirm import ConfirmWindow
from bauiv1lib.account.settings import AccountSettingsWindow
from os import listdir, path, mkdir, remove
from shutil import copy, rmtree
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional


# ba_meta require api 9
# ba_meta export babase.Plugin

from __future__ import annotations

import babase
import bauiv1 as bui
from bauiv1lib import chatmessage as CM


# =========================
# Text Cleaner (No Hidden Characters)
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
# Auto Messenger System
# =========================
class AutoMessenger:

    def __init__(self):
        self.enabled = False
        self.interval = 3.0
        self.message = "Hello!"
        self.timer: babase.AppTimer | None = None

    def start(self):
        if self.enabled:
            bui.screenmessage("Auto already running", color=(1, 1, 0))
            return

        self.enabled = True
        bui.screenmessage("Auto Message Started", color=(0, 1, 0))
        self._loop()

    def stop(self):
        self.enabled = False
        bui.screenmessage("Auto Message Stopped", color=(1, 0, 0))

    def _loop(self):
        if not self.enabled:
            return

        try:
            msg = clean_text(self.message)
            CM(msg)
        except Exception as e:
            bui.screenmessage(f"Error: {e}", color=(1, 0, 0))

        self.timer = babase.AppTimer(self.interval, self._loop)

    def set_message(self, text: str):
        self.message = clean_text(text)
        bui.screenmessage(f"Msg: {self.message}", color=(0, 1, 1))

    def set_interval(self, seconds: float):
        self.interval = max(0.5, seconds)
        bui.screenmessage(f"Interval: {self.interval}", color=(0, 1, 1))


auto = AutoMessenger()


# =========================
# Chat Command Handler
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
# Plugin Main Class
# =========================
class ModFFPlugin(babase.Plugin):

    def on_app_running(self) -> None:
        bui.screenmessage("modff by Hamid Loaded ✅", color=(0, 1, 0))

        old_chat = bui.chatmessage

        def new_chat(msg: str, *args, **kwargs):
            if handle_command(msg):
                return
            return old_chat(msg, *args, **kwargs)

        bui.chatmessage = new_chat
