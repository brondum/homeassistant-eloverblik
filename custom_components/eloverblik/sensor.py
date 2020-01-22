"""Platform for sensor integration."""
import logging
from homeassistant.const import ENERGY_KILO_WATT_HOUR
from homeassistant.helpers.entity import Entity
from datetime import timedelta
from pyeloverblik.eloverblik import Eloverblik
from homeassistant.util import Throttle
_LOGGER = logging.getLogger(__name__)
DOMAIN = 'eloverblik'
MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=60)
async def async_setup_entry(hass, config, async_add_entities):
    """Set up the sensor platform."""
    eloverblik = hass.data[DOMAIN][config.entry_id]
    metering_point = config.data['metering_point']

    async_add_entities([EloverblikEnergy(eloverblik, metering_point)])


class EloverblikEnergy(Entity):
    """Representation of a Sensor."""

    def __init__(self, eloverblik, metering_point):
        """Initialize the sensor."""
        self._state = None
        self._eloverblik = eloverblik
        self._metering_point = metering_point

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Eloverblik energy yesterday'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return ENERGY_KILO_WATT_HOUR

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        """Use the data from Danfoss Air API."""
        _LOGGER.debug("Fetching data from Danfoss Air CCM module")

        usage = self._eloverblik.getYesterDayNiceFormat(self._metering_point)
        

        _LOGGER.debug("Done fetching data from Danfoss Air CCM module")
        total = 0
        for value in usage.values():
            total += float(value)


        self._state = total