import json
import unittest
from unittest import mock

from libpurecool.dyson_pure_hotcool import DysonPureHotCool
from libpurecool.const import FanPower, FrontalDirection, AutoMode, \
    OscillationV2, NightMode, ContinuousMonitoring, \
    FanSpeed, ResetFilter, DYSON_PURE_HOT_COOL, TiltState, \
    HeatTarget, SLEEP_TIMER_OFF
from libpurecool.dyson_device import NetworkDevice
from libpurecool.dyson_pure_state_v2 import DysonPureHotCoolV2State


def _mocked_send_command(*args):
    assert args[0] == '{0}/device-id-1/command'.format(DYSON_PURE_HOT_COOL)
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
    assert args[0] == '{0}/device-id-1/command'.format(DYSON_PURE_HOT_COOL)
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


def _mocked_send_command_heat_on(*args):
    assert args[0] == '{0}/device-id-1/command'.format(DYSON_PURE_HOT_COOL)
    payload = json.loads(args[1])
    if payload['msg'] == "STATE-SET":
        assert payload['time']
        assert payload['data']['hmod'] == "HEAT"

        assert payload['mode-reason'] == "LAPP"
        assert payload['msg'] == "STATE-SET"
        assert args[2] == 1


def _mocked_send_command_heat_off(*args):
    assert args[0] == '{0}/device-id-1/command'.format(DYSON_PURE_HOT_COOL)
    payload = json.loads(args[1])
    if payload['msg'] == "STATE-SET":
        assert payload['time']
        assert payload['data']['hmod'] == "OFF"

        assert payload['mode-reason'] == "LAPP"
        assert payload['msg'] == "STATE-SET"
        assert args[2] == 1


def _mocked_send_command_heat_target(*args):
    assert args[0] == '{0}/device-id-1/command'.format(DYSON_PURE_HOT_COOL)
    payload = json.loads(args[1])
    if payload['msg'] == "STATE-SET":
        assert payload['time']
        assert payload['data']['hmax'] == "2970"

        assert payload['mode-reason'] == "LAPP"
        assert payload['msg'] == "STATE-SET"
        assert args[2] == 1


class TestPureHotCool(unittest.TestCase):
    def setUp(self):
        device = DysonPureHotCool({
            "Serial": "device-id-1",
            "Name": "device-1",
            "ScaleUnit": "SU01",
            "Version": "21.03.08",
            "LocalCredentials": "1/aJ5t52WvAfn+z+fjDuef86kQDQPefbQ6/70ZGysII1K"
                                "e1i0ZHakFH84DZuxsSQ4KTT2vbCm7uYeTORULKLKQ==",
            "AutoUpdate": True,
            "NewVersionAvailable": False,
            "ProductType": DYSON_PURE_HOT_COOL
        })
        network_device = NetworkDevice('device-1', 'host', 1111)
        device._add_network_device(network_device)
        device._current_state = DysonPureHotCoolV2State(
            open("tests/data/state_pure_hotcool.json", "r").read())
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
                               tilt=TiltState.TILT_TRUE
                               )

        self.assertEqual(mocked_publish.call_count, 3)
        self.assertEqual(self._device.__repr__(),
                         "DysonPureHotCool(serial=device-id-1,active=None,"
                         "name=device-1,version=21.03.08,auto_update=True,"
                         "new_version_available=False,product_type=527,"
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
                         "DysonPureHotCool(serial=device-id-1,active=None,"
                         "name=device-1,version=21.03.08,auto_update=True,"
                         "new_version_available=False,product_type=527,"
                         "network_device=NetworkDevice(name=device-1,"
                         "address=host,port=1111))")
        self._device.disconnect()

    @mock.patch('paho.mqtt.client.Client.publish',
                side_effect=_mocked_send_command_heat_on)
    @mock.patch('paho.mqtt.client.Client.connect')
    def test_enable_heat_mode(self, mocked_connect, mocked_publish):

        connected = self._device.auto_connect()
        self.assertTrue(connected)
        self.assertEqual(mocked_connect.call_count, 1)
        self._device.enable_heat_mode()

        self.assertEqual(mocked_publish.call_count, 3)
        self._device.disconnect()

    @mock.patch('paho.mqtt.client.Client.publish',
                side_effect=_mocked_send_command_heat_off)
    @mock.patch('paho.mqtt.client.Client.connect')
    def test_disable_heat_mode(self, mocked_connect, mocked_publish):

        connected = self._device.auto_connect()
        self.assertTrue(connected)
        self.assertEqual(mocked_connect.call_count, 1)
        self._device.disable_heat_mode()

        self.assertEqual(mocked_publish.call_count, 3)
        self._device.disconnect()

    @mock.patch('paho.mqtt.client.Client.publish',
                side_effect=_mocked_send_command_heat_target)
    @mock.patch('paho.mqtt.client.Client.connect')
    def test_heat_target(self, mocked_connect, mocked_publish):

        connected = self._device.auto_connect()
        self.assertTrue(connected)
        self.assertEqual(mocked_connect.call_count, 1)
        self._device.set_heat_target(HeatTarget.celsius(24))

        self.assertEqual(mocked_publish.call_count, 3)
        self._device.disconnect()

    def test_dyson_v2_state(self):
        dyson_state = DysonPureHotCoolV2State(
            open("tests/data/state_pure_hotcool.json", "r").read())
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
        self.assertEqual(dyson_state.tilt, "OK")
        self.assertEqual(dyson_state.heat_mode, "HEAT")
        self.assertEqual(dyson_state.heat_target, "2932")
        self.assertEqual(dyson_state.heat_state, "OFF")
        self.assertEqual(dyson_state.__repr__(),
                         "DysonPureHotCoolV2State(fan_power=OFF,"
                         "front_direction=OFF,auto_mode=OFF,"
                         "oscillation_status=OFF,oscillation=OIOF,"
                         "night_mode=OFF,continuous_monitoring=OFF,"
                         "fan_state=FAN,night_mode_speed=0004,"
                         "speed=AUTO,carbon_filter_state=0100,"
                         "hepa_filter_state=0100,sleep_timer=OFF,"
                         "oscillation_angle_low=0063,"
                         "oscillation_angle_high=0243,"
                         "tilt=OK,heat_mode=HEAT,heat_target=2932,"
                         "heat_state=OFF)")
