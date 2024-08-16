# ServeM

[![pypi](https://img.shields.io/pypi/v/servem.svg)](https://pypi.org/project/servem/)
[![Release](https://img.shields.io/github/release/bruttazz/servem.svg)](https://github.com/bruttazz/servem/releases/latest)
[![Release](https://github.com/bruttazz/servem/actions/workflows/release.yml/badge.svg)](https://github.com/bRuttaZz/servem/actions/workflows/release.yml)



A simple screen sharing server for modern GNU/LINUX desktops!

## Installation

**Dependencies**

- A GNU/Linux desktop with GLib availability and the python 'gi' (GObject Introspection) (usually almost all popular distros came with it)
- Gstreamer and jpeg encoders installed. If not available execute the following commands
```sh
# for debian based distros
sudo apt-get install python3-gi gstreamer1.0-tools gstreamer1.0-plugins-base gstreamer1.0-plugins-good

# for fedora / ..
sudo dnf install python3-gi gstreamer1 gstreamer1-plugins-base gstreamer1-plugins-good

# arch linux
sudo pacman -S python-gobject gstreamer
```
- Pyhon dbus package.
```sh
pip install dbus-python
# prefer to install using system package manager
```


Lastly, the service is packaged as a Python CLI that can be installed with,
```sh
pip3 install servem
```


## Usage

The tool is meant to be used as a command line utility. After installation of the package one can follow the bellow mentioned commands to get started
```sh
# to get usage details
servem --help

# spinning a simple server (with cursor position)
servem --cursor
```


## The Story & The Name

BTW, this repo was not originally intended to be a Python one... (poor me, lacking time and expertise in GLib conventions).
Anyway, hopefully, it's here and it's working.

Initially, I set out to create a C-based HTTP server purely for educational purposes :) So I named it **Cerve** (substituting the `s` in `serve` with `c`—pure brilliance!).
During development, I happened to watch [this video](https://laotzu.ftp.acc.umu.se/pub/debian-meetings/2024/DebConf24/debconf24-386-learnings-from-creating-an-input-method-for-gnulinux-from-a-product-perspective.av1.webm)
by a friend, [Subin](https://x.com/subinsiby). It was a nice one, and the thing was, he was using Jitsi Meet to share his screen with his peer's computer and from there to a presentation screen using an HDMI port (as his MacBook running Asahi doesn't have an HDMI port).
And, as usual, due to some network issues, his Jitsi Meet session got disconnected midway. (Anyway, the presentation went well.)

So I thought, what about creating an HTTP server that shares my computer screen with my local peers, so that they can access it in a more reliable and low-latency fashion in such scenarios? One could even use it to share their desktop with others when no screen-sharing facility is available.
I decided to build something like that in C and changed the project's initial name from Cerve to CerveM (this one sounds like the word 'sarvam' in Malayalam, meaning 'everything').
But after dealing with a bunch of Wayland issues, Linux display portals, and some convention-related matters, and due to my limited time (as I was on a tight schedule), I decided to drop the project and stick with a simple HTTP server instead.

Anyway, the feature I was thinking about seemed good. So I built this Python script that does the job during my train journey back to Ernakulam.
And that's what it is—a simple script for a simple hack.
