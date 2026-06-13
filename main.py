#!/usr/bin/env python3

import os
import platform
import socket
import subprocess
import shutil

def get_distro():
    try:
        with open("/etc/os-release") as f:
            data = f.read().lower()

        if "artix" in data:
            return "artix"
        if "arch" in data:
            return "arch"
        if "gentoo" in data:
            return "gentoo"
        if "ubuntu" in data:
            return "ubuntu"
        if "debian" in data:
            return "debian"
        if "fedora" in data:
            return "fedora"
        if "opensuse" in data:
            return "opensuse"
    except:
        pass

    return "linux"

def get_ascii(distro):
    path = f"ascii/{distro}.txt"
    try:
        with open(path, "r") as f:
            return f.read()
    except FileNotFoundError:
        with open("ascii/linux.txt", "r") as f:
            return f.read()


def get_cpu():
    try:
        with open("/proc/cpuinfo") as f:
            for line in f:
                if "model name" in line:
                    return line.split(":", 1)[1].strip()
    except:
        pass
    return "Unknown"

def get_uptime():
    try:
        with open("/proc/uptime") as f:
            sec = float(f.readline().split()[0])

        d = int(sec // 86400)
        h = int((sec % 86400) // 3600)
        m = int((sec % 3600) // 60)

        return f"{d}d {h}h {m}m"
    except:
        return "Unknown"

def get_memory():
    try:
        mem = {}
        with open("/proc/meminfo") as f:
            for line in f:
                k, v = line.split(":")
                mem[k] = int(v.split()[0])

        total = mem["MemTotal"] // 1024
        avail = mem["MemAvailable"] // 1024
        used = total - avail

        return f"{used} MiB / {total} MiB"
    except:
        return "Unknown"

def get_shell():
    return os.environ.get("SHELL", "Unknown")


def get_packages():
    try:
        # Arch / Artix
        if shutil.which("pacman"):
            out = subprocess.check_output(["pacman", "-Q"], text=True)
            return f"{len(out.splitlines())} (pacman)"

        # Debian / Ubuntu
        if shutil.which("dpkg"):
            out = subprocess.check_output(["dpkg", "--get-selections"], text=True)
            return f"{len(out.splitlines())} (dpkg)"

        # Gentoo
        if shutil.which("qlist"):
            out = subprocess.check_output(["qlist", "-I"], text=True)
            return f"{len(out.splitlines())} (portage)"

    except:
        pass

    return "Unknown"


hostname = socket.gethostname()
user = os.getenv("USER", "user")

info = [
    f"{user}@{hostname}",
    "-" * (len(user) + len(hostname) + 1),
    f"OS: {platform.system()} {platform.release()}",
    f"Kernel: {platform.release()}",
    f"Architecture: {platform.machine()}",
    f"CPU: {get_cpu()}",
    f"Packages: {get_packages()}",
    f"Memory: {get_memory()}",
    f"Uptime: {get_uptime()}",
    f"Shell: {get_shell()}",
]


distro = get_distro()
art = get_ascii(distro)

art_lines = art.splitlines()
width = max(len(line) for line in art_lines)

for i in range(max(len(art_lines), len(info))):
    left = art_lines[i] if i < len(art_lines) else ""
    right = info[i] if i < len(info) else ""
    print(f"{left:<{width + 5}} {right}")
