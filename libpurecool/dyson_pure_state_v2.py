"""Dyson v2 pure cool devices."""

# pylint: disable=too-many-public-methods,too-many-instance-attributes

import json

from .const import SENSOR_INIT_STATES, FocusMode, FrontalDirection, \
    FanPower, FanMode, FanSpeed, FanState, QualityTarget
from .utils import printable_fields, get_field_value


class DysonPureCoolV2State:
    """Dyson device state."""

    @staticmethod
    def _get_field_value(state, field):
        """Get field value."""
        return state[field][1] if isinstance(state[field], list) else state[
            field]

    def __init__(self, payload):
        """Create a new state.

        :param payload: Message payload
        """
        json_message = json.loads(payload)
        self._state = json_message['product-state']
        self._fan_power = get_field_value(self._state, 'fpwr')
        self._front_direction = get_field_value(self._state, 'fdir')
        self._auto_mode = get_field_value(self._state, 'auto')
        self._oscillation_status = get_field_value(self._state, 'oscs')
        self._oscillation = get_field_value(self._state, 'oson')
        self._night_mode = get_field_value(self._state, 'nmod')
        self._continuous_monitoring = \
            get_field_value(self._state, 'rhtm')
        self._fan_state = get_field_value(self._state, 'fnst')
        self._night_mode_speed = get_field_value(self._state, 'nmdv')
        self._speed = get_field_value(self._state, 'fnsp')
        self._carbon_filter_state = get_field_value(self._state, 'cflr')
        self._hepa_filter_state = get_field_value(self._state, 'hflr')
        self._sleep_timer = get_field_value(self._state, 'sltm')
        self._oscillation_angle_low = \
            get_field_value(self._state, 'osal')
        self._oscillation_angle_high = \
            get_field_value(self._state, 'osau')

    @property
    def fan_power(self):
        """Fan on/off."""
        return self._fan_power

    @property
    def front_direction(self):
        """Airflow front/back direction."""
        return self._front_direction

    @property
    def focus_mode(self):
        """Focus the fan on one stream or spread. - Backwards compat with non-v2"""
        if self._front_direction == FrontalDirection.FRONTAL_ON.value:
            return FocusMode.FOCUS_ON.value
        return FocusMode.FOCUS_OFF.value

    @property
    def auto_mode(self):
        """Auto mode."""
        return self._auto_mode

    @property
    def oscillation_status(self):
        """Oscillation. Can be IDLE if auto mode is on."""
        return self._oscillation_status

    @property
    def oscillation(self):
        """Oscillation mode."""
        return self._oscillation

    @property
    def night_mode(self):
        """Night mode."""
        return self._night_mode

    @property
    def continuous_monitoring(self):
        """Monitor when inactive (standby)."""
        return self._continuous_monitoring

    @property
    def fan_mode(self):
        """Fan mode. - Backwards compat with non-v2"""
        if self._fan_power == FanPower.POWER_OFF.value:
            return FanMode.OFF.value
        elif self._fan_state == FanState.FAN_ON.value:
            return FanMode.FAN.value
        elif self._speed == FanSpeed.FAN_SPEED_AUTO.value:
            return FanMode.AUTO.value
        return FanMode.OFF.value

    @property
    def fan_state(self):
        """Fan state."""
        return self._fan_state

    @property
    def night_mode_speed(self):
        """Night mode fan speed."""
        return self._night_mode_speed

    @property
    def speed(self):
        """Fan speed."""
        return self._speed

    @property
    def carbon_filter_state(self):
        """State of crabon filter in percentage."""
        return self._carbon_filter_state

    @property
    def hepa_filter_state(self):
        """State of crabon filter in percentage."""
        return self._hepa_filter_state

    @property
    def filter_life(self):
        """Filter life. - Backwards compat with non-v2"""
        hours_in_year = 365 * 24
        hours_carbon = (float(self._carbon_filter_state) / 100.0) * hours_in_year
        hours_hepa = (float(self._hepa_filter_state) / 100.0) * hours_in_year
        return min(hours_carbon, hours_hepa)

    @property
    def quality_target(self):
        """Air quality target. - Backwards compat with non-v2"""
        return QualityTarget.QUALITY_BETTER.value

    @property
    def standby_monitoring(self):
        """Monitor when inactive (standby). - Backwards compat with non-v2"""
        return self._continuous_monitoring

    @property
    def sleep_timer(self):
        """Sleep timer."""
        return self._sleep_timer

    @property
    def oscillation_angle_low(self):
        """Lower oscillation angle."""
        return self._oscillation_angle_low

    @property
    def oscillation_angle_high(self):
        """Higher oscillation angle."""
        return self._oscillation_angle_high

    def __repr__(self):
        """Return a String representation."""
        fields = [("fan_power", self.fan_power),
                  ("front_direction", self.front_direction),
                  ("auto_mode", self.auto_mode),
                  ("oscillation_status", self.oscillation_status),
                  ("oscillation", self.oscillation),
                  ("night_mode", self.night_mode),
                  ("continuous_monitoring", self.continuous_monitoring),
                  ("fan_state", self.fan_state),
                  ("night_mode_speed", self.night_mode_speed),
                  ("speed", self.speed),
                  ("carbon_filter_state", self.carbon_filter_state),
                  ("hepa_filter_state", self.hepa_filter_state),
                  ("sleep_timer", self.sleep_timer),
                  ("oscillation_angle_low", self.oscillation_angle_low),
                  ("oscillation_angle_high", self.oscillation_angle_high)]
        return 'DysonPureCoolV2State(' + ",".join(printable_fields(fields)) \
               + ')'


