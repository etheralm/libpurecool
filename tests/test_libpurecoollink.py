import unittest

from unittest import mock
from unittest.mock import Mock
import json

from libpurecool.dyson_device import NetworkDevice
from libpurecool.dyson_pure_cool_link import DysonPureCoolState, \
    DysonEnvironmentalSensorState, DysonPureCoolLink
from libpurecool.dyson_pure_hotcool_link import DysonPureHotCoolLink
from libpurecool.dyson_pure_state import DysonPureHotCoolState
from libpurecool.const import FanMode, NightMode, FanSpeed, Oscillation, \
    FanState, QualityTarget, StandbyMonitoring as SM, \
    DYSON_PURE_COOL_LINK_DESK as Desk, DYSON_PURE_HOT_COOL_LINK_TOUR as Hot, \
    HeatMode, HeatState, HeatTarget, FocusMode, TiltState, ResetFilter
from libpurecool.exceptions import DysonInvalidTargetTemperatureException


def _mocked_request_state(*args, **kwargs):
    assert args[0] == '475/device-id-1/command'
    msg = json.loads(args[1])
    assert msg['msg'] in ['REQUEST-CURRENT-STATE',
                          'REQUEST-PRODUCT-ENVIRONMENT-CURRENT-SENSOR-DATA']
    assert msg['time']


def _mocked_send_command(*args, **kwargs):
    assert args[0] == '{0}/device-id-1/command'.format(Desk)
    payload = json.loads(args[1])
    if payload['msg'] == "STATE-SET":
        assert payload['time']
        assert payload['data']['fmod'] == "FAN"
        assert payload['data']['nmod'] == "OFF"
        assert payload['data']['oson'] == "ON"
        assert payload['data']['rstf'] == "STET"
        assert payload['data']['qtar'] == "0004"
        assert payload['data']['fnsp'] == "0003"
        assert payload['data']['sltm'] == "STET"
        assert payload['data']['rhtm'] == "ON"
        assert payload['mode-reason'] == "LAPP"
        assert payload['msg'] == "STATE-SET"
        assert args[2] == 1


def _mocked_send_command_hot(*args, **kwargs):
    assert args[0] == '{0}/device-id-1/command'.format(Hot)
    payload = json.loads(args[1])
    if payload['msg'] == "STATE-SET":
        assert payload['time']
        assert payload['data']['fmod'] == "FAN"
        assert payload['data']['nmod'] == "OFF"
        assert payload['data']['oson'] == "ON"
        assert payload['data']['rstf'] == "STET"
        assert payload['data']['qtar'] == "0004"
        assert payload['data']['fnsp'] == "0003"
        assert payload['data']['sltm'] == "STET"
        assert payload['data']['rhtm'] == "ON"
        assert payload['data']['hmod'] == "HEAT"
        assert payload['data']['hmax'] == "2980"
        assert payload['data']['ffoc'] == "ON"
        assert payload['mode-reason'] == "LAPP"
        assert payload['msg'] == "STATE-SET"
        assert args[2] == 1


def _mocked_send_command_rst_filter(*args, **kwargs):
    assert args[0] == '475/device-id-1/command'
    payload = json.loads(args[1])
    if payload['msg'] == "STATE-SET":
        assert payload['time']
        assert payload['data']['fmod'] == "FAN"
        assert payload['data']['nmod'] == "OFF"
        assert payload['data']['oson'] == "ON"
        assert payload['data']['rstf'] == "RSTF"
        assert payload['data']['qtar'] == "0004"
        assert payload['data']['fnsp'] == "0003"
        assert payload['data']['sltm'] == "STET"
        assert payload['data']['rhtm'] == "ON"
        assert payload['mode-reason'] == "LAPP"
        assert payload['msg'] == "STATE-SET"
        assert args[2] == 1


def _mocked_send_command_timer(*args, **kwargs):
    assert args[0] == '475/device-id-1/command'
    payload = json.loads(args[1])
    if payload['msg'] == "STATE-SET":
        assert payload['time']
        assert payload['data']['sltm'] == 10
        assert args[2] == 1


def _mocked_send_command_timer_off(*args, **kwargs):
    assert args[0] == '475/device-id-1/command'
    payload = json.loads(args[1])
    if payload['msg'] == "STATE-SET":
        assert payload['time']
        assert payload['data']['sltm'] == 0
        assert args[2] == 1


def on_add_device(network_device):
    pass


def device_serial_from_name(name):
    return (name.split(".")[0]).split("_")[1]


class TestLibPureCoolLink(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @mock.patch('paho.mqtt.client.Client.loop_start')
    @mock.patch('paho.mqtt.client.Client.connect')
    def test_connect_device(self, mocked_connect, mocked_loop):
        device = DysonPureCoolLink({
            "Active": True,
            "Serial": "device-id-1",
            "Name": "device-1",
            "ScaleUnit": "SU01",
            "Version": "21.03.08",
            "LocalCredentials": "1/aJ5t52WvAfn+z+fjDuef86kQDQPefbQ6/"
                                "70ZGysII1Ke1i0ZHakFH84DZuxsSQ4KTT2v"
                                "bCm7uYeTORULKLKQ==",
            "AutoUpdate": True,
            "NewVersionAvailable": False,
            "ProductType": "475"
        })
        network_device = NetworkDevice('device-1', 'host', 1111)
        device.state_data_available()
        device.sensor_data_available()
        device.connection_callback(True)
        device._add_network_device(network_device)
        connected = device.auto_connect()
        self.assertTrue(connected)
        self.assertIsNone(device.state)
        self.assertEqual(device.network_device, network_device)
        self.assertEqual(mocked_connect.call_count, 1)
        self.assertEqual(mocked_loop.call_count, 1)
        device.disconnect()

    @mock.patch('paho.mqtt.client.Client.loop_start')
    @mock.patch('paho.mqtt.client.Client.connect')
    def test_connect_device_with_config(self, mocked_connect, mocked_loop):
        device = DysonPureCoolLink({
            "Active": True,
            "Serial": "device-id-1",
            "Name": "device-1",
            "ScaleUnit": "SU01",
            "Version": "21.03.08",
            "LocalCredentials": "1/aJ5t52WvAfn+z+fjDuef86kQDQPefbQ6/"
                                "70ZGysII1Ke1i0ZHakFH84DZuxsSQ4KTT2v"
                                "bCm7uYeTORULKLKQ==",
            "AutoUpdate": True,
            "NewVersionAvailable": False,
            "ProductType": "475"
        })
        device.connection_callback(True)
        device.state_data_available()
        device.sensor_data_available()
        connected = device.connect("192.168.0.2")
        self.assertTrue(connected)
        self.assertIsNone(device.state)
        self.assertEqual(device.network_device.name, "device-1")
        self.assertEqual(device.network_device.address, "192.168.0.2")
        self.assertEqual(device.network_device.port, 1883)
        self.assertEqual(mocked_connect.call_count, 1)
        self.assertEqual(mocked_loop.call_count, 1)
        device.disconnect()

    @mock.patch('paho.mqtt.client.Client.loop_stop')
    @mock.patch('paho.mqtt.client.Client.loop_start')
    @mock.patch('paho.mqtt.client.Client.connect')
    def test_connect_device_with_config_failed(self,
                                               mocked_connect,
                                               mocked_loop_start,
                                               mocked_loop_stop):
        device = DysonPureCoolLink({
            "Active": True,
            "Serial": "device-id-1",
            "Name": "device-1",
            "ScaleUnit": "SU01",
            "Version": "21.03.08",
            "LocalCredentials": "1/aJ5t52WvAfn+z+fjDuef86kQDQPefbQ6/"
                                "70ZGysII1Ke1i0ZHakFH84DZuxsSQ4KTT2v"
                                "bCm7uYeTORULKLKQ==",
            "AutoUpdate": True,
            "NewVersionAvailable": False,
            "ProductType": "475"
        })
        device.connection_callback(False)
        connected = device.connect("192.168.0.2")
        self.assertFalse(connected)
        self.assertIsNone(device.state)
        self.assertEqual(device.network_device.name, "device-1")
        self.assertEqual(device.network_device.address, "192.168.0.2")
        self.assertEqual(device.network_device.port, 1883)
        self.assertEqual(mocked_connect.call_count, 1)
        self.assertEqual(mocked_loop_start.call_count, 1)
        self.assertEqual(mocked_loop_stop.call_count, 1)

    @mock.patch('libpurecool.zeroconf.Zeroconf.close')
    def test_connect_device_fail(self, mocked_close_zeroconf):
        device = DysonPureCoolLink({
            "Active": True,
            "Serial": "device-id-1",
            "Name": "device-1",
            "ScaleUnit": "SU01",
            "Version": "21.03.08",
            "LocalCredentials": "1/aJ5t52WvAfn+z+fjDuef86kQDQPefbQ6/"
                                "70ZGysII1Ke1i0ZHakFH84DZuxsSQ4KTT2v"
                                "bCm7uYeTORULKLKQ==",
            "AutoUpdate": True,
            "NewVersionAvailable": False,
            "ProductType": "475"
        })
        connected = device.auto_connect(retry=1, timeout=1)
        self.assertFalse(connected)
        self.assertEqual(mocked_close_zeroconf.call_count, 1)

    def test_status_topic(self):
        device = DysonPureCoolLink({
            "Active": True,
            "Serial": "device-id-1",
            "Name": "device-1",
            "ScaleUnit": "SU01",
            "Version": "21.03.08",
            "LocalCredentials": "1/aJ5t52WvAfn+z+fjDuef86kQDQPefbQ6/"
                                "70ZGysII1Ke1i0ZHakFH84DZuxsSQ4KTT2v"
                                "bCm7uYeTORULKLKQ==",
            "AutoUpdate": True,
            "NewVersionAvailable": False,
            "ProductType": "475"
        })
        self.assertEqual(device.status_topic, "475/device-id-1/status/current")

    @mock.patch('socket.inet_ntoa', )
    def test_device_dyson_listener(self, mocked_ntoa):
        listener = DysonPureCoolLink.DysonDeviceListener('serial-1',
                                                         on_add_device,
                                                         device_serial_from_name)
        zeroconf = Mock()
        listener.remove_service(zeroconf, "ptype", "serial-1")
        info = Mock()
        info.address = "192.168.0.1"
        zeroconf.get_service_info = Mock()
        zeroconf.get_service_info.return_value = info
        listener.add_service(zeroconf, '_dyson_mqtt._tcp.local.',
                             'ptype_serial-1._dyson_mqtt._tcp.local.')

    def test_on_connect(self):
        client = Mock()
        client.subscribe = Mock()
        userdata = Mock()
        userdata.status_topic = "ptype/serial/status/current"
        DysonPureCoolLink.on_connect(client, userdata, None, 0)
        userdata.connection_callback.assert_called_with(True)
        self.assertEqual(userdata.connection_callback.call_count, 1)
        client.subscribe.assert_called_with("ptype/serial/status/current")

    def test_on_connect_failed(self):
        userdata = Mock()
        userdata.product_type = 'ptype'
        userdata.serial = 'serial'
        DysonPureCoolLink.on_connect(None, userdata, None, 1)
        userdata.connection_callback.assert_called_with(False)
        self.assertEqual(userdata.connection_callback.call_count, 1)

    def test_add_message_listener(self):
        def on_message():
            pass

        def on_message_2():
            pass

        device = DysonPureCoolLink({
            "Active": True,
            "Serial": "device-id-1",
            "Name": "device-1",
            "ScaleUnit": "SU01",
            "Version": "21.03.08",
            "LocalCredentials": "1/aJ5t52WvAfn+z+fjDuef86kQDQPefbQ6/70ZGysII1K"
                                "e1i0ZHakFH84DZuxsSQ4KTT2vbCm7uYeTORULKLKQ==",
            "AutoUpdate": True,
            "NewVersionAvailable": False,
            "ProductType": "475"
        })
        device.add_message_listener(on_message)
        assert len(device.callback_message) == 1
        device.remove_message_listener(on_message)
        assert len(device.callback_message) == 0
        device.add_message_listener(on_message_2)
        device.add_message_listener(on_message)
        assert len(device.callback_message) == 2
        device.clear_message_listener()
        assert len(device.callback_message) == 0

    def test_on_message(self):
        def on_message(msg):
            assert isinstance(msg, DysonPureCoolState)
        device = DysonPureCoolLink({
            "Active": True,
            "Serial": "device-id-1",
            "Name": "device-1",
            "ScaleUnit": "SU01",
            "Version": "21.03.08",
            "LocalCredentials": "1/aJ5t52WvAfn+z+fjDuef86kQDQPefbQ6/"
                                "70ZGysII1Ke1i0ZHakFH84DZuxsSQ4KTT2v"
                                "bCm7uYeTORULKLKQ==",
            "AutoUpdate": True,
            "NewVersionAvailable": False,
            "ProductType": "475"
        })
        device.add_message_listener(on_message)
        msg = Mock()
        payload = open("tests/data/state.json", "r").read()
        msg.payload = Mock()
        msg.payload.decode.return_value = payload
        DysonPureCoolLink.on_message(None, device, msg)

    def test_on_message_hot(self):
        def on_message(msg):
            assert isinstance(msg, DysonPureHotCoolState)
        device = DysonPureCoolLink({
            "Active": True,
            "Serial": "device-id-1",
            "Name": "device-1",
            "ScaleUnit": "SU01",
            "Version": "21.03.08",
            "LocalCredentials": "1/aJ5t52WvAfn+z+fjDuef86kQDQPefbQ6/"
                                "70ZGysII1Ke1i0ZHakFH84DZuxsSQ4KTT2v"
                                "bCm7uYeTORULKLKQ==",
            "AutoUpdate": True,
            "NewVersionAvailable": False,
            "ProductType": "455"
        })
        device.add_message_listener(on_message)
        msg = Mock()
        payload = open("tests/data/state_hot.json", "r").read()
        msg.payload = Mock()
        msg.payload.decode.return_value = payload
        DysonPureCoolLink.on_message(None, device, msg)

    def test_on_message_sensor(self):
        def on_message(msg):
            assert isinstance(msg, DysonEnvironmentalSensorState)

        userdata = Mock()
        userdata.callback_message = [on_message]
        msg = Mock()
        payload = b'{"msg": "ENVIRONMENTAL-CURRENT-SENSOR-DATA","time":' \
                  b'"2017-06-17T23:05:49.001Z","data": '\
                  b'{"tact": "2967","hact": "0054","pact": "0004",' \
                  b'"vact": "0005","sltm": "0028"}}'
        msg.payload = payload
        DysonPureCoolLink.on_message(None, userdata, msg)

    def test_on_message_with_unknown_message(self):
        def on_message(msg):
            # Should not be called
            assert msg == 0

        userdata = Mock()
        userdata.callback_message = [on_message]
        msg = Mock()
        payload = b'{"msg": "ENVIRONMENTAL-CURRENT-SENSOR-DATAS","time":' \
                  b'"2017-06-17T23:05:49.001Z","data": ' \
                  b'{"tact": "2967","hact": "0054","pact": "0004",' \
                  b'"vact": "0005","sltm": "0028"}}'
        msg.payload = payload
        DysonPureCoolLink.on_message(None, userdata, msg)

    def test_on_message_without_callback(self):
        userdata = Mock()
        userdata.callback_message = []
        msg = Mock()
        payload = b'{"msg":"CURRENT-STATE","time":' \
                  b'"2017-02-19T15:00:18.000Z","mode-reason":"LAPP",' \
                  b'"state-reason":"MODE","dial":"OFF","rssi":"-58",' \
                  b'"product-state":{"fmod":"AUTO","fnst":"FAN",' \
                  b'"fnsp":"AUTO","qtar":"0004","oson":"OFF","rhtm":"ON",' \
                  b'"filf":"2159","ercd":"02C0","nmod":"ON","wacd":"NONE"},' \
                  b'"scheduler":{"srsc":"cbd0","dstv":"0001","tzid":"0001"}}'
        msg.payload = payload
        DysonPureCoolLink.on_message(None, userdata, msg)

    @mock.patch('paho.mqtt.client.Client.publish',
                side_effect=_mocked_request_state)
    @mock.patch('paho.mqtt.client.Client.connect')
    def test_request_state(self, mocked_connect, mocked_publish):
        device = DysonPureCoolLink({
            "Active": True,
            "Serial": "device-id-1",
            "Name": "device-1",
            "ScaleUnit": "SU01",
            "Version": "21.03.08",
            "LocalCredentials": "1/aJ5t52WvAfn+z+fjDuef86kQDQPefbQ6/70ZGysII1K"
                                "e1i0ZHakFH84DZuxsSQ4KTT2vbCm7uYeTORULKLKQ==",
            "AutoUpdate": True,
            "NewVersionAvailable": False,
            "ProductType": "475"
        })
        network_device = NetworkDevice('device-1', 'host', 1111)
        device.connection_callback(True)
        device._add_network_device(network_device)
        device.state_data_available()
        device.sensor_data_available()
        connected = device.connect(None)
        self.assertTrue(connected)
        self.assertEqual(mocked_connect.call_count, 1)
        self.assertEqual(mocked_publish.call_count, 2)
        device.request_current_state()
        self.assertEqual(mocked_publish.call_count, 3)
        device.request_environmental_state()
        self.assertEqual(mocked_publish.call_count, 4)
        device.disconnect()

    @mock.patch('paho.mqtt.client.Client.publish',
                side_effect=_mocked_request_state)
    @mock.patch('paho.mqtt.client.Client.connect')
    def test_dont_request_state_if_not_connected(self, mocked_connect,
                                                 mocked_publish):
        device = DysonPureCoolLink({
            "Active": True,
            "Serial": "device-id-1",
            "Name": "device-1",
            "ScaleUnit": "SU01",
            "Version": "21.03.08",
            "LocalCredentials": "1/aJ5t52WvAfn+z+fjDuef86kQDQPefbQ6/70ZGysII1K"
                                "e1i0ZHakFH84DZuxsSQ4KTT2vbCm7uYeTORULKLKQ==",
            "AutoUpdate": True,
            "NewVersionAvailable": False,
            "ProductType": "475"
        })
        network_device = NetworkDevice('device-1', 'host', 1111)
        device.connection_callback(False)
        device._add_network_device(network_device)
        connected = device.connect(None, "192.168.0.2")
        self.assertFalse(connected)
        self.assertEqual(mocked_connect.call_count, 1)
        device.request_current_state()
        self.assertEqual(mocked_publish.call_count, 0)
        device.request_environmental_state()
        self.assertEqual(mocked_publish.call_count, 0)

    @mock.patch('paho.mqtt.client.Client.publish',
                side_effect=_mocked_send_command)
    @mock.patch('paho.mqtt.client.Client.connect')
    def test_set_configuration(self, mocked_connect, mocked_publish):
        device = DysonPureCoolLink({
            "Active": True,
            "Serial": "device-id-1",
            "Name": "device-1",
            "ScaleUnit": "SU01",
            "Version": "21.03.08",
            "LocalCredentials": "1/aJ5t52WvAfn+z+fjDuef86kQDQPefbQ6/70ZGysII1K"
                                "e1i0ZHakFH84DZuxsSQ4KTT2vbCm7uYeTORULKLKQ==",
            "AutoUpdate": True,
            "NewVersionAvailable": False,
            "ProductType": Desk
        })
        network_device = NetworkDevice('device-1', 'host', 1111)
        device._add_network_device(network_device)
        device._current_state = DysonPureCoolState(
            open("tests/data/state.json", "r").read())
        device.connection_callback(True)
        device.state_data_available()
        device.sensor_data_available()
        connected = device.auto_connect()
        self.assertTrue(connected)
        self.assertEqual(mocked_connect.call_count, 1)
        device.set_configuration(fan_mode=FanMode.FAN,
                                 oscillation=Oscillation.OSCILLATION_ON,
                                 fan_speed=FanSpeed.FAN_SPEED_3,
                                 night_mode=NightMode.NIGHT_MODE_OFF,
                                 quality_target=QualityTarget.QUALITY_NORMAL,
                                 standby_monitoring=SM.STANDBY_MONITORING_ON
                                 )
        self.assertEqual(mocked_publish.call_count, 3)
        self.assertEqual(device.__repr__(),
                         "DysonPureCoolLink(serial=device-id-1,active=True,"
                         "name=device-1,version=21.03.08,auto_update=True,"
                         "new_version_available=False,product_type=469,"
                         "network_device=NetworkDevice(name=device-1,"
                         "address=host,port=1111))")
        device.disconnect()

    @mock.patch('paho.mqtt.client.Client.publish',
                side_effect=_mocked_send_command_hot)
    @mock.patch('paho.mqtt.client.Client.connect')
    def test_set_configuration_hot(self, mocked_connect, mocked_publish):
        device = DysonPureHotCoolLink({
            "Active": True,
            "Serial": "device-id-1",
            "Name": "device-1",
            "ScaleUnit": "SU01",
            "Version": "21.03.08",
            "LocalCredentials": "1/aJ5t52WvAfn+z+fjDuef86kQDQPefbQ6/70ZGysII1K"
                                "e1i0ZHakFH84DZuxsSQ4KTT2vbCm7uYeTORULKLKQ==",
            "AutoUpdate": True,
            "NewVersionAvailable": False,
            "ProductType": Hot
        })
        network_device = NetworkDevice('device-1', 'host', 1111)
        device._add_network_device(network_device)
        device._current_state = DysonPureCoolState(
            open("tests/data/state_hot.json", "r").read())
        device.connection_callback(True)
        device.state_data_available()
        device.sensor_data_available()
        connected = device.auto_connect()
        self.assertTrue(connected)
        self.assertEqual(mocked_connect.call_count, 1)
        device.set_configuration(fan_mode=FanMode.FAN,
                                 oscillation=Oscillation.OSCILLATION_ON,
                                 fan_speed=FanSpeed.FAN_SPEED_3,
                                 night_mode=NightMode.NIGHT_MODE_OFF,
                                 quality_target=QualityTarget.QUALITY_NORMAL,
                                 standby_monitoring=SM.STANDBY_MONITORING_ON,
                                 heat_mode=HeatMode.HEAT_ON,
                                 focus_mode=FocusMode.FOCUS_ON,
                                 heat_target=HeatTarget.celsius(25)
                                 )
        self.assertEqual(mocked_publish.call_count, 3)
        self.assertEqual(device.__repr__(),
                         "DysonPureHotCoolLink(serial=device-id-1,active=True,"
                         "name=device-1,version=21.03.08,auto_update=True,"
                         "new_version_available=False,product_type=455,"
                         "network_device=NetworkDevice(name=device-1,"
                         "address=host,port=1111))")
        device.disconnect()

    @mock.patch('paho.mqtt.client.Client.publish',
                side_effect=_mocked_send_command_rst_filter)
    @mock.patch('paho.mqtt.client.Client.connect')
    def test_set_configuration_rst_filter(self, mocked_connect,
                                          mocked_publish):
        device = DysonPureCoolLink({
            "Active": True,
            "Serial": "device-id-1",
            "Name": "device-1",
            "ScaleUnit": "SU01",
            "Version": "21.03.08",
            "LocalCredentials": "1/aJ5t52WvAfn+z+fjDuef86kQDQPefbQ6/70ZGysII1K"
                                "e1i0ZHakFH84DZuxsSQ4KTT2vbCm7uYeTORULKLKQ==",
            "AutoUpdate": True,
            "NewVersionAvailable": False,
            "ProductType": "475"
        })
        network_device = NetworkDevice('device-1', 'host', 1111)
        device._add_network_device(network_device)
        device._current_state = DysonPureCoolState(
            open("tests/data/state.json", "r").read())
        device.connection_callback(True)
        device.state_data_available()
        device.sensor_data_available()
        connected = device.auto_connect()
        self.assertTrue(connected)
        self.assertEqual(mocked_connect.call_count, 1)
        device.set_configuration(fan_mode=FanMode.FAN,
                                 oscillation=Oscillation.OSCILLATION_ON,
                                 fan_speed=FanSpeed.FAN_SPEED_3,
                                 night_mode=NightMode.NIGHT_MODE_OFF,
                                 quality_target=QualityTarget.QUALITY_NORMAL,
                                 standby_monitoring=SM.STANDBY_MONITORING_ON,
                                 reset_filter=ResetFilter.RESET_FILTER
                                 )
        self.assertEqual(mocked_publish.call_count, 3)
        self.assertEqual(device.__repr__(),
                         "DysonPureCoolLink(serial=device-id-1,active=True,"
                         "name=device-1,version=21.03.08,auto_update=True,"
                         "new_version_available=False,product_type=475,"
                         "network_device=NetworkDevice(name=device-1,"
                         "address=host,port=1111))")
        device.disconnect()

    @mock.patch('paho.mqtt.client.Client.publish',
                side_effect=_mocked_send_command_timer)
    @mock.patch('paho.mqtt.client.Client.connect')
    def test_set_configuration_timer(self, mocked_connect, mocked_publish):
        device = DysonPureCoolLink({
            "Active": True,
            "Serial": "device-id-1",
            "Name": "device-1",
            "ScaleUnit": "SU01",
            "Version": "21.03.08",
            "LocalCredentials": "1/aJ5t52WvAfn+z+fjDuef86kQDQPefbQ6/70ZGysII1K"
                                "e1i0ZHakFH84DZuxsSQ4KTT2vbCm7uYeTORULKLKQ==",
            "AutoUpdate": True,
            "NewVersionAvailable": False,
            "ProductType": "475"
        })
        network_device = NetworkDevice('device-1', 'host', 1111)
        device._add_network_device(network_device)
        device._current_state = DysonPureCoolState(
            open("tests/data/state.json", "r").read())
        device.connection_callback(True)
        device.state_data_available()
        device.sensor_data_available()
        connected = device.auto_connect()
        self.assertTrue(connected)
        self.assertEqual(mocked_connect.call_count, 1)
        device.set_configuration(sleep_timer=10)
        self.assertEqual(mocked_publish.call_count, 3)
        self.assertEqual(device.__repr__(),
                         "DysonPureCoolLink(serial=device-id-1,active=True,"
                         "name=device-1,version=21.03.08,auto_update=True,"
                         "new_version_available=False,product_type=475,"
                         "network_device=NetworkDevice(name=device-1,"
                         "address=host,port=1111))")
        device.disconnect()

    @mock.patch('paho.mqtt.client.Client.publish',
                side_effect=_mocked_send_command_timer_off)
    @mock.patch('paho.mqtt.client.Client.connect')
    def test_set_configuration_timer_off(self, mocked_connect, mocked_publish):
        device = DysonPureCoolLink({
            "Active": True,
            "Serial": "device-id-1",
            "Name": "device-1",
            "ScaleUnit": "SU01",
            "Version": "21.03.08",
            "LocalCredentials": "1/aJ5t52WvAfn+z+fjDuef86kQDQPefbQ6/70ZGysII1K"
                                "e1i0ZHakFH84DZuxsSQ4KTT2vbCm7uYeTORULKLKQ==",
            "AutoUpdate": True,
            "NewVersionAvailable": False,
            "ProductType": "475"
        })
        network_device = NetworkDevice('device-1', 'host', 1111)
        device._add_network_device(network_device)
        device._current_state = DysonPureCoolState(
            open("tests/data/state.json", "r").read())
        device.connection_callback(True)
        device.state_data_available()
        device.sensor_data_available()
        connected = device.auto_connect()
        self.assertTrue(connected)
        self.assertEqual(mocked_connect.call_count, 1)
        device.set_configuration(sleep_timer=0)
        self.assertEqual(mocked_publish.call_count, 3)
        self.assertEqual(device.__repr__(),
                         "DysonPureCoolLink(serial=device-id-1,active=True,"
                         "name=device-1,version=21.03.08,auto_update=True,"
                         "new_version_available=False,product_type=475,"
                         "network_device=NetworkDevice(name=device-1,"
                         "address=host,port=1111))")
        device.disconnect()

    @mock.patch('paho.mqtt.client.Client.publish',
                side_effect=_mocked_send_command)
    @mock.patch('paho.mqtt.client.Client.connect')
    def test_dont_set_configuration_if_not_connected(self, mocked_connect,
                                                     mocked_publish):
        device = DysonPureCoolLink({
            "Active": True,
            "Serial": "device-id-1",
            "Name": "device-1",
            "ScaleUnit": "SU01",
            "Version": "21.03.08",
            "LocalCredentials": "1/aJ5t52WvAfn+z+fjDuef86kQDQPefbQ6/70ZGysII1K"
                                "e1i0ZHakFH84DZuxsSQ4KTT2vbCm7uYeTORULKLKQ==",
            "AutoUpdate": True,
            "NewVersionAvailable": False,
            "ProductType": "475"
        })
        network_device = NetworkDevice('device-1', 'host', 1111)
        device._add_network_device(network_device)
        device._current_state = DysonPureCoolState(
            open("tests/data/state.json", "r").read())
        device.connection_callback(False)
        connected = device.auto_connect()
        self.assertFalse(connected)
        self.assertEqual(mocked_connect.call_count, 1)
        device.set_configuration(fan_mode=FanMode.FAN,
                                 oscillation=Oscillation.OSCILLATION_ON,
                                 fan_speed=FanSpeed.FAN_SPEED_3,
                                 night_mode=NightMode.NIGHT_MODE_OFF)
        self.assertEqual(mocked_publish.call_count, 0)
        self.assertEqual(device.__repr__(),
                         "DysonPureCoolLink(serial=device-id-1,active=True,"
                         "name=device-1,version=21.03.08,auto_update=True,"
                         "new_version_available=False,product_type=475,"
                         "network_device=NetworkDevice(name=device-1,"
                         "address=host,port=1111))")

    def test_network_device(self):
        device = NetworkDevice("device", "192.168.1.1", "8090")
        self.assertEqual(device.name, "device")
        self.assertEqual(device.address, "192.168.1.1")
        self.assertEqual(device.port, "8090")
        self.assertEqual(device.__repr__(),
                         "NetworkDevice(name=device,address=192.168.1.1,"
                         "port=8090)")

    def test_dyson_state(self):
        dyson_state = DysonPureCoolState(
            open("tests/data/state.json", "r").read())
        self.assertEqual(dyson_state.fan_mode, FanMode.AUTO.value)
        self.assertEqual(dyson_state.fan_state, FanState.FAN_ON.value)
        self.assertEqual(dyson_state.night_mode, NightMode.NIGHT_MODE_ON.value)
        self.assertEqual(dyson_state.speed, FanSpeed.FAN_SPEED_AUTO.value)
        self.assertEqual(dyson_state.oscillation,
                         Oscillation.OSCILLATION_OFF.value)
        self.assertEqual(dyson_state.filter_life, '2087')
        self.assertEqual(dyson_state.__repr__(),
                         "DysonPureCoolState(fan_mode=AUTO,fan_state=FAN,"
                         "night_mode=ON,speed=AUTO,oscillation=OFF,"
                         "filter_life=2087,quality_target=0004,"
                         "standby_monitoring=ON)")
        self.assertEqual(dyson_state.quality_target,
                         QualityTarget.QUALITY_NORMAL.value)
        self.assertEqual(dyson_state.standby_monitoring,
                         SM.STANDBY_MONITORING_ON.value)

    def test_dyson_state_hot(self):
        dyson_state = DysonPureHotCoolState(
            open("tests/data/state_hot.json", "r").read())
        self.assertEqual(dyson_state.fan_mode, FanMode.AUTO.value)
        self.assertEqual(dyson_state.fan_state, FanState.FAN_ON.value)
        self.assertEqual(dyson_state.night_mode, NightMode.NIGHT_MODE_ON.value)
        self.assertEqual(dyson_state.speed, FanSpeed.FAN_SPEED_AUTO.value)
        self.assertEqual(dyson_state.oscillation,
                         Oscillation.OSCILLATION_OFF.value)
        self.assertEqual(dyson_state.filter_life, '2087')
        self.assertEqual(dyson_state.heat_mode, HeatMode.HEAT_ON.value)
        self.assertEqual(dyson_state.heat_state, HeatState.HEAT_STATE_ON.value)
        self.assertEqual(dyson_state.tilt, TiltState.TILT_FALSE.value)
        self.assertEqual(dyson_state.focus_mode, FocusMode.FOCUS_ON.value)
        self.assertEqual(dyson_state.heat_target, '2950')
        self.assertEqual(dyson_state.__repr__(),
                         "DysonHotCoolState(fan_mode=AUTO,fan_state=FAN,"
                         "night_mode=ON,speed=AUTO,oscillation=OFF,"
                         "filter_life=2087,quality_target=0004,"
                         "standby_monitoring=ON,tilt=OK,focus_mode=ON,"
                         "heat_mode=HEAT,heat_target=2950,heat_state=HEAT)")
        self.assertEqual(dyson_state.quality_target,
                         QualityTarget.QUALITY_NORMAL.value)
        self.assertEqual(dyson_state.standby_monitoring,
                         SM.STANDBY_MONITORING_ON.value)

    def test_sensor_state(self):
        sensor_state = DysonEnvironmentalSensorState(
            open("tests/data/sensor.json", "r").read())
        self.assertEqual(sensor_state.sleep_timer, 28)
        self.assertEqual(sensor_state.dust, 4)
        self.assertEqual(sensor_state.humidity, 54)
        self.assertEqual(sensor_state.temperature, 296.7)
        self.assertEqual(sensor_state.volatil_organic_compounds, 5)
        self.assertEqual(sensor_state.__repr__(),
                         "DysonEnvironmentalSensorState(humidity=54,"
                         "air quality=5,temperature=296.7,"
                         "dust=4,sleep_timer=28)")

    def test_sensor_state_sleep_timer_off(self):
        sensor_state = DysonEnvironmentalSensorState(
            open("tests/data/sensor_sltm_off.json", "r").read())
        self.assertEqual(sensor_state.sleep_timer, 0)
        self.assertEqual(sensor_state.dust, 4)
        self.assertEqual(sensor_state.humidity, 54)
        self.assertEqual(sensor_state.temperature, 296.7)
        self.assertEqual(sensor_state.volatil_organic_compounds, 5)

    def test_heat_target_celsius(self):
        self.assertEqual(HeatTarget.celsius(25), "2980")
        self.assertEqual(HeatTarget.celsius(25.5), "2985")

        with self.assertRaises(DysonInvalidTargetTemperatureException) as ex:
            HeatTarget.celsius(38)
        invalid_target_exception = ex.exception
        self.assertEqual(invalid_target_exception.temperature_unit,
                         DysonInvalidTargetTemperatureException.CELSIUS)
        self.assertEqual(invalid_target_exception.current_value, 38)
        self.assertEqual(invalid_target_exception.__repr__(),
                         "38 is not a valid temperature target. "
                         "It must be between 1 to 37 inclusive.")

    def test_heat_target_fahrenheit(self):
        self.assertEqual(HeatTarget.fahrenheit(77), "2980")

        with self.assertRaises(DysonInvalidTargetTemperatureException) as ex:
            HeatTarget.fahrenheit(99)
        invalid_target_exception = ex.exception
        self.assertEqual(invalid_target_exception.temperature_unit,
                         DysonInvalidTargetTemperatureException.FAHRENHEIT)
        self.assertEqual(invalid_target_exception.current_value, 99)
        self.assertEqual(invalid_target_exception.__repr__(),
                         "99 is not a valid temperature target. "
                         "It must be between 34 to 98 inclusive.")

    def test_device_connected(self):
        device = DysonPureCoolLink({
            "Active": True,
            "Serial": "device-id-1",
            "Name": "device-1",
            "ScaleUnit": "SU01",
            "Version": "21.03.08",
            "LocalCredentials": "1/aJ5t52WvAfn+z+fjDuef86kQDQPefbQ6/70ZGysII1K"
                                "e1i0ZHakFH84DZuxsSQ4KTT2vbCm7uYeTORULKLKQ==",
            "AutoUpdate": True,
            "NewVersionAvailable": False,
            "ProductType": "475"
        })
        device.connected = True
        self.assertTrue(device.connected)
        device.connected = False
        self.assertFalse(device.connected)

    def test_environment_state(self):
        device = DysonPureCoolLink({
            "Active": True,
            "Serial": "device-id-1",
            "Name": "device-1",
            "ScaleUnit": "SU01",
            "Version": "21.03.08",
            "LocalCredentials": "1/aJ5t52WvAfn+z+fjDuef86kQDQPefbQ6/70ZGysII1K"
                                "e1i0ZHakFH84DZuxsSQ4KTT2vbCm7uYeTORULKLKQ==",
            "AutoUpdate": True,
            "NewVersionAvailable": False,
            "ProductType": "475"
        })
        sensor_state = DysonEnvironmentalSensorState(
            open("tests/data/sensor.json", "r").read())
        device.environmental_state = sensor_state
        self.assertEqual(device.environmental_state.dust, 4)
