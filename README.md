# mfetch

A minimal, fast system info tool written in Python. No dependencies beyond the standard library.

```
user@hostname
─────────────
OS:       Arch Linux
Kernel:   6.9.3-arch1-1
Arch:     x86_64
Uptime:   2d 4h 17m
DE/WM:    Hyprland
Shell:    zsh
Terminal: kitty
CPU:      Intel Core i7-13700K @ 3.40GHz
GPU:      NVIDIA GeForce RTX 4070
Memory:   6821 MiB / 32000 MiB (21%)
Packages: 1342 (pacman), 4 (flatpak)
▓▓▓ ▓▓▓ ▓▓▓ ▓▓▓ ▓▓▓ ▓▓▓ ▓▓▓ ▓▓▓   ▓▓▓ ▓▓▓ ▓▓▓ ▓▓▓ ▓▓▓ ▓▓▓ ▓▓▓ ▓▓▓
```

## Features

- Distro-specific ASCII art
- Colored output (256-color ANSI)
- Detects: OS, Kernel, Arch, Uptime, DE/WM, Shell, Terminal, CPU, GPU, Memory, Packages
- Package manager support: pacman, dpkg, rpm, portage, apk, flatpak
- GPU detection via `lspci` / `glxinfo`
- Zero dependencies — pure Python 3

## Installation

```bash
git clone https://github.com/larprxlokm/mfetch
cd mfetch
chmod +x mfetch
```

Optionally install system-wide:

```bash
sudo cp mfetch /usr/local/bin/mfetch
sudo cp -r ascii /usr/local/share/mfetch/ascii
```

> If installing system-wide, update `SCRIPT_DIR` in the script or symlink the `ascii/` folder next to the binary.

## Usage

```bash
./mfetch
```

Or if installed to PATH:

```bash
mfetch
```

## ASCII Art

Art files live in `ascii/<distro>.txt`. The filename must match the distro's `ID` field from `/etc/os-release`.

Currently included:

| File | Distro |
|------|--------|
| `arch.txt` | Arch Linux |
| `artix.txt` | Artix Linux |
| `debian.txt` | Debian |
| `ubuntu.txt` | Ubuntu |
| `fedora.txt` | Fedora |
| `gentoo.txt` | Gentoo |
| `opensuse.txt` | openSUSE |
| `alpine.txt` | Alpine Linux |
| `void.txt` | Void Linux |
| `nixos.txt` | NixOS |
| `linux.txt` | Fallback |

To add a new distro, drop a plain text ASCII art file in the `ascii/` directory named after the distro's `ID` value.

## Supported Distros

Detection works on any distro with `/etc/os-release`. The ASCII art falls back to `linux.txt` if no matching file is found.

## Requirements

- Python 3.6+
- Linux
- `lspci` (optional, for GPU detection — usually from `pciutils`)
- `glxinfo` (optional, GPU fallback — from `mesa-utils`)

## License

MIT
