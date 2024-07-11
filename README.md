# ATTENTION!
This project has **NOT** been finished. It is still **WORKING IN PROGRESS** and can't be used.

I'm re-writing the whole program, and it might take some time.

# atLAs
atLAs is a Python script that helps you run and manage GNU/Linux distributions on Termux without root.

## Features
* Run, manage and pack your distributions just like managing containers
* Use multiple mirrors, custom links
* Run and deploy in a single line
* No root access is required thanks to `proot`

## Installation
WIP

## Usage

``` bash
atlas [Command] [Argument]
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
WIP

## GUI

[Using GUI on Termux (X11 method)](https://ivonblog.com/en-us/posts/termux-x11/)

# Credits
This program can't be made without these free and open-source projects:

**[YadominJinta/atilo](https://github.com/YadominJinta/atilo/)**: Linux installer for Termux

**[termux/proot-distro](https://github.com/termux/proot-distro)**: An utility for managing installations of the Linux distributions in Termux. 

# See also

**[EXALAB/AnLinux-App](https://github.com/EXALAB/AnLinux-App)**: APP to help install Linux on termux.

**[sdrausty/TermuxArch](https://github.com/sdrausty/TermuxArch)**: Arch install script

**[Neo-Oli/termux-ubuntu](https://github.com/Neo-Oli/termux-ubuntu)**: Ubuntu chroot on termux

**[Hax4us/Nethunter-In-Termux](https://github.com/Hax4us/Nethunter-In-Termux)**: Install Kali nethunter (Kali Linux) in your termux application without root access

**[nmilosev/termux-fedora](https://github.com/nmilosev/termux-fedora)**: A script to install a Fedora chroot into Termux

**[sp4rkie/debian-on-termux](https://github.com/sp4rkie/debian-on-termux)**: Install Debian 9 (stretch) on your Android smartphone

**[Hax4us/TermuxAlpine](https://github.com/Hax4us/TermuxAlpine)**: Use TermuxAlpine.sh calling to install Alpine Linux in Termux on Android

## License
GPL-3.0