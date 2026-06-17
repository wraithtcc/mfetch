#!/usr/bin/env python3
import os
import platform
import socket
import subprocess
import shutil

RESET  = "\033[0m"
BOLD   = "\033[1m"

def ansi256bg(n): return f"\033[48;5;{n}m"

C_LABEL  = BOLD + "\033[38;5;81m"
C_VALUE  = "\033[38;5;253m"
C_ACCENT = BOLD + "\033[38;5;213m"
C_SEP    = "\033[38;5;240m"
C_ART    = "\033[38;5;81m"

def get_distro_info():
    try:
        data = {}
        with open("/etc/os-release") as f:
            for line in f:
                line = line.strip()
                if "=" in line:
                    k, _, v = line.partition("=")
                    data[k] = v.strip('"')
        pretty = data.get("PRETTY_NAME", "Linux")
        id_like = (data.get("ID_LIKE", "") + " " + data.get("ID", "")).lower()
        _id = data.get("ID", "linux").lower()
        for name in ("artix", "arch", "gentoo", "ubuntu", "debian",
                     "fedora", "opensuse", "alpine", "void", "nixos"):
            if name in _id or name in id_like:
                return name, pretty
        return "linux", pretty
    except Exception:
        return "linux", "Linux"

SCRIPT_DIR = "/usr/share/mfetch"

def get_ascii(distro):
    for base in (SCRIPT_DIR, os.path.dirname(os.path.realpath(__file__)), os.getcwd()):
        path = os.path.join(base, "ascii", f"{distro}.txt")
        if os.path.exists(path):
            with open(path) as f:
                return f.read()
    for base in (SCRIPT_DIR, os.path.dirname(os.path.realpath(__file__)), os.getcwd()):
        path = os.path.join(base, "ascii", "linux.txt")
        if os.path.exists(path):
            with open(path) as f:
                return f.read()
    return ""

def get_cpu():
    try:
        with open("/proc/cpuinfo") as f:
            for line in f:
                if "model name" in line:
                    name = line.split(":", 1)[1].strip()
                    for noise in (" CPU", "(R)", "(TM)", "  "):
                        name = name.replace(noise, "")
                    return name.strip()
    except Exception:
        pass
    return platform.processor() or "Unknown"

def get_gpu():
    try:
        out = subprocess.check_output(["lspci"], text=True, stderr=subprocess.DEVNULL)
        for line in out.splitlines():
            low = line.lower()
            if "vga" in low or "3d" in low or "display" in low:
                return line.split(":", 2)[-1].strip()[:60]
    except Exception:
        pass
    try:
        out = subprocess.check_output(["glxinfo", "-B"], text=True, stderr=subprocess.DEVNULL)
        for line in out.splitlines():
            if "OpenGL renderer" in line:
                return line.split(":", 1)[1].strip()[:60]
    except Exception:
        pass
    return None

