import os
import json

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
kivy.require("1.10.1")

from config import USER_CONFIG_DIR, USER_JOIN_FILE

def init_conf():
    pass

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

        print(f"Trying to join {ip}:{port} as {username}")
        self.set_config({
            "ip" : ip,
            "port"   : port,
            "username" : username
        })

    def set_config(self, data):
        with open(USER_JOIN_FILE, "w+") as file:
            json.dump(data, file)
    def get_config(self):
        with open(USER_JOIN_FILE, "r") as file:
            print(USER_JOIN_FILE)
            return json.load(file)

class EpicChatApp(App):
    def build(self):
        return StartPage()

if __name__ == "__main__":
    init_conf()
    app = EpicChatApp()
    app.title = "Kivy Epic Chat"
    app.icon = os.path.abspath("assets/icon.ico") # not working
    app.run()
