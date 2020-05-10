from libpurecool.dyson import DysonAccount

import time

USER = "<user>"
PASS = "<pass>"
LANG = "GB"

def print_new_attributes():
    print("Humidifier state: " + device.state.humidifier_state)
    print("Humidifier auto mode: " + device.state.humidifier_auto)
    print("Humidity target: " + device.state.humidity_target)

def wait():
    print("Waiting for 10 seconds...")
    time.sleep(10)

dyson_account = DysonAccount(USER, PASS, LANG)
logged = dyson_account.login()

devices = dyson_account.devices()
connected = devices[0].auto_connect()
device = devices[0]

print("Running tests...")
print_new_attributes()

print("Enabling humidifier")
device.enable_humidifier()
print_new_attributes()
wait()

print("Disabling humidifier")
device.disable_humidifier()
print_new_attributes()
wait()

print("Enabling humidifier auto mode")
device.enable_humidifier_auto()
print_new_attributes()
wait()

print("Disabling humidifier auto mode")
device.disable_humidifier_auto()
print_new_attributes()
wait()

print("Setting humidity target")
device.set_humidity_target(70)
print_new_attributes()