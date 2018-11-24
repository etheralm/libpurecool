import json
import unittest
from unittest import mock
from unittest.mock import Mock

from libpurecool.const import FanPower, FrontalDirection, AutoMode, \
    OscillationV2, NightMode, ContinuousMonitoring, \
    FanSpeed, ResetFilter, DYSON_PURE_COOL, SLEEP_TIMER_OFF
from libpurecool.dyson_device import NetworkDevice
from libpurecool.dyson_pure_cool import DysonPureCool
from libpurecool.dyson_pure_state_v2 import \
    DysonPureCoolV2State, DysonEnvironmentalSensorV2State


def _mocked_send_command(*args):
    assert args[0] == '{0}/device-id-1/command'.format(DYSON_PURE_COOL)
    payload = json.loads(args[1])
    if payload['msg'] == "STATE-SET":
        assert payload['time']
        assert payload['data']['fpwr'] == "ON"
        assert payload['data']['fdir'] == "ON"
        assert payload['data']['auto'] == "ON"
        assert payload['data']['oson'] == "OION"
        assert payload['data']['nmod'] == "ON"
        assert payload['data']['rhtm'] == "ON"
        assert payload['data']['fnsp'] == "0007"
        assert payload['data']['sltm'] == "240"
        assert payload['data']['ancp'] == "CUST"
        assert payload['data']['osal'] == "110"
        assert payload['data']['osau'] == "150"
        assert payload['data']['rstf'] == "STET"
        assert payload['mode-reason'] == "LAPP"
        assert payload['msg'] == "STATE-SET"
        assert args[2] == 1


def _mocked_send_command_default(*args):
    assert args[0] == '{0}/device-id-1/command'.format(DYSON_PURE_COOL)
    payload = json.loads(args[1])
    if payload['msg'] == "STATE-SET":
        assert payload['time']
        assert payload['data']['fpwr'] == "OFF"
        assert payload['data']['fdir'] == "OFF"
        assert payload['data']['auto'] == "OFF"
        assert payload['data']['oson'] == "OIOF"
        assert payload['data']['nmod'] == "OFF"
        assert payload['data']['rhtm'] == "OFF"
        assert payload['data']['fnsp'] == "AUTO"
        assert payload['data']['ancp'] == "CUST"
        assert payload['data']['osal'] == "0063"
        assert payload['data']['osau'] == "0243"
        assert payload['data']['rstf'] == "STET"
        assert payload['mode-reason'] == "LAPP"
        assert payload['msg'] == "STATE-SET"
        assert args[2] == 1


def _mocked_send_command_turn_on(*args):
    assert args[0] == '{0}/device-id-1/command'.format(DYSON_PURE_COOL)
    payload = json.loads(args[1])
    if payload['msg'] == "STATE-SET":
        assert payload['time']
        assert payload['data']['fpwr'] == "ON"

        assert payload['mode-reason'] == "LAPP"
        assert payload['msg'] == "STATE-SET"
        assert args[2] == 1


def _mocked_send_command_turn_off(*args):
    assert args[0] == '{0}/device-id-1/command'.format(DYSON_PURE_COOL)
    payload = json.loads(args[1])
    if payload['msg'] == "STATE-SET":
        assert payload['time']
        assert payload['data']['fpwr'] == "OFF"

        assert payload['mode-reason'] == "LAPP"
        assert payload['msg'] == "STATE-SET"
        assert args[2] == 1


def _mocked_send_command_oscillation_on_empty(*args):
    assert args[0] == '{0}/device-id-1/command'.format(DYSON_PURE_COOL)
    payload = json.loads(args[1])
    if payload['msg'] == "STATE-SET":
        assert payload['time']
        assert payload['data']['oson'] == "OION"
        assert payload['data']['fpwr'] == "ON"
        assert payload['data']['ancp'] == "CUST"
        assert payload['data']['osal'] == "0063"
        assert payload['data']['osau'] == "0243"

        assert payload['mode-reason'] == "LAPP"
        assert payload['msg'] == "STATE-SET"
        assert args[2] == 1


def _mocked_send_command_oscillation_on(*args):
    assert args[0] == '{0}/device-id-1/command'.format(DYSON_PURE_COOL)
    payload = json.loads(args[1])
    if payload['msg'] == "STATE-SET":
        assert payload['time']
        assert payload['data']['oson'] == "OION"
        assert payload['data']['fpwr'] == "ON"
        assert payload['data']['ancp'] == "CUST"
        assert payload['data']['osal'] == "0120"
        assert payload['data']['osau'] == "0150"

        assert payload['mode-reason'] == "LAPP"
        assert payload['msg'] == "STATE-SET"
        assert args[2] == 1


def _mocked_send_command_oscillation_on_equal(*args):
    assert args[0] == '{0}/device-id-1/command'.format(DYSON_PURE_COOL)
    payload = json.loads(args[1])
    if payload['msg'] == "STATE-SET":
        assert payload['time']
        assert payload['data']['oson'] == "OION"
        assert payload['data']['fpwr'] == "ON"
        assert payload['data']['ancp'] == "CUST"
        assert payload['data']['osal'] == "0120"
        assert payload['data']['osau'] == "0120"

        assert payload['mode-reason'] == "LAPP"
        assert payload['msg'] == "STATE-SET"
        assert args[2] == 1


def _mocked_send_command_oscillation_off(*args):
    assert args[0] == '{0}/device-id-1/command'.format(DYSON_PURE_COOL)
    payload = json.loads(args[1])
    if payload['msg'] == "STATE-SET":
        assert payload['time']
        assert payload['data']['oson'] == "OIOF"

        assert payload['mode-reason'] == "LAPP"
        assert payload['msg'] == "STATE-SET"
        assert args[2] == 1


def _mocked_send_command_timer_on(*args):
    assert args[0] == '{0}/device-id-1/command'.format(DYSON_PURE_COOL)
    payload = json.loads(args[1])
    if payload['msg'] == "STATE-SET":
        assert payload['time']
        assert payload['data']['sltm'] == "0540"

        assert payload['mode-reason'] == "LAPP"
        assert payload['msg'] == "STATE-SET"
        assert args[2] == 1


def _mocked_send_command_timer_off(*args):
    assert args[0] == '{0}/device-id-1/command'.format(DYSON_PURE_COOL)
    payload = json.loads(args[1])
    if payload['msg'] == "STATE-SET":
        assert payload['time']
        assert payload['data']['sltm'] == "OFF"

        assert payload['mode-reason'] == "LAPP"
        assert payload['msg'] == "STATE-SET"
        assert args[2] == 1


def _mocked_send_command_set_speed(*args):
    assert args[0] == '{0}/device-id-1/command'.format(DYSON_PURE_COOL)
    payload = json.loads(args[1])
    if payload['msg'] == "STATE-SET":
        assert payload['time']
        assert payload['data']['fnsp'] == "0007"

        assert payload['mode-reason'] == "LAPP"
        assert payload['msg'] == "STATE-SET"
        assert args[2] == 1


def _mocked_send_command_front_on(*args):
    assert args[0] == '{0}/device-id-1/command'.format(DYSON_PURE_COOL)
    payload = json.loads(args[1])
    if payload['msg'] == "STATE-SET":
        assert payload['time']
        assert payload['data']['fdir'] == "ON"

        assert payload['mode-reason'] == "LAPP"
        assert payload['msg'] == "STATE-SET"
        assert args[2] == 1


def _mocked_send_command_front_off(*args):
    assert args[0] == '{0}/device-id-1/command'.format(DYSON_PURE_COOL)
    payload = json.loads(args[1])
    if payload['msg'] == "STATE-SET":
        assert payload['time']
        assert payload['data']['fdir'] == "OFF"

        assert payload['mode-reason'] == "LAPP"
        assert payload['msg'] == "STATE-SET"
        assert args[2] == 1


def _mocked_send_command_auto_on(*args):
    assert args[0] == '{0}/device-id-1/command'.format(DYSON_PURE_COOL)
    payload = json.loads(args[1])
    if payload['msg'] == "STATE-SET":
        assert payload['time']
        assert payload['data']['auto'] == "ON"

        assert payload['mode-reason'] == "LAPP"
        assert payload['msg'] == "STATE-SET"
        assert args[2] == 1


