"""Dyson pure cool device."""

# pylint: disable=too-many-locals

from .const import FanPower, \
    SLEEP_TIMER_OFF, FanSpeed, FrontalDirection, AutoMode, \
    NightMode, OscillationV2
from .dyson_pure_cool_link import DysonPureCoolLink
from .utils import printable_fields


class DysonPureCool(DysonPureCoolLink):
    """Dyson pure cool device."""

    def _parse_command_args(self, **kwargs):
        """Parse command arguments.

        :param kwargs Arguments
        :return payload dictionary
        """
        fan_power = kwargs.get('fan_power')
        front_direction = kwargs.get('front_direction')
        auto_mode = kwargs.get('auto_mode')
        oscillation = kwargs.get('oscillation')
        night_mode = kwargs.get('night_mode')
        continuous_monitoring = kwargs.get('continuous_monitoring')
        fan_speed = kwargs.get('fan_speed')
        sleep_timer = kwargs.get('sleep_timer')
        oscillation_angle_low = kwargs.get('oscillation_angle_low')
        oscillation_angle_high = kwargs.get('oscillation_angle_high')
        reset_filter = kwargs.get('reset_filter')

        f_power = fan_power.value if fan_power \
            else self._current_state.fan_power
        f_front_direction = front_direction.value if front_direction \
            else self._current_state.front_direction
        f_auto_mode = auto_mode.value if auto_mode \
            else self._current_state.auto_mode
        f_oscillation = oscillation.value if oscillation \
            else self._current_state.oscillation
        f_night_mode = night_mode.value if night_mode \
            else self._current_state.night_mode
        f_continuous_monitoring = continuous_monitoring.value if \
            continuous_monitoring \
            else self._current_state.continuous_monitoring
        f_speed = fan_speed.value if fan_speed \
            else self._current_state.speed
        f_sleep_timer = str(sleep_timer) if sleep_timer or isinstance(
            sleep_timer, int) else "STET"
        f_oscillation_angle_low = str(oscillation_angle_low) \
            if oscillation_angle_low \
            else self._current_state.oscillation_angle_low
        f_oscillation_angle_high = str(oscillation_angle_high) \
            if oscillation_angle_high \
            else self._current_state.oscillation_angle_high
        f_reset_filter = reset_filter.value if reset_filter \
            else "STET"

        return {
            "fpwr": f_power,
            "fdir": f_front_direction,
            "auto": f_auto_mode,  # sleep timer
            "oson": f_oscillation,  # monitor air quality
            "nmod": f_night_mode,  # monitor air quality
            "rhtm": f_continuous_monitoring,  # monitor air quality
            "fnsp": f_speed,  # monitor air quality
            "sltm": f_sleep_timer,  # monitor air quality
            "ancp": "CUST",
            "osal": f_oscillation_angle_low,  # monitor air quality
            "osau": f_oscillation_angle_high,  # monitor air quality
            # when inactive
            "rstf": f_reset_filter,  # reset filter lifecycle
        }

    def turn_on(self):
        """Turn off the fan."""
        data = {
            "fpwr": FanPower.POWER_ON.value
        }
        self.set_fan_configuration(data)

    def turn_off(self):
        """Turn on the fan."""
        data = {
            "fpwr": FanPower.POWER_OFF.value
        }
        self.set_fan_configuration(data)

    def enable_oscillation(self,
                           oscillation_angle_low=None,
                           oscillation_angle_high=None):
        """Enable oscillation.

        Both angle arguments represent degrees.
        They must be ints between 5 and 355.
        The high angle must either be equal or
        30 bigger than the low one.
        If any of the arguments are empty it will
        use the previously set values.

        :param oscillation_angle_low: int between 5 and 355.
                                       High angle of oscillation. Can be empty
        :param oscillation_angle_high: int between 5 and 355.
                                       Low angle of oscillation. Can be empty
        """
        if not oscillation_angle_low:
            oscillation_angle_low = \
                int(self._current_state.oscillation_angle_low)
        if not oscillation_angle_high:
            oscillation_angle_high = \
                int(self._current_state.oscillation_angle_high)

        if not isinstance(oscillation_angle_low, int):
            raise TypeError('oscillation_angle_low must be an int')
        if not isinstance(oscillation_angle_high, int):
            raise TypeError('oscillation_angle_high must be an int')

        if not 5 <= oscillation_angle_low <= 355:
            raise ValueError('oscillation_angle_low must be '
                             'between 5 and 355')
        if not 5 <= oscillation_angle_high <= 355:
            raise ValueError('oscillation_angle_high must be '
                             'between 5 and 355')

        if oscillation_angle_high < oscillation_angle_low:
            raise ValueError('oscillation_angle_high must be equal '
                             'or bigger than oscillation_angle_low')
        if oscillation_angle_high != oscillation_angle_low and \
                oscillation_angle_high - oscillation_angle_low < 30:
            raise ValueError('oscillation_angle_high must be be bigger '
                             'than oscillation_angle_low by at least 30')

        data = {
            "oson": OscillationV2.OSCILLATION_ON.value,
            "fpwr": FanPower.POWER_ON.value,
            "ancp": "CUST",
            "osal": str(oscillation_angle_low).rjust(4, '0'),
            "osau": str(oscillation_angle_high).rjust(4, '0'),
        }
        self.set_fan_configuration(data)

    def disable_oscillation(self):
        """Disable oscillation."""
        data = {
            "oson": OscillationV2.OSCILLATION_OFF.value
        }
        self.set_fan_configuration(data)

    def enable_sleep_timer(self, duration):
        """Enable the sleep timer.

        :param duration: int between 1 and 540 representing minutes
        """
        if not isinstance(duration, int):
            raise TypeError('duration must be an int')
        if not 0 < duration <= 540:
            raise ValueError('duration must be between 1 and 540')

        data = {
            "sltm": str(duration).rjust(4, '0')
        }

        self.set_fan_configuration(data)

    def disable_sleep_timer(self):
        """Disable the sleep timer."""
        data = {
            "sltm": SLEEP_TIMER_OFF
        }

        self.set_fan_configuration(data)

    def set_fan_speed(self, fan_speed):
        """Set the fan speed.

        :param fan_speed: FanSpeed to set (const.FanSpeed)
        :return:
        """
        if not isinstance(fan_speed, FanSpeed):
            raise TypeError('fan_speed must be a FanSpeed enumeration')

        data = {
            "fnsp": fan_speed.value
        }

        self.set_fan_configuration(data)

    def enable_frontal_direction(self):
        """Enable frontal direction."""
        data = {
            "fdir": FrontalDirection.FRONTAL_ON.value
        }

        self.set_fan_configuration(data)

    def disable_frontal_direction(self):
        """Disable frontal direction."""
        data = {
            "fdir": FrontalDirection.FRONTAL_OFF.value
        }

        self.set_fan_configuration(data)

    def enable_auto_mode(self):
        """Enable auto mode."""
        data = {
            "auto": AutoMode.AUTO_ON.value
        }

        self.set_fan_configuration(data)

    def disable_auto_mode(self):
        """Disable auto mode."""
        data = {
            "auto": AutoMode.AUTO_OFF.value
        }

        self.set_fan_configuration(data)

    def enable_night_mode(self):
        """Enable night mode."""
        data = {
            "nmod": NightMode.NIGHT_MODE_ON.value
        }

        self.set_fan_configuration(data)

    def disable_night_mode(self):
        """Disable night mode."""
        data = {
            "nmod": NightMode.NIGHT_MODE_OFF.value
        }

        self.set_fan_configuration(data)

    def __repr__(self):
        """Return a String representation."""
        fields = self._fields()
        return 'DysonPureCool(' + ",".join(
            printable_fields(fields)) + ')'
