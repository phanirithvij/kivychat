import os
import json

USER_CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".kivy_chat")
USER_CONFIG_DIR = os.path.abspath(USER_CONFIG_DIR)
USER_JOIN_FILE = os.path.join(USER_CONFIG_DIR, "join.json")
USER_JOIN_FILE = os.path.abspath(USER_JOIN_FILE)

def setup_dirs():
    if not os.path.isdir(USER_CONFIG_DIR):
        os.makedirs(USER_CONFIG_DIR)

    if not os.path.isfile(USER_JOIN_FILE):
        with open(USER_JOIN_FILE, "w+") as file:
            json.dump({}, file)

setup_dirs()