def _mocked_send_command_auto_off(*args):
    assert args[0] == '{0}/device-id-1/command'.format(DYSON_PURE_COOL)
    payload = json.loads(args[1])
    if payload['msg'] == "STATE-SET":
        assert payload['time']
        assert payload['data']['auto'] == "OFF"

        assert payload['mode-reason'] == "LAPP"
        assert payload['msg'] == "STATE-SET"
        assert args[2] == 1


def _mocked_send_command_night_mode_on(*args):
    assert args[0] == '{0}/device-id-1/command'.format(DYSON_PURE_COOL)
    payload = json.loads(args[1])
    if payload['msg'] == "STATE-SET":
        assert payload['time']
        assert payload['data']['nmod'] == "ON"

        assert payload['mode-reason'] == "LAPP"
        assert payload['msg'] == "STATE-SET"
        assert args[2] == 1


def _mocked_send_command_night_mode_off(*args):
    assert args[0] == '{0}/device-id-1/command'.format(DYSON_PURE_COOL)
    payload = json.loads(args[1])
    if payload['msg'] == "STATE-SET":
        assert payload['time']
        assert payload['data']['nmod'] == "OFF"

        assert payload['mode-reason'] == "LAPP"
        assert payload['msg'] == "STATE-SET"
        assert args[2] == 1


