from libpurecoollink.dyson_pure_cool_link import DysonPureCoolLink
from libpurecoollink.utils import printable_fields


class DysonPureCool(DysonPureCoolLink):

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
            continuous_monitoring else self._current_state.continuous_monitoring
        f_speed = fan_speed.value if fan_speed \
            else self._current_state.speed
        f_sleep_timer = sleep_timer if sleep_timer or isinstance(
            sleep_timer, int) else "STET"
        f_oscillation_angle_low = oscillation_angle_low \
            if oscillation_angle_low else self._current_state.oscillation_angle_low
        f_oscillation_angle_high = oscillation_angle_high \
            if oscillation_angle_high else self._current_state.oscillation_angle_high
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
            "osal": f_oscillation_angle_low,  # monitor air quality
            "osau": f_oscillation_angle_high,  # monitor air quality
            # when inactive
            "rstf": f_reset_filter,  # reset filter lifecycle
        }

    def set_configuration(self, **kwargs):
        """Configure fan.

        :param kwargs: Parameters
        """
        data = self._parse_command_args(**kwargs)
        self.set_fan_configuration(data)

    def __repr__(self):
        """Return a String representation."""
        fields = self._fields()
        return 'DysonPureCool(' + ",".join(
            printable_fields(fields)) + ')'
