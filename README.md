# Webremote (project)

## Section
- [Description](#description)
- [Requirements](#requirements)
- [Usage](#usage)
- [Plans](#plans)
- [Misc](#misc)


## Description

Project to control various IoT devices in the house (WiFi) and the RPi server (DNS, fileserver, entertainment center, etc).


## Requirements

You can install required modules with either command below

For virtaul enviroment
```
python3 -m pip install -r requirements.txt
```

Without virtual enviroment
```
pip install -r requirements.txt
```


## Usage

1. At present configuration is done manually editing **config.ini*. You can change ip, port and debug options among others.
2. Start with `python3 main.py` and your browser will open at the specified ip port specified in previous step.
3. You will need to register a user on first run to get to the dashboard.


## Plans

- Themes
- Cusomtize Quick buttons dynically
- Ability to add more devices
- Get device details

Planning to work on this and make it public, kinda like a template Smart Home hub.
Examples for powering on/off devices are for Sonoff Basic smart plugs flashed with Tasmota firmware.
![image](https://github.com/zdssdavidb/Webremote/assets/58611751/c500e8af-9cf0-4eea-b590-d1427265c0de)
[Tasmota](https://tasmota.github.io/docs/)


## Misc

Can check the journal (if Debug=off) using command: **journalctl -u flask -n 25**
