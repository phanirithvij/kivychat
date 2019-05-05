import os
import json

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
kivy.require("1.10.1")

from config import USER_CONFIG_DIR, USER_JOIN_FILE

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

    def set_config(self, data):
        with open(USER_JOIN_FILE, "w+") as file:
            json.dump(data, file)

        SRC_DIR = os.path.dirname(__file__)
        TEMP_DEBUG_JOIN_FILE = os.path.join(SRC_DIR, "temp", "join.json")
        TEMP_DEBUG_JOIN_FILE = os.path.abspath(TEMP_DEBUG_JOIN_FILE)

        print("Temp join file", TEMP_DEBUG_JOIN_FILE)
        with open(TEMP_DEBUG_JOIN_FILE, "w+") as file:
            json.dump(data, file)

    def get_config(self):
        with open(USER_JOIN_FILE, "r") as file:
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

# if __name__ == "__main__":
app = EpicChatApp()
app.title = "Kivy Epic Chat"
app.icon = os.path.abspath("assets/icon.ico") # not working
app.run()
