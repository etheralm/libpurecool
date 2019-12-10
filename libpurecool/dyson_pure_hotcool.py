"""Dyson new v2 pure Hot+Cool device."""

import logging

from .const import HeatMode
from .dyson_pure_cool import DysonPureCool
from .utils import printable_fields

_LOGGER = logging.getLogger(__name__)


class DysonPureHotCool(DysonPureCool):
    """Dyson new Pure Hot+Cool device."""

    def _parse_command_args(self, **kwargs):
        """Parse command arguments.

        :param kwargs Arguments
        :return payload dictionary
        """
        data = super()._parse_command_args(**kwargs)

        heat_target = kwargs.get('heat_target')
        heat_mode = kwargs.get('heat_mode')

        f_heat_target = heat_target if heat_target \
            else self._current_state.heat_target
        f_heat_mode = heat_mode.value if heat_mode \
            else self._current_state.heat_mode

        data["hmax"] = f_heat_target
        data["hmod"] = f_heat_mode

        return data

    def enable_heat_mode(self):
        """Turn on head mode."""
        data = {
            "hmod": HeatMode.HEAT_ON.value
        }

        self.set_fan_configuration(data)

    def disable_heat_mode(self):
        """Turn off head mode."""
        data = {
            "hmod": HeatMode.HEAT_OFF.value
        }

        self.set_fan_configuration(data)

    def set_heat_target(self, heat_target):
        """Set temperature target.

        Use either const.HeatTarget.celsius or const.HeatTarget.fahrenheit
        to get a string representation of the target temperature in kelvins.

        ex. set_heat_target(const.HeatTarget.celsius(24))

        :param heat_target: target temperature in Kalvin
        """
        data = {
            "hmax": heat_target
        }

        self.set_fan_configuration(data)

    def __repr__(self):
        """Return a String representation."""
        fields = self._fields()
        return 'DysonPureHotCool(' + ",".join(
            printable_fields(fields)) + ')'
