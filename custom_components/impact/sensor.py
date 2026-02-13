from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, BUCKETS

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []
    for bucket in BUCKETS:
        entities.append(ImpactEnergySensor(coordinator, bucket))

    async_add_entities(entities)


class ImpactEnergySensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, bucket):
        super().__init__(coordinator)
        self._bucket = bucket
        self._attr_name = f"Impact Import {bucket}"
        self._attr_unique_id = f"impact_import_{bucket.lower()}"

    @property
    def state(self):
        return self.coordinator.state.import_energy[self._bucket]
