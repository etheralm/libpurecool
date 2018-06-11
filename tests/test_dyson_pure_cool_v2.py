import json
import unittest
from unittest import mock

from libpurecoollink.const import FanPower, FrontalDirection, AutoMode, \
    OscillationV2, NightMode, ContinuousMonitoring, \
    FanSpeed, ResetFilter, DYSON_PURE_COOL
from libpurecoollink.dyson_device import NetworkDevice
from libpurecoollink.dyson_pure_cool import DysonPureCool
from libpurecoollink.dyson_pure_state_v2 import DysonPureCoolV2State


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