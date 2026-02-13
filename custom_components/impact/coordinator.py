import logging
from datetime import datetime, timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.storage import Store
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .impact_state import ImpactState
from .financial import ImpactFinancialModel
from .grd_mapping import get_transport_prices

_LOGGER = logging.getLogger(__name__)

STORAGE_VERSION = 1
STORAGE_KEY = "impact_state"


class ImpactCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        super().__init__(
            hass,
            _LOGGER,
            name="Impact Coordinator",
            update_interval=timedelta(seconds=30),
        )

        self.hass = hass
        self.entry = entry
        self.store = Store(hass, STORAGE_VERSION, STORAGE_KEY)

        self.state = ImpactState()

        self.import_entity = entry.data.get("import_entity")
        self.export_entity = entry.data.get("export_entity")

        self.start_month_of_year = entry.data.get("start_month_of_year", 1)

        mapped_transport = None
        if not entry.data.get("override_transport", False):
            mapped_transport = get_transport_prices(entry.data.get("grd"))

        if mapped_transport:
            transport_prices = mapped_transport
        else:
            transport_prices = {
                "PIC": entry.data.get("transport_pic", 0.0),
                "MEDIUM": entry.data.get("transport_medium", 0.0),
                "ECO": entry.data.get("transport_eco", 0.0),
            }

        self.config_prices = {
            "transport_prices": transport_prices,
            "energy_prices": {
                "PIC": entry.data.get("energy_pic", 0.0),
                "MEDIUM": entry.data.get("energy_medium", 0.0),
                "ECO": entry.data.get("energy_eco", 0.0),
            },
            "injection_prices": {
                "PIC": entry.data.get("injection_price", 0.0),
                "MEDIUM": entry.data.get("injection_price", 0.0),
                "ECO": entry.data.get("injection_price", 0.0),
            },
            "compensation_enabled": entry.data.get("compensation_enabled", False),
        }

        self.financial_model = ImpactFinancialModel(
            self.config_prices,
            self.state
        )

    async def async_load_state(self):
        data = await self.store.async_load()
        if data:
            self.state = ImpactState.from_dict(data)

    async def async_save_state(self):
        await self.store.async_save(self.state.to_dict())

    async def _async_update_data(self):
        return self.state
