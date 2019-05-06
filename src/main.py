import os
import sys
import json
from pathlib import Path

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.clock import Clock
kivy.require("1.10.1")

import client

from config import USER_CONFIG_DIR, USER_JOIN_FILE
from config import RIGHT_MESSAGE, LEFT_MESSAGE

class ChatHistory(ScrollView):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.layout = GridLayout(cols=1, size_hint_y=None)
        self.add_widget(self.layout)

        self.messages = []

        self.chat_history = GridLayout(cols=2)
        self.scroll_to_point = Label()

        self.layout.add_widget(self.chat_history)
        self.layout.add_widget(self.scroll_to_point)

    def update_chat_history(self, chat_message : str, side : int=LEFT_MESSAGE) -> None:
        self.messages.append((chat_message, side))

        message = Label(markup=True, text=chat_message)
        if side == LEFT_MESSAGE:
            self.chat_history.add_widget(message)
            elabel = Label()
            self.chat_history.add_widget(elabel)
        elif side == RIGHT_MESSAGE:
            elabel = Label()
            self.chat_history.add_widget(elabel)
            self.chat_history.add_widget(message)

        self.layout.height = len(self.messages) * (Label().texture_size[1]) + 15
        # self.chat_history.height = len(self.messages) * 
        for z in self.chat_history.children:
            z.height = (Label().texture_size[1])
            z.text_size = (z.width*0.98, None)

        self.scroll_to(self.scroll_to_point)

class ChatPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 2

        # self.history = Label(height=Window.size[1]*0.9, size_hint_y=None)
        self.history = ChatHistory(height=Window.size[1]*0.9, size_hint_y=None)
        self.add_widget(self.history)

        self.message_input = TextInput(width=Window.size[0]*0.8, size_hint_x=None, multiline=False)
        self.message_input.focus = True
        self.send_btn = Button(text="Send")
        self.send_btn.size_hint_max_y = 30
        # self.send_btn.on_press = self.send_message
        self.send_btn.bind(on_press=self.send_message)

        holder = GridLayout(cols=2)
        holder.add_widget(self.message_input)
        holder.add_widget(self.send_btn)

        self.add_widget(holder)

        Window.bind(on_key_down=self.on_key_down)

    def on_key_down(self, inst, keyb, keyc, text, modif):
        if keyc == 40: # enterkey
            self.send_message(None)
        if keyc == 43: # tab
            if app.settings_open:
                app.close_settings()
                app.settings_open = False
            else:
                app.open_settings()
                app.settings_open = True

    def send_message(self, _) -> None :
        message = self.message_input.text
        self.message_input.text = ""
        if message:
            # send and update_chat_history
            message = f"[color=dd2020]{app.start_page.username_dat}[/color] > {message}"
            app.chat_page.history.update_chat_history(message, RIGHT_MESSAGE)
            Clock.schedule_once(self.focus_async, 0.2)

    def focus_async(self, _):
        self.message_input.focus = True

class InfoPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        self.message = Label(halign="center", valign="middle", font_size=30)
        self.message.bind(width=self.update_text_width)
        self.add_widget(self.message)

    def update_info(self, message):
        self.message.text = message

    def update_text_width(self, *_):
        self.message.text_size = (self.message.width*0.9, None)

class StartPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2

        self.ip_dat = ""
        self.port_dat = "3000"
        self.username_dat = ""

        print("trying to get config")
        joindata = self.get_config()
        if joindata:
            self.ip_dat = joindata["ip"]
            self.port_dat = joindata["port"]
            self.username_dat = joindata["username"]

        self.add_widget(Label(text="IP:"))
        self.ip = TextInput(text=self.ip_dat, multiline=False)
        self.add_widget(self.ip)

        self.add_widget(Label(text="Port:"))
        self.port = TextInput(text=self.port_dat, multiline=False)
        self.add_widget(self.port)

        self.add_widget(Label(text="username:"))
        self.username = TextInput(text=self.username_dat, multiline=False)
        self.add_widget(self.username)

        self.add_widget(Label()) # fill empty cell

        self.joinBtn = Button(text="Join")
        self.joinBtn.bind(on_press=self.joinchat)
        self.add_widget(self.joinBtn)

    def joinchat(self, instance):
        ip = self.ip.text
        port = self.port.text
        username = self.username.text

        self.set_config({
            "ip" : ip,
            "port"   : port,
            "username" : username
        })

        info_message = f"Joining {ip}:{port} as {username}"
        print(info_message)

        app.info_page.update_info(info_message)
        app.screen_manager.current = "Info"

        Clock.schedule_once(self.connect, 1)
    
    def connect(self, _):
        port = int(self.port.text)
        ip = self.ip.text
        username = self.username.text

        if not client.connect(ip, port, username, show_error):
            return

        app.create_chat_page()
        app.screen_manager.current = "Chat"

    def set_config(self, data):
        with open(str(USER_JOIN_FILE), "w+") as file:
            json.dump(data, file)

        SRC_DIR = Path(__file__).parent
        TEMP_DEBUG_JOIN_FILE = (SRC_DIR / "temp/join.json").resolve()

        print("Temp join file", TEMP_DEBUG_JOIN_FILE)
        with open(str(TEMP_DEBUG_JOIN_FILE), "w+") as file:
            json.dump(data, file)

    def get_config(self):
        with open(str(USER_JOIN_FILE), "r") as file:
            print(USER_JOIN_FILE)
            return json.load(file)

class EpicChatApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        self.start_page = StartPage()
        start_screen = Screen(name="Connect")
        start_screen.add_widget(self.start_page)

        self.info_page = InfoPage()
        info_screen = Screen(name="Info")
        info_screen.add_widget(self.info_page)

        self.screen_manager.add_widget(start_screen)
        self.screen_manager.add_widget(info_screen)

        return self.screen_manager
    def create_chat_page(self):
        self.chat_page = ChatPage()
        screen = Screen(name="Chat")
        screen.add_widget(self.chat_page)
        self.screen_manager.add_widget(screen)

    def on_config_change(self, *args, **kw):
        print("config changed", *args, **kw)

def show_error(message):
    app.info_page.update_info(message)
    app.screen_manager.current = "Info"
    Clock.schedule_once(sys.exit, 10)

# if __name__ == "__main__":
app = EpicChatApp()
app.title = "Kivy Epic Chat"

src_path = Path(__file__).parent
icon_path = (src_path / "assets/icon.ico").resolve()
app.icon = str(icon_path)
app.settings_open = False

app.run()
