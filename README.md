# Project Lappland
Python script to help you run GNU/Linux distributions on Termux without root.
Fork of https://github.com/YadominJinta/atilo.

[简体中文](https://github.com/YadominJinta/atilo/blob/master/CN/README_CN.md)

## Installation

WIP

## Usage

``` bash
lappland [Command] [Argument]
```

|Command|Meaning                   |
|:-----:|:------------------------:|
|images |list available images     |
|remove |remove a local image      |
|pull   |pull a remote image       |
|run    |start a local image       |
|clean  |clean temporary files     |
|help   |show detailed help message|

## Supported distributions

| Distribution  | aarch64 |  arm  | x86_64 | i686  |
| ------------- | :-----: | :---: | :----: | :---: |
| Alpine        |    √    |   √   |   √    |   √   |
| CentOS        |    √    |   ×   |   √    |   ×   |
| Debian        |    √    |   √   |   √    |   √   |
| Fedora        |    √    |   √   |   √    |   ×   |
| Kali          |    √    |   √   |   √    |   √   |
| openSUSE      |    √    |   √   |   ×    |   ×   |
| Ubuntu        |    √    |   √   |   √    |   √   |

## GUI

[Using GUI on Termux (X11 method)](https://ivonblog.com/en-us/posts/termux-x11/)

# See also

**[EXALAB/AnLinux-App](https://github.com/EXALAB/AnLinux-App)**: APP to help install Linux on termux.

**[YadominJinta/atilo](https://github.com/YadominJinta/atilo/)**: Linux installer for Termux<br>

**[sdrausty/TermuxArch](https://github.com/sdrausty/TermuxArch)**: Arch install script

**[Neo-Oli/termux-ubuntu](https://github.com/Neo-Oli/termux-ubuntu)**: Ubuntu chroot on termux

**[Hax4us/Nethunter-In-Termux](https://github.com/Hax4us/Nethunter-In-Termux)**: Install Kali nethunter (Kali Linux) in your termux application without root access

**[nmilosev/termux-fedora](https://github.com/nmilosev/termux-fedora)**: A script to install a Fedora chroot into Termux

**[sp4rkie/debian-on-termux](https://github.com/sp4rkie/debian-on-termux)**: Install Debian 9 (stretch) on your Android smartphone

**[Hax4us/TermuxAlpine](https://github.com/Hax4us/TermuxAlpine)**: Use TermuxAlpine.sh calling to install Alpine Linux in Termux on Android
