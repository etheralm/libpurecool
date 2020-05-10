"""Dyson new v2 pure Humidify+Cool device."""

import logging

from .const import HeatMode, HumidifierState, HumidifierAuto
from .dyson_pure_cool import DysonPureCool
from .utils import printable_fields

_LOGGER = logging.getLogger(__name__)


class DysonPureHumidifyCool(DysonPureCool):
    """Dyson new Pure Humidify+Cool device."""

    def _parse_command_args(self, **kwargs):
        """Parse command arguments.

        :param kwargs Arguments
        :return payload dictionary
        """
        data = super()._parse_command_args(**kwargs)

        humidifier_state = kwargs.get('humidifier_state')
        humidifier_auto = kwargs.get('humidifier_auto')
        humidity_target = kwargs.get('humidity_target')

        f_humidifier_state = humidifier_state.value if humidifier_state \
            else self._current_state.humidifier_state
        f_humidifier_auto = humidifier_auto.value if humidifier_auto \
            else self._current_state.humidifier_auto
        f_humidity_target = humidity_target if humidity_target \
            else self._current_state.humidity_target

        data["hume"] = f_humidifier_state
        data["haut"] = f_humidifier_auto
        data["humt"] = f_humidity_target

        return data

    def enable_humidifier(self):
        """Turn on humidifier."""
        data = {
            "hume": HumidifierState.HUMIDIFIER_ON.value
        }

        self.set_fan_configuration(data)


    def disable_humidifier(self):
        """Turn off humidifier."""
        data = {
            "hume": HumidifierState.HUMIDIFIER_OFF.value
        }

        self.set_fan_configuration(data)

    def enable_humidifier_auto(self):
        """Turn on humidifier auto mode."""
        data = {
            "haut": HumidifierAuto.HUMIDIFIER_AUTO_ON.value
        }

        self.set_fan_configuration(data)

    def disable_humidifier_auto(self):
        """Turn off humidifier auto mode."""
        data = {
            "haut": HumidifierAuto.HUMIDIFIER_AUTO_OFF.value
        }

        self.set_fan_configuration(data)

    def set_humidity_target(self, humidity):
        """Set humidifier target humidity
        
        Humidity must be an int between 0 and 100

        :param humidity: int between 0 and 100. Humidity Target
        ."""

        if not isinstance(humidity, int):
            raise TypeError('humidity must be an int')

        if not 0 <= humidity <= 100:
            raise ValueError('humidity must be '
                             'between 0 and 100')

        data = {
            "humt": str(humidity).rjust(4, '0')
        }

        self.set_fan_configuration(data)

    def __repr__(self):
        """Return a String representation."""
        fields = self._fields()
        return 'DysonPureHumidifyCool(' + ",".join(
            printable_fields(fields)) + ')'
