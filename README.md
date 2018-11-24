# Dyson Pure Cool Python library

## Fork of Charles Blonde's libpurecoolink library: [link](https://github.com/CharlesBlonde/libpurecoollink)

This Python 3.4+ library allow you to control [Dyson fan/purifier devices](http://www.dyson.com/air-treatment/purifiers/dyson-pure-hot-cool-link.aspx) and [Dyson 360 Eye robot vacuum device](http://www.dyson.com/vacuum-cleaners/robot/dyson-360-eye.aspx).

[official documentation](http://libpurecoollink.readthedocs.io)

## Status

This library is becoming quite stable but backward compatibility is not yet guaranteed.

## Full documentation

http://libpurecoollink.readthedocs.io

### Supported devices

* Dyson pure cool tower (TP04)
* Dyson pure cool desk (DP04)
* Dyson pure cool link devices (Tower and Desk)
* Dyson pure cool+hot devices
* Dyson 360 Eye robot vacuum

## Features

The following feature are supported:

* Purifier/fan devices
    * Connect to the device using discovery or manually with IP Address
    * Turn on/off
    * Set speed
    * Turn on/off oscillation
    * Set Auto mode
    * Set night mode
    * Set sleep timer
    * Set Air Quality target (Normal, High, Better)
    * Enable/disable standby monitoring (the device continue to update sensors when in standby)
    * Reset filter life
    * Adjust oscillation angle (TP04/DP04)
* Cool+Hot purifier/fan devices
    * Set heat mode
    * Set heat target
    * Set fan focus mode
* 360 Eye device (robot vacuum)
    * Set power mode (Quiet/Max)
    * Start cleaning
    * Pause cleaning
    * Resume cleaning
    * Abort cleaning

The following sensors are available for fan/purifier devices:

* Humidity
* Temperature in Kelvin
* Dust (unknown metric)
* Air quality (unknown metric)

## Quick start

Please read [official documentation](http://libpurecoollink.readthedocs.io)

## How it's work

Dyson devices use many different protocols in order to work:

* HTTPS to Dyson API in order to get devices informations (credentials, historical data, etc ...)
* MDNS to discover devices on the local network
* MQTT (with auth) to get device status and send commands

To my knowledge, no public technical information about API/MQTT are available so all the work is done by testing and a lot of properties are unknown to me at this time.

This library come with a modified version of [Zeroconf](https://github.com/jstasiak/python-zeroconf) because Dyson MDNS implementation is not valid.

This [documentation](https://github.com/shadowwa/Dyson-MQTT2RRD) help me to understand some of return values.

## Work to do

* Better protocol understanding
* Better technical documentation on how it is working
* Get historical data from the API (air quality, etc ...)
