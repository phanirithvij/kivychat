# Learnings from this project

Video series followed: [sentdex](https://www.youtube.com/playlist?list=PLQVvvaa0QuDfwnDTZWw8H3hN_VRQfq8rF)

Tools : kivy, python

## Setup

Install python, pip etc..
Install kivy by following [this](https://kivy.org/doc/stable/installation/installation-windows.html)

```shell
python -m pip install --upgrade pip wheel setuptools
```

Deps
```shell
python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew
```

Optional
```shell
python -m pip install kivy.deps.angle
python -m pip install kivy.deps.gstreamer
```

Finally
```shell
python -m pip install kivy
```

## New stuff
+ Getting Relative path in python
    - **Title** : Get the same file relative to the source dir independent of the execution directory
    eg:
        ```shell
        #from ./
        python src/main.py
        #or from ./src/
        python ../src/main.py
        #or from ~
        pyhton /path/to/src/main.py
        #or from ./src/
        python ./main.py
        ```
    Should all access the same file inside like relative imports.
    - **Solution** :
        ```python
        SRC_DIR = os.path.dirname(__file__)
        TEMP_DEBUG_JOIN_FILE = os.path.join(SRC_DIR, "temp", "join.json")
        TEMP_DEBUG_JOIN_FILE = os.path.abspath(TEMP_DEBUG_JOIN_FILE)
        # finally gives src/temp/join.json
        ```
        OR
        ```python
        from pathlib import Path
        src_path = Path(__file__).parent
        icon_path = (src_path / "assets/icon.ico").resolve()
        ```
    - **Link** : [this stackoverflow post](https://stackoverflow.com/a/40416154/8608146)


## Bugs


## Mistakes
+ Changing App icon in Kivy
    - **Issue** : Changing the kivy app icon didn't work
    - **State** : unresolved
    - **Solution** : Nothing
