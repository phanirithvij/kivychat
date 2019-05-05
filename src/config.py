import os
import json
from pathlib import Path

# USER_CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".kivy_chat")
# USER_CONFIG_DIR = os.path.abspath(USER_CONFIG_DIR)
USER_CONFIG_DIR = (Path.home() / ".kivy_chat").resolve()
USER_JOIN_FILE = (Path(USER_CONFIG_DIR) / "join.json")

def setup_dirs():
    if not Path(USER_CONFIG_DIR).is_dir():
        os.makedirs(str(USER_CONFIG_DIR))

    if not Path(USER_JOIN_FILE).is_file():
        with open(str(USER_JOIN_FILE), "w+") as file:
            json.dump({}, file)

setup_dirs()
