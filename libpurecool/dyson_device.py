"""Base Dyson devices."""

# pylint: disable=too-many-public-methods,too-many-instance-attributes

from queue import Queue, Empty
import logging
import json
import abc
import time
import socket

from .utils import printable_fields
from .utils import decrypt_password
from .zeroconf import ServiceBrowser, Zeroconf

_LOGGER = logging.getLogger(__name__)

MQTT_RETURN_CODES = {
    0: "Connection successful",
    1: "Connection refused - incorrect protocol version",
    2: "Connection refused - invalid client identifier",
    3: "Connection refused - server unavailable",
    4: "Connection refused - bad username or password",
    5: "Connection refused - not authorised"
}

DEFAULT_PORT = 1883


class NetworkDevice:
    """Network device."""

    def __init__(self, name, address, port):
        """Create a new network device.

        :param name: Device name
        :param address: Device address
        :param port: Device port
        """
        self._name = name
        self._address = address
        self._port = port

    @property
    def name(self):
        """Device name."""
        return self._name

    @property
    def address(self):
        """Device address."""
        return self._address

    @property
    def port(self):
        """Device port."""
        return self._port

    def __repr__(self):
        """Return a String representation."""
        fields = [("name", self.name), ("address", self.address),
                  ("port", str(self.port))]
        return 'NetworkDevice(' + ",".join(printable_fields(fields)) + ')'