def get_uptime():
    try:
        with open("/proc/uptime") as f:
            sec = float(f.readline().split()[0])
        d = int(sec // 86400)
        h = int((sec % 86400) // 3600)
        m = int((sec % 3600) // 60)
        parts = []
        if d: parts.append(f"{d}d")
        if h: parts.append(f"{h}h")
        parts.append(f"{m}m")
        return " ".join(parts)
    except Exception:
        return "Unknown"

def get_memory():
    try:
        mem = {}
        with open("/proc/meminfo") as f:
            for line in f:
                k, v = line.split(":")
                mem[k.strip()] = int(v.split()[0])
        total = mem["MemTotal"] // 1024
        avail = mem["MemAvailable"] // 1024
        used  = total - avail
        pct   = int(used / total * 100)
        return f"{used} MiB / {total} MiB ({pct}%)"
    except Exception:
        return "Unknown"

def get_shell():
    shell = os.environ.get("SHELL", "")
    return os.path.basename(shell) if shell else "Unknown"

def get_terminal():
    for var in ("TERM_PROGRAM", "TERMINAL", "TERM"):
        val = os.environ.get(var, "")
        if val and val not in ("xterm", "xterm-256color", "screen",
                               "screen-256color", "tmux-256color"):
            return val
    return os.environ.get("TERM", "Unknown")

def get_de_wm():
    for var in ("XDG_CURRENT_DESKTOP", "DESKTOP_SESSION", "SWAYSOCK", "WAYLAND_DISPLAY"):
        val = os.environ.get(var, "")
        if val:
            if var == "SWAYSOCK":
                return "Sway"
            if var == "WAYLAND_DISPLAY" and not os.environ.get("XDG_CURRENT_DESKTOP"):
                return "Wayland"
            return val.split(":")[0].split("/")[-1]
    return None

def get_packages():
    counts = []
    try:
        if shutil.which("pacman"):
            out = subprocess.check_output(["pacman", "-Qq"], text=True, stderr=subprocess.DEVNULL)
            counts.append(f"{len(out.splitlines())} (pacman)")
        elif shutil.which("dpkg-query"):
            out = subprocess.check_output(["dpkg-query", "-f", "${binary:Package}\n", "-W"],
                                          text=True, stderr=subprocess.DEVNULL)
            counts.append(f"{len(out.splitlines())} (dpkg)")
        elif shutil.which("rpm"):
            out = subprocess.check_output(["rpm", "-qa"], text=True, stderr=subprocess.DEVNULL)
            counts.append(f"{len(out.splitlines())} (rpm)")
        elif shutil.which("qlist"):
            out = subprocess.check_output(["qlist", "-I"], text=True, stderr=subprocess.DEVNULL)
            counts.append(f"{len(out.splitlines())} (portage)")
        elif shutil.which("apk"):
            out = subprocess.check_output(["apk", "list", "--installed"], text=True, stderr=subprocess.DEVNULL)
            counts.append(f"{len(out.splitlines())} (apk)")
    except Exception:
        pass
    try:
        if shutil.which("flatpak"):
            out = subprocess.check_output(["flatpak", "list"], text=True, stderr=subprocess.DEVNULL)
            n = len([l for l in out.splitlines() if l.strip()])
            if n:
                counts.append(f"{n} (flatpak)")
    except Exception:
        pass
    return ", ".join(counts) if counts else "Unknown"

def color_blocks():
    blocks = ""
    for i in range(8):
        blocks += f"{ansi256bg(i)}   {RESET}"
    blocks += "  "
    for i in range(8, 16):
        blocks += f"{ansi256bg(i)}   {RESET}"
    return blocks

def strip_ansi(s):
    import re
    return re.sub(r"\033\[[0-9;]*m", "", s)

def vlen(s):
    return len(strip_ansi(s))

distro_id, distro_pretty = get_distro_info()
hostname = socket.gethostname()
user     = os.getenv("USER") or os.getenv("LOGNAME") or "user"
title    = f"{C_ACCENT}{BOLD}{user}{C_SEP}@{C_ACCENT}{hostname}{RESET}"
sep      = C_SEP + "─" * (len(user) + len(hostname) + 1) + RESET

def row(label, value):
    return f"{C_LABEL}{label}{RESET}{C_SEP}:{RESET} {C_VALUE}{value}{RESET}"

info = [title, sep]
info.append(row("OS",       distro_pretty))
info.append(row("Kernel",   platform.release()))
info.append(row("Arch",     platform.machine()))
info.append(row("Uptime",   get_uptime()))

de_wm = get_de_wm()
if de_wm:
    info.append(row("DE/WM", de_wm))

info.append(row("Shell",    get_shell()))
info.append(row("Terminal", get_terminal()))
info.append(row("CPU",      get_cpu()))

gpu = get_gpu()
if gpu:
    info.append(row("GPU", gpu))

info.append(row("Memory",   get_memory()))
info.append(row("Packages", get_packages()))
info.append("")
info.append(color_blocks())

art_raw   = get_ascii(distro_id)
art_lines = (C_ART + art_raw + RESET).splitlines() if art_raw else []
art_width = max((vlen(l) for l in art_lines), default=0)

rows = max(len(art_lines), len(info))
for i in range(rows):
    left  = art_lines[i] if i < len(art_lines) else ""
    right = info[i]      if i < len(info)       else ""
    pad   = art_width - vlen(left) + 4
    print(f"{left}{' ' * pad}{right}")

print()