class DysonEnvironmentalSensorV2State:
    """Environmental sensor state."""

    def __init__(self, payload):
        """Create a new Environmental sensor state.

        :param payload: Message payload
        """
        json_message = json.loads(payload)
        data = json_message['data']

        temperature = get_field_value(data, 'tact')
        self._temperature = 0 if temperature in SENSOR_INIT_STATES else float(
            temperature) / 10

        humidity = get_field_value(data, 'hact')
        self._humidity = 0 if humidity in SENSOR_INIT_STATES else int(humidity)

        particulate_matter_25 = get_field_value(data, 'pm25')
        self._particulate_matter_25 = 0 \
            if particulate_matter_25 in SENSOR_INIT_STATES \
            else int(particulate_matter_25)

        particulate_matter_10 = get_field_value(data, 'pm10')
        self._particulate_matter_10 = 0 \
            if particulate_matter_10 in SENSOR_INIT_STATES \
            else int(particulate_matter_10)

        volatile_organic_compounds = get_field_value(data, 'va10')
        self._volatile_organic_compounds = 0 \
            if volatile_organic_compounds in SENSOR_INIT_STATES \
            else int(volatile_organic_compounds)

        nitrogen_dioxide = get_field_value(data, 'noxl')
        self._nitrogen_dioxide = 0 if nitrogen_dioxide in SENSOR_INIT_STATES \
            else int(nitrogen_dioxide)

        p25r = get_field_value(data, 'p25r')
        self._p25r = 0 if p25r in SENSOR_INIT_STATES \
            else int(p25r)

        p10r = get_field_value(data, 'p10r')
        self._p10r = 0 if p10r in SENSOR_INIT_STATES \
            else int(p10r)

        sleep_timer = get_field_value(data, 'sltm')
        self._sleep_timer = 0 if sleep_timer in SENSOR_INIT_STATES \
            else int(sleep_timer)

    @property
    def temperature(self):
        """Temperature in Kelvin."""
        return self._temperature

    @property
    def humidity(self):
        """Humidity in percent."""
        return self._humidity

    @property
    def particulate_matter_25(self):
        """Particulate matter under 2.5microns."""
        return self._particulate_matter_25

    @property
    def particulate_matter_10(self):
        """Particulate matter under 10microns."""
        return self._particulate_matter_10

    @property
    def volatile_organic_compounds(self):
        """Volatile organic compounds level."""
        return self._volatile_organic_compounds

    @property
    def volatil_organic_compounds(self):
        """Volatile organic compounds level. - Backwards compat with non-v2"""
        return self._volatile_organic_compounds

    @property
    def dust(self):
        """Dust level. - Backwards compat with non-v2"""
        return max(self._particulate_matter_25, self._particulate_matter_10)

    @property
    def nitrogen_dioxide(self):
        """Nitrogen dioxide level."""
        return self._nitrogen_dioxide

    @property
    def p25r(self):
        """Unknown."""
        return self._p25r

    @property
    def p10r(self):
        """Unknown."""
        return self._p10r

    @property
    def sleep_timer(self):
        """Sleep timer."""
        return self._sleep_timer

    def __repr__(self):
        """Return a String representation."""
        fields = [("temperature", str(self.temperature)),
                  ("humidity", str(self.humidity)),
                  ("particulate_matter_25", str(self.particulate_matter_25)),
                  ("particulate_matter_10", str(self.particulate_matter_10)),
                  ("volatile_organic_compounds",
                   str(self.volatile_organic_compounds)),
                  ("nitrogen_dioxide", str(self.nitrogen_dioxide)),
                  ("p25r", str(self.p25r)),
                  ("p10r", str(self.p10r)),
                  ("sleep_timer", str(self.sleep_timer))]
        return 'DysonEnvironmentalSensorV2State(' + ",".join(
            printable_fields(fields)) + ')'



