from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.core import HomeAssistant
from datetime import datetime
from .const import DOMAIN
from .storage import ImpactStorage
from .state import ImpactState
from .financial import ImpactFinancialModel

class ImpactCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, config):
        super().__init__(hass, None, name="Impact")

        self.hass = hass
        self.config = config

        self.storage = ImpactStorage(hass)
        self.state = ImpactState()
        self.model = ImpactFinancialModel(config)

    async def async_setup(self):
        data = await self.storage.async_load()
        if data:
            self.state = ImpactState.from_dict(data)

    async def process_delta(self, bucket, delta_import, delta_export):
        self.state.import_energy[bucket] += delta_import
        self.state.export_energy[bucket] += delta_export

        self.model.apply_delta(bucket, delta_import, delta_export)

        await self.storage.async_save(self.state.to_dict())
        self.async_set_updated_data(self.state)
