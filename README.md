# (LKBBD) Linux Key-Binds By Device
## Create and use custom keybinds in linux so individual input devices can have different sets of keybinds
___
### Usage:
```shell
lkbbd [<path/to/config/file>]
```
___
### Download Release:
- Download the latest [Release](https://github.com/Vawlpe/LinuxKeyBindsByDevice/releases)
- Untar to a new directory in whatever system-wide accessible location you want (anything in your PATH env var)
- ***Follow [Configuration](#configuration) steps bellow***
## OR
### Manual Build:
- ```shell
    git clone https://github.com/Vawlpe/LinuxKeyBindsByDevice.git
    pip install -r requirements.txt
    gcc -o lkbbd -Wall lkbbd.c
    ```
- Copy `lkbdd`, `main.py`, `cfg.py`, and `kbeIntercepter.py`
to a new directory in whatever system-wide accessible location you want (anything in your PATH env var)
___
### Configuration
- Make sure you are in lkbdd directory
- Run `sudo chown <USERNAME>:input ./lkbbd` to modify group ownership of the lkbbd binary to `input`,
allowing it to read and write input files without root perms
- Run `sudo chmod g+s ./lkbbd` to enable setuid bit for group on lkbbd binary 
to allow privelege escalation to `input` group
- Create a valid configuration file:    
    - Create a config file at `~/.config/lkbbd.json` with content similar to this:
      ```json
      {
        "/dev/input/by-id/usb-USB_KB_USB_KB-event-kbd" : {
          "96" : {
              "run": "alacritty",
              "blockThread": "False"
            },
          "keepDefaultBehaviour": "False"
        }
      }
      ```
    ***OR***
    - Run `lkbbd` to begin config generation wizard
- Add the following line to your `.xinitrc` file to run `lkbbd` at startup:
    ```shell
    exec lkbbd
    ```
