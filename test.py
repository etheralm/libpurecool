import time

from libpurecool.const import FanSpeed, HeatTarget
from libpurecool.dyson import DysonAccount
from libpurecool.dyson_pure_state_v2 import DysonEnvironmentalSensorV2State

EMAIL = '<email>'
PASSWORD = '<password>'
DEVICE_NUM = 0

logged_env_message = False


def on_message(msg):
    # Message received
    global logged_env_message
    if isinstance(msg, DysonEnvironmentalSensorV2State):
        if logged_env_message is False:
            print(msg)
            logged_env_message = True
    else:
        print(msg)


dyson_account = DysonAccount(EMAIL, PASSWORD, 'GB')
logged = dyson_account.login()

if not logged:
    print('Unable to login to Dyson account')
    exit(1)

devices = dyson_account.devices()

dnum = 0
for d in devices:
    print('device #' + str(dnum) + ": " + str(d))
    dnum = dnum + 1

device = devices[DEVICE_NUM]

connected = devices[DEVICE_NUM].auto_connect()
device.add_message_listener(on_message)

print('device connected: ' + str(connected))

print('device state: ' + str(device.state))

print('Turning off device...')
device.turn_off()

time.sleep(10)

print('Turning on device...')
device.turn_on()

time.sleep(10)

print('Enabling oscillation...')
device.enable_oscillation(90, 180)

time.sleep(10)

print('Disabling oscillation...')
device.disable_oscillation()

time.sleep(10)

print('Enabling sleep timer...')
device.enable_sleep_timer(100)

time.sleep(10)

print('Disabling sleep timer...')
device.disable_sleep_timer()

time.sleep(10)

print('Setting fan speed...')
device.set_fan_speed(FanSpeed.FAN_SPEED_10)

time.sleep(10)

print('Enabling frontal direction...')
device.enable_frontal_direction()

time.sleep(10)

print('Disabling frontal direction...')
device.disable_frontal_direction()

time.sleep(10)

print('Enabling auto mode...')
device.enable_auto_mode()

time.sleep(10)

print('Disabling auto mode...')
device.disable_auto_mode()

time.sleep(10)

print('Enabling night mode...')
device.enable_night_mode()

time.sleep(10)

print('Disabling night mode...')
device.disable_night_mode()

time.sleep(10)

print('Enabling heating mode...')
device.enable_heat_mode()

time.sleep(10)

print('Setting target temperature...')
device.set_heat_target(HeatTarget.celsius(24))

time.sleep(10)

print('Disabling heating mode...')
device.disable_heat_mode()

print('Done')

exit(0)
