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

## Bugs


## Mistakes
+ Changing App icon
    - **Issue** : Changing the kivy app icon didn't work
    - **State** : unresolved
    - **Solution** : Nothing