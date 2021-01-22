from libpurecool.dyson_360_eye import Dyson360Eye
import pytest
import socket
from libpurecool.zeroconf import ServiceInfo, Zeroconf
from unittest import mock
from unittest.mock import MagicMock

from libpurecool.dyson_pure_cool_link import DysonPureCoolLink

IP_ADDRESS = "192.168.1.2"
SERIAL = "XXX-XX-XXXXXXXX"


def _mocked_zeroconf():
    def _get_service_info(*args):
        service_info = MagicMock(spec=ServiceInfo)
        service_info.address = socket.inet_aton(IP_ADDRESS)
        service_info.port = 1883
        return service_info

    zeroconf = MagicMock(spec=Zeroconf)
    zeroconf.get_service_info = MagicMock(side_effect=_get_service_info)
    return zeroconf


def _get_mocked_service_browser(serial):
    def _mocked_service_browser(zeroconf, type, listener):
        listener.add_service(zeroconf, type, "{}.{}".format(serial, type))
    return _mocked_service_browser


@pytest.mark.parametrize(
    "device_class,serial_prefix",
    [
        (DysonPureCoolLink, "PURE-COOL-LINK_"),
        (Dyson360Eye, "360EYE-"),
    ]
)
def test_auto_connect(device_class, serial_prefix):
    with mock.patch(
        'libpurecool.dyson_device.ServiceBrowser',
        side_effect=_get_mocked_service_browser(serial_prefix + SERIAL),
    ), mock.patch(
        'libpurecool.dyson_device.Zeroconf',
        side_effect=_mocked_zeroconf,
    ), mock.patch('paho.mqtt.client.Client'):
        device = device_class({
            "Active": True,
            "Serial": SERIAL,
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
        device.state_data_available()
        if hasattr(device, "sensor_data_available"):
            device.sensor_data_available()
        device.connection_callback(True)
        connected = device.auto_connect()
        assert connected is True
        assert device.state is None
        if hasattr(device, "disconnect"):
            device.disconnect()