class DysonPureHotCoolV2State(DysonPureCoolV2State):
    """Dyson device state."""

    def __init__(self, payload):
        """Create a new Dyson Hot+Cool V2 state.

        :param product_type: Product type
        :param payload: Message payload
        """
        super().__init__(payload)

        self._tilt = DysonPureCoolV2State._get_field_value(self._state, 'tilt')

        self._heat_target = DysonPureCoolV2State._get_field_value(self._state,
                                                                  'hmax')

        self._heat_mode = DysonPureCoolV2State._get_field_value(self._state,
                                                                'hmod')

        self._heat_state = DysonPureCoolV2State._get_field_value(self._state,
                                                                 'hsta')

    @property
    def tilt(self):
        """Return tilt status."""
        return self._tilt

    @property
    def heat_target(self):
        """Heat target of the temperature."""
        return self._heat_target

    @property
    def heat_mode(self):
        """Heat mode on or off."""
        return self._heat_mode

    @property
    def heat_state(self):
        """Return heat state."""
        return self._heat_state

    def __repr__(self):
        """Return a String representation."""
        fields = [("fan_power", self.fan_power),
                  ("front_direction", self.front_direction),
                  ("auto_mode", self.auto_mode),
                  ("oscillation_status", self.oscillation_status),
                  ("oscillation", self.oscillation),
                  ("night_mode", self.night_mode),
                  ("continuous_monitoring", self.continuous_monitoring),
                  ("fan_state", self.fan_state),
                  ("night_mode_speed", self.night_mode_speed),
                  ("speed", self.speed),
                  ("carbon_filter_state", self.carbon_filter_state),
                  ("hepa_filter_state", self.hepa_filter_state),
                  ("sleep_timer", self.sleep_timer),
                  ("oscillation_angle_low", self.oscillation_angle_low),
                  ("oscillation_angle_high", self.oscillation_angle_high),
                  ("tilt", self.tilt),
                  ("heat_mode", self.heat_mode),
                  ("heat_target", self.heat_target),
                  ("heat_state", self.heat_state)]

        return 'DysonHotCoolV2State(' + ",".join(printable_fields(fields)) + ')'