class TestPureCool(unittest.TestCase):
    def setUp(self):
        device = DysonPureCool({
            "Serial": "device-id-1",
            "Name": "device-1",
            "ScaleUnit": "SU01",
            "Version": "21.03.08",
            "LocalCredentials": "1/aJ5t52WvAfn+z+fjDuef86kQDQPefbQ6/70ZGysII1K"
                                "e1i0ZHakFH84DZuxsSQ4KTT2vbCm7uYeTORULKLKQ==",
            "AutoUpdate": True,
            "NewVersionAvailable": False,
            "ProductType": DYSON_PURE_COOL
        })
        network_device = NetworkDevice('device-1', 'host', 1111)
        device._add_network_device(network_device)
        device._current_state = DysonPureCoolV2State(
            open("tests/data/state_pure_cool.json", "r").read())
        device.connection_callback(True)
        device.state_data_available()
        device.sensor_data_available()
        self._device = device

    def tearDown(self):
        pass

    @mock.patch('paho.mqtt.client.Client.publish',
                side_effect=_mocked_send_command)
    @mock.patch('paho.mqtt.client.Client.connect')
    def test_set_configuration(self, mocked_connect, mocked_publish):

        connected = self._device.auto_connect()
        self.assertTrue(connected)
        self.assertEqual(mocked_connect.call_count, 1)
        self._device\
            .set_configuration(fan_power=FanPower.POWER_ON,
                               front_direction=FrontalDirection.FRONTAL_ON,
                               auto_mode=AutoMode.AUTO_ON,
                               oscillation=OscillationV2.OSCILLATION_ON,
                               night_mode=NightMode.NIGHT_MODE_ON,
                               continuous_monitoring=ContinuousMonitoring.
                               MONITORING_ON,
                               fan_speed=FanSpeed.FAN_SPEED_7,
                               sleep_timer=240,
                               oscillation_angle_low=110,
                               oscillation_angle_high=150,
                               reset_filter=ResetFilter.DO_NOTHING,
                               )

        self.assertEqual(mocked_publish.call_count, 3)
        self.assertEqual(self._device.__repr__(),
                         "DysonPureCool(serial=device-id-1,active=None,"
                         "name=device-1,version=21.03.08,auto_update=True,"
                         "new_version_available=False,product_type=438,"
                         "network_device=NetworkDevice(name=device-1,"
                         "address=host,port=1111))")
        self._device.disconnect()

    @mock.patch('paho.mqtt.client.Client.publish',
                side_effect=_mocked_send_command_default)
    @mock.patch('paho.mqtt.client.Client.connect')
    def test_set_configuration_empty(self, mocked_connect, mocked_publish):
        connected = self._device.auto_connect()
        self.assertTrue(connected)
        self.assertEqual(mocked_connect.call_count, 1)
        self._device.set_configuration()

        self.assertEqual(mocked_publish.call_count, 3)
        self.assertEqual(self._device.__repr__(),
                         "DysonPureCool(serial=device-id-1,active=None,"
                         "name=device-1,version=21.03.08,auto_update=True,"
                         "new_version_available=False,product_type=438,"
                         "network_device=NetworkDevice(name=device-1,"
                         "address=host,port=1111))")
        self._device.disconnect()

    @mock.patch('paho.mqtt.client.Client.publish',
                side_effect=_mocked_send_command_turn_on)
    @mock.patch('paho.mqtt.client.Client.connect')
    def test_turn_on(self, mocked_connect, mocked_publish):

        connected = self._device.auto_connect()
        self.assertTrue(connected)
        self.assertEqual(mocked_connect.call_count, 1)
        self._device.turn_on()

        self.assertEqual(mocked_publish.call_count, 3)
        self._device.disconnect()

    @mock.patch('paho.mqtt.client.Client.publish',
                side_effect=_mocked_send_command_turn_off)
    @mock.patch('paho.mqtt.client.Client.connect')
    def test_turn_off(self, mocked_connect, mocked_publish):

        connected = self._device.auto_connect()
        self.assertTrue(connected)
        self.assertEqual(mocked_connect.call_count, 1)
        self._device.turn_off()

        self.assertEqual(mocked_publish.call_count, 3)
        self._device.disconnect()

    @mock.patch('paho.mqtt.client.Client.publish',
                side_effect=_mocked_send_command_oscillation_on_empty)
    @mock.patch('paho.mqtt.client.Client.connect')
    def test_turn_oscillation_on_empty(self, mocked_connect, mocked_publish):

        connected = self._device.auto_connect()
        self.assertTrue(connected)
        self.assertEqual(mocked_connect.call_count, 1)
        self._device.enable_oscillation()

        self.assertEqual(mocked_publish.call_count, 3)
        self._device.disconnect()

    @mock.patch('paho.mqtt.client.Client.publish',
                side_effect=_mocked_send_command_oscillation_on)
    @mock.patch('paho.mqtt.client.Client.connect')
    def test_turn_oscillation_on(self, mocked_connect, mocked_publish):

        connected = self._device.auto_connect()
        self.assertTrue(connected)
        self.assertEqual(mocked_connect.call_count, 1)
        self._device.enable_oscillation(120, 150)

        self.assertEqual(mocked_publish.call_count, 3)
        self._device.disconnect()

    @mock.patch('paho.mqtt.client.Client.publish',
                side_effect=_mocked_send_command_oscillation_on_equal)
    @mock.patch('paho.mqtt.client.Client.connect')
    def test_turn_oscillation_on_equal(self, mocked_connect, mocked_publish):

        connected = self._device.auto_connect()
        self.assertTrue(connected)
        self.assertEqual(mocked_connect.call_count, 1)
        self._device.enable_oscillation(120, 120)

        self.assertEqual(mocked_publish.call_count, 3)
        self._device.disconnect()

    @mock.patch('paho.mqtt.client.Client.connect')
    def test_oson_wrong_args_raise_errors(self, mocked_connect):

        connected = self._device.auto_connect()
        self.assertTrue(connected)
        self.assertEqual(mocked_connect.call_count, 1)
        self.assertRaises(TypeError,
                          self._device.enable_oscillation, "test", 160)
        self.assertRaises(TypeError,
                          self._device.enable_oscillation, 160, "test")
        self.assertRaises(ValueError,
                          self._device.enable_oscillation, 1, 110)
        self.assertRaises(ValueError,
                          self._device.enable_oscillation, 356, 110)
        self.assertRaises(ValueError,
                          self._device.enable_oscillation, 110, 1)
        self.assertRaises(ValueError,
                          self._device.enable_oscillation, 110, 356)
        self.assertRaises(ValueError,
                          self._device.enable_oscillation, 355, 5)
        self.assertRaises(ValueError,
                          self._device.enable_oscillation, 110, 129)
        self._device.disconnect()

    @mock.patch('paho.mqtt.client.Client.publish',
                side_effect=_mocked_send_command_oscillation_off)
    @mock.patch('paho.mqtt.client.Client.connect')
    def test_oscillation_off(self, mocked_connect, mocked_publish):
        connected = self._device.auto_connect()
        self.assertTrue(connected)
        self.assertEqual(mocked_connect.call_count, 1)
        self._device.disable_oscillation()

        self.assertEqual(mocked_publish.call_count, 3)
        self._device.disconnect()

    @mock.patch('paho.mqtt.client.Client.publish',
                side_effect=_mocked_send_command_timer_on)
    @mock.patch('paho.mqtt.client.Client.connect')
    def test_timer_on(self, mocked_connect, mocked_publish):

        connected = self._device.auto_connect()
        self.assertTrue(connected)
        self.assertEqual(mocked_connect.call_count, 1)
        self._device.enable_sleep_timer(540)

        self.assertEqual(mocked_publish.call_count, 3)
        self._device.disconnect()

    @mock.patch('paho.mqtt.client.Client.connect')
    def test_sltm_wrong_arg_rise_errors(self, mocked_connect):

        connected = self._device.auto_connect()
        self.assertTrue(connected)
        self.assertEqual(mocked_connect.call_count, 1)

        self.assertRaises(TypeError,
                          self._device.enable_sleep_timer)
        self.assertRaises(TypeError,
                          self._device.enable_sleep_timer, "test")
        self.assertRaises(ValueError,
                          self._device.enable_sleep_timer, 0)
        self.assertRaises(ValueError,
                          self._device.enable_sleep_timer, 541)
        self._device.disconnect()

    @mock.patch('paho.mqtt.client.Client.publish',
                side_effect=_mocked_send_command_timer_off)
    @mock.patch('paho.mqtt.client.Client.connect')
    def test_timer_off(self, mocked_connect, mocked_publish):

        connected = self._device.auto_connect()
        self.assertTrue(connected)
        self.assertEqual(mocked_connect.call_count, 1)
        self._device.disable_sleep_timer()

        self.assertEqual(mocked_publish.call_count, 3)
        self._device.disconnect()

    @mock.patch('paho.mqtt.client.Client.publish',
                side_effect=_mocked_send_command_set_speed)
    @mock.patch('paho.mqtt.client.Client.connect')
    def test_set_speed(self, mocked_connect, mocked_publish):

        connected = self._device.auto_connect()
        self.assertTrue(connected)
        self.assertEqual(mocked_connect.call_count, 1)
        self._device.set_fan_speed(FanSpeed.FAN_SPEED_7)

        self.assertEqual(mocked_publish.call_count, 3)
        self._device.disconnect()

    @mock.patch('paho.mqtt.client.Client.connect')
    def test_set_speed_wrong_value_raise_error(self, mocked_connect):

        connected = self._device.auto_connect()
        self.assertTrue(connected)
        self.assertEqual(mocked_connect.call_count, 1)
        self.assertRaises(TypeError,
                          self._device.set_fan_speed, "test")

        self._device.disconnect()

    @mock.patch('paho.mqtt.client.Client.publish',
                side_effect=_mocked_send_command_front_on)
    @mock.patch('paho.mqtt.client.Client.connect')
    def test_front_on(self, mocked_connect, mocked_publish):

        connected = self._device.auto_connect()
        self.assertTrue(connected)
        self.assertEqual(mocked_connect.call_count, 1)
        self._device.enable_frontal_direction()

        self.assertEqual(mocked_publish.call_count, 3)
        self._device.disconnect()

    @mock.patch('paho.mqtt.client.Client.publish',
                side_effect=_mocked_send_command_front_off)
    @mock.patch('paho.mqtt.client.Client.connect')
    def test_front_off(self, mocked_connect, mocked_publish):

        connected = self._device.auto_connect()
        self.assertTrue(connected)
        self.assertEqual(mocked_connect.call_count, 1)
        self._device.disable_frontal_direction()

        self.assertEqual(mocked_publish.call_count, 3)
        self._device.disconnect()

    @mock.patch('paho.mqtt.client.Client.publish',
                side_effect=_mocked_send_command_auto_on)
    @mock.patch('paho.mqtt.client.Client.connect')
    def test_auto_on(self, mocked_connect, mocked_publish):

        connected = self._device.auto_connect()
        self.assertTrue(connected)
        self.assertEqual(mocked_connect.call_count, 1)
        self._device.enable_auto_mode()

        self.assertEqual(mocked_publish.call_count, 3)
        self._device.disconnect()

    @mock.patch('paho.mqtt.client.Client.publish',
                side_effect=_mocked_send_command_auto_off)
    @mock.patch('paho.mqtt.client.Client.connect')
    def test_auto_off(self, mocked_connect, mocked_publish):

        connected = self._device.auto_connect()
        self.assertTrue(connected)
        self.assertEqual(mocked_connect.call_count, 1)
        self._device.disable_auto_mode()

        self.assertEqual(mocked_publish.call_count, 3)
        self._device.disconnect()

    @mock.patch('paho.mqtt.client.Client.publish',
                side_effect=_mocked_send_command_night_mode_on)
    @mock.patch('paho.mqtt.client.Client.connect')
    def test_night_mode_on(self, mocked_connect, mocked_publish):

        connected = self._device.auto_connect()
        self.assertTrue(connected)
        self.assertEqual(mocked_connect.call_count, 1)
        self._device.enable_night_mode()

        self.assertEqual(mocked_publish.call_count, 3)
        self._device.disconnect()

    @mock.patch('paho.mqtt.client.Client.publish',
                side_effect=_mocked_send_command_night_mode_off)
    @mock.patch('paho.mqtt.client.Client.connect')
    def test_night_mode_off(self, mocked_connect, mocked_publish):

        connected = self._device.auto_connect()
        self.assertTrue(connected)
        self.assertEqual(mocked_connect.call_count, 1)
        self._device.disable_night_mode()

        self.assertEqual(mocked_publish.call_count, 3)
        self._device.disconnect()

    def test_dyson_v2_state(self):
        dyson_state = DysonPureCoolV2State(
            open("tests/data/state_pure_cool.json", "r").read())
        self.assertEqual(dyson_state.fan_power, FanPower.POWER_OFF.value)
        self.assertEqual(dyson_state.front_direction,
                         FrontalDirection.FRONTAL_OFF.value)
        self.assertEqual(dyson_state.auto_mode, AutoMode.AUTO_OFF.value)
        self.assertEqual(dyson_state.oscillation_status, "OFF")
        self.assertEqual(dyson_state.oscillation,
                         OscillationV2.OSCILLATION_OFF.value)
        self.assertEqual(dyson_state.night_mode,
                         NightMode.NIGHT_MODE_OFF.value)
        self.assertEqual(dyson_state.continuous_monitoring,
                         ContinuousMonitoring.MONITORING_OFF.value)
        self.assertEqual(dyson_state.fan_state, "FAN")
        self.assertEqual(dyson_state.night_mode_speed, "0004")
        self.assertEqual(dyson_state.speed, FanSpeed.FAN_SPEED_AUTO.value)
        self.assertEqual(dyson_state.carbon_filter_state, "0100")
        self.assertEqual(dyson_state.hepa_filter_state, "0100")
        self.assertEqual(dyson_state.sleep_timer, SLEEP_TIMER_OFF)
        self.assertEqual(dyson_state.oscillation_angle_low, "0063")
        self.assertEqual(dyson_state.oscillation_angle_high, "0243")
        self.assertEqual(dyson_state.__repr__(),
                         "DysonPureCoolV2State(fan_power=OFF,"
                         "front_direction=OFF,auto_mode=OFF,"
                         "oscillation_status=OFF,oscillation=OIOF,"
                         "night_mode=OFF,continuous_monitoring=OFF,"
                         "fan_state=FAN,night_mode_speed=0004,"
                         "speed=AUTO,carbon_filter_state=0100,"
                         "hepa_filter_state=0100,sleep_timer=OFF,"
                         "oscillation_angle_low=0063,"
                         "oscillation_angle_high=0243)")

    def test_dyson_v2_sensor_state(self):
        dyson_sensor_state = DysonEnvironmentalSensorV2State(
            open("tests/data/sensor_pure_cool.json", "r").read())
        self.assertEqual(dyson_sensor_state.temperature, 297.7)
        self.assertEqual(dyson_sensor_state.humidity, 58)
        self.assertEqual(dyson_sensor_state.particulate_matter_25, 9)
        self.assertEqual(dyson_sensor_state.particulate_matter_10, 5)
        self.assertEqual(dyson_sensor_state.volatile_organic_compounds, 4)
        self.assertEqual(dyson_sensor_state.volatile_organic_compounds, 4)
        self.assertEqual(dyson_sensor_state.p25r, 10)
        self.assertEqual(dyson_sensor_state.p10r, 9)
        self.assertEqual(dyson_sensor_state.__repr__(),
                         "DysonEnvironmentalSensorV2State("
                         "temperature=297.7,humidity=58,"
                         "particulate_matter_25=9,particulate_matter_10=5,"
                         "volatile_organic_compounds=4,nitrogen_dioxide=11,"
                         "p25r=10,p10r=9,sleep_timer=0)")

    def test_dyson_v2_sensor_state_off(self):
        dyson_sensor_state = DysonEnvironmentalSensorV2State(
            open("tests/data/sensor_pure_cool_off.json", "r").read())
        self.assertEqual(dyson_sensor_state.temperature, 0)
        self.assertEqual(dyson_sensor_state.humidity, 0)
        self.assertEqual(dyson_sensor_state.particulate_matter_25, 0)
        self.assertEqual(dyson_sensor_state.particulate_matter_10, 0)
        self.assertEqual(dyson_sensor_state.volatile_organic_compounds, 0)
        self.assertEqual(dyson_sensor_state.volatile_organic_compounds, 0)
        self.assertEqual(dyson_sensor_state.p25r, 0)
        self.assertEqual(dyson_sensor_state.p10r, 0)
        self.assertEqual(dyson_sensor_state.__repr__(),
                         "DysonEnvironmentalSensorV2State("
                         "temperature=0,humidity=0,particulate_matter_25=0,"
                         "particulate_matter_10=0,"
                         "volatile_organic_compounds=0,nitrogen_dioxide=0,"
                         "p25r=0,p10r=0,sleep_timer=0)")

    def test_dyson_v2_sensor_state_init(self):
        dyson_sensor_state = DysonEnvironmentalSensorV2State(
            open("tests/data/sensor_pure_cool_init.json", "r").read())
        self.assertEqual(dyson_sensor_state.temperature, 0)
        self.assertEqual(dyson_sensor_state.humidity, 0)
        self.assertEqual(dyson_sensor_state.particulate_matter_25, 0)
        self.assertEqual(dyson_sensor_state.particulate_matter_10, 0)
        self.assertEqual(dyson_sensor_state.volatile_organic_compounds, 0)
        self.assertEqual(dyson_sensor_state.volatile_organic_compounds, 0)
        self.assertEqual(dyson_sensor_state.p25r, 0)
        self.assertEqual(dyson_sensor_state.p10r, 0)
        self.assertEqual(dyson_sensor_state.__repr__(),
                         "DysonEnvironmentalSensorV2State("
                         "temperature=0,humidity=0,particulate_matter_25=0,"
                         "particulate_matter_10=0,"
                         "volatile_organic_compounds=0,nitrogen_dioxide=0,"
                         "p25r=0,p10r=0,sleep_timer=0)")

    def test_on_state_v2_message(self):
        def on_message(msg):
            assert isinstance(msg, DysonPureCoolV2State)

        self._device.add_message_listener(on_message)
        msg = Mock()
        payload = open("tests/data/state_pure_cool.json", "r").read()
        msg.payload = Mock()
        msg.payload.decode.return_value = payload
        DysonPureCool.on_message(None, self._device, msg)

    def test_on_sensor_v2_message(self):
        def on_message(msg):
            assert isinstance(msg, DysonEnvironmentalSensorV2State)

        self._device.add_message_listener(on_message)
        msg = Mock()
        payload = open("tests/data/sensor_pure_cool.json", "r").read()
        msg.payload = Mock()
        msg.payload.decode.return_value = payload
        DysonPureCool.on_message(None, self._device, msg)