class DysonDevice:
    """Abstract Dyson device."""

    class DysonDeviceListener:
        """Message listener."""

        def __init__(self, serial, add_device_function, serial_from_name):
            """Create a new message listener.

            :param serial: Device serial
            :param add_device_function: Callback function
            """
            self._serial = serial
            self.add_device_function = add_device_function
            self.serial_from_name = serial_from_name

        def remove_service(self, zeroconf, device_type, name):
            # pylint: disable=unused-argument,no-self-use
            """Remove listener."""
            _LOGGER.info("Service %s removed", name)

        def add_service(self, zeroconf, device_type, name):
            """Add device.

            :param zeroconf: MSDNS object
            :param device_type: Service type
            :param name: Device name
            """
            device_serial = self.serial_from_name(name)
            if device_serial == self._serial:
                # Find searched device
                info = zeroconf.get_service_info(device_type, name)
                address = socket.inet_ntoa(info.address)
                network_device = NetworkDevice(device_serial, address,
                                               info.port)
                self.add_device_function(network_device)
                zeroconf.close()

    @staticmethod
    def on_connect(client, userdata, flags, return_code):
        # pylint: disable=unused-argument
        """Set function callback when connected."""
        if return_code == 0:
            _LOGGER.debug("Connected with result code: %s", return_code)
            client.subscribe(userdata.status_topic)

            userdata.connection_callback(True)
        else:
            _LOGGER.error("Connection error: %s",
                          MQTT_RETURN_CODES[return_code])
            userdata.connection_callback(False)

    def __init__(self, json_body):
        """Create a new Dyson device.

        :param json_body: JSON message returned by the HTTPS API
        """
        if 'Active' in json_body:
            self._active = json_body['Active']
        else:
            self._active = None
        self._serial = json_body['Serial']
        self._name = json_body['Name']
        self._version = json_body['Version']
        self._credentials = decrypt_password(json_body['LocalCredentials'])
        self._auto_update = json_body['AutoUpdate']
        self._new_version_available = json_body['NewVersionAvailable']
        self._product_type = json_body['ProductType']
        self._network_device = None
        self._connected = False
        self._mqtt = None
        self._callback_message = []
        self._device_available = False
        self._current_state = None
        self._state_data_available = Queue()

        self._search_device_queue = Queue()
        self._connection_queue = Queue()

    def connection_callback(self, connected):
        """Set function called when device is connected."""
        self._connection_queue.put_nowait(connected)

    def connect(self, device_ip, device_port=DEFAULT_PORT):
        """Connect to the device using ip address.

        :param device_ip: Device IP address
        :param device_port: Device Port (default: 1883)
        :return: True if connected, else False
        """
        self._network_device = NetworkDevice(self._name, device_ip,
                                             device_port)

        return self._mqtt_connect()

    def _auto_connect(self, type_, timeout=5, retry=15):
        """Try to connect to device using mDNS."""
        for i in range(retry):
            zeroconf = Zeroconf()
            listener = self.DysonDeviceListener(self._serial,
                                                self._add_network_device,
                                                self._device_serial_from_name)
            ServiceBrowser(zeroconf, type_, listener)
            try:
                self._network_device = self._search_device_queue.get(
                    timeout=timeout)
            except Empty:
                # Unable to find device
                _LOGGER.warning("Unable to find device %s, try %s",
                                self._serial, i)
                zeroconf.close()
            else:
                break
        if self._network_device is None:
            _LOGGER.error("Unable to connect to device %s", self._serial)
            return False
        return self._mqtt_connect()

    @abc.abstractmethod
    def _mqtt_connect(self):
        """Connect to the MQTT broker."""
        return

    @staticmethod
    @abc.abstractmethod
    def _device_serial_from_name(name):
        """Get device serial from mDNS name."""
        return

    @property
    @abc.abstractmethod
    def status_topic(self):
        """MQTT status topic."""
        return

    @property
    def command_topic(self):
        """MQTT command topic."""
        return "{0}/{1}/command".format(self._product_type, self._serial)

    def request_current_state(self):
        """Request new state message."""
        if self._connected:
            payload = {
                "msg": "REQUEST-CURRENT-STATE",
                "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
            self._mqtt.publish(self.command_topic, json.dumps(payload))
        else:
            _LOGGER.warning(
                "Unable to send commands because device %s is not connected",
                self.serial)

    @property
    def state(self):
        """Device state."""
        return self._current_state

    @state.setter
    def state(self, value):
        """Set current state."""
        self._current_state = value

    @property
    def active(self):
        """Active status."""
        return self._active

    @property
    def serial(self):
        """Device serial."""
        return self._serial

    @property
    def name(self):
        """Device name."""
        return self._name

    @property
    def version(self):
        """Device version."""
        return self._version

    @property
    def credentials(self):
        """Device encrypted credentials."""
        return self._credentials

    @property
    def auto_update(self):
        """Auto update configuration."""
        return self._auto_update

    @property
    def new_version_available(self):
        """Return if new version available."""
        return self._new_version_available

    @property
    def product_type(self):
        """Product type."""
        return self._product_type

    @property
    def network_device(self):
        """Network device."""
        return self._network_device

    def _add_network_device(self, network_device):
        """Add network device.

        :param network_device: Network device
        """
        self._search_device_queue.put_nowait(network_device)

    @property
    def callback_message(self):
        """Return callback functions when message are received."""
        return self._callback_message

    def add_message_listener(self, callback_message):
        """Add message listener."""
        self._callback_message.append(callback_message)

    def remove_message_listener(self, callback_message):
        """Remove a message listener."""
        if callback_message in self._callback_message:
            self.callback_message.remove(callback_message)

    def clear_message_listener(self):
        """Clear all message listener."""
        self.callback_message.clear()

    @property
    def device_available(self):
        """Return True if device is fully available, else false."""
        return self._device_available

    def state_data_available(self):
        """Call when first state data are available. Internal method."""
        _LOGGER.debug("State data available for device %s", self._serial)
        self._state_data_available.put_nowait(True)

    def _fields(self):
        """Return list of field tuples."""
        fields = [("serial", self.serial), ("active", str(self.active)),
                  ("name", self.name), ("version", self.version),
                  ("auto_update", str(self.auto_update)),
                  ("new_version_available", str(self.new_version_available)),
                  ("product_type", self.product_type),
                  ("network_device", str(self.network_device))]
        return fields
