# Weather Display

ESP32 based wireless epaper weather display written in MicroPython.

You can find the build video [here on my YouTube channel](https://youtu.be/Qtb_GlVeLOc).

## Setup

The following assumes that you have Python installed and available within a *nix system.

For setting up variables, make a copy of `template.config.py` and save it to `config.py`. This will store your env configs. DO NOT CHECK YOUR ACTUAL VERSION OF `config.py` INTO SOURCE CONTROL.

### Install Deps

```./scripts/install_deps```

### Flash Micropython

```./scripts/flash_firmware```

## Deploy Code

```./scripts/deploy```

## Debugging

Access MicroPython REPL with:

```screen /dev/tty.usbserial-0001 115200```

Access filesystem with RShell:

```rshell -p /dev/tty.usbserial-0001 -b 115200```
