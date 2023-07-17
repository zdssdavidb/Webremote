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

pip install flask

## Features config
touch /var/www/html/{project_name}/status      # for power switching for devices
touch /var/www/html/{project_name}/color      # for storing current LED color


## Usage

1. Configure interface and port in **main.py**
2. Start flask web server with **python3 main.py**
3. Use browser to navigate to server address and register new user.
4. Login and start using.





## Plans

Planning to work on this and make it public, kinda like a template Smart Home hub.
Examples for powering on/off devices are for Sonoff Basic smart plugs flashed with Tasmota firmware.
![image](https://github.com/zdssdavidb/Webremote/assets/58611751/c500e8af-9cf0-4eea-b590-d1427265c0de)
[Tasmota](https://tasmota.github.io/docs/)







## Misc

Can check the journal (if Debug=off) using command: **journalctl -u flask -n 25**
