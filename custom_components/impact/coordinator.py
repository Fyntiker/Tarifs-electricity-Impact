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


def resolve_bucket(now: datetime) -> str:
    hour = now.hour

    if 17 <= hour < 22:
        return "PIC"
    elif (7 <= hour < 11) or (22 <= hour < 24) or (0 <= hour < 1):
        return "MEDIUM"
    else:
        return "ECO"


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

        # ======================
        # CONFIG UTILISATEUR
        # ======================

        self.import_entity = entry.data["import_entity"]
        self.export_entity = entry.data["export_entity"]
        self.start_month_of_year = entry.data["start_month_of_year"]

        # ======================
        # PRIX TRANSPORT VIA GRD
        # ======================

        mapped_transport = None

if not entry.data.get("override_transport", False):
    mapped_transport = get_transport_prices(entry.data["grd"])

if mapped_transport:
    transport_prices = mapped_transport
else:
    transport_prices = {
        "PIC": entry.data["transport_pic"],
        "MEDIUM": entry.data["transport_medium"],
        "ECO": entry.data["transport_eco"],
    }


        self.config_prices = {
            "transport_prices": transport_prices,
            "energy_prices": {
                "PIC": entry.data["energy_pic"],
                "MEDIUM": entry.data["energy_medium"],
                "ECO": entry.data["energy_eco"],
            },
            "injection_prices": {
                "PIC": entry.data["injection_price"],
                "MEDIUM": entry.data["injection_price"],
                "ECO": entry.data["injection_price"],
            },
            "compensation_enabled": entry.data["compensation_enabled"],
        }

        self.financial_model = ImpactFinancialModel(
            self.config_prices,
            self.state
        )

        now = datetime.now()
        self.current_day = now.day
        self.current_month = now.month
        self.current_year = now.year

    async def async_load_state(self):
        data = await self.store.async_load()
        if data:
            self.state = ImpactState.from_dict(data)

    async def async_save_state(self):
        await self.store.async_save(self.state.to_dict())

    async def _async_update_data(self):
        now = datetime.now()

        # =========================
        # SNAPSHOTS PÉRIODES
        # =========================

        if now.day != self.current_day:
            self.state.take_snapshot("day")
            self.current_day = now.day

        if now.month != self.current_month:
            self.state.take_snapshot("month")
            self.current_month = now.month

        if (
            now.month == self.start_month_of_year
            and now.year != self.current_year
        ):
            self.state.take_snapshot("year")
            self.current_year = now.year

        bucket = resolve_bucket(now)

        # =========================
        # IMPORT
        # =========================

        import_state = self.hass.states.get(self.import_entity)

        if import_state:
            try:
                current_import = float(import_state.state)
            except:
                current_import = None

            if current_import is not None:
                if self.state.last_import_index == 0:
                    self.state.last_import_index = current_import
                else:
                    delta = current_import - self.state.last_import_index
                    if delta > 0:
                        self.state.import_energy[bucket] += delta
                        self.financial_model.apply_delta(bucket, delta, 0)
                    self.state.last_import_index = current_import

        # =========================
        # EXPORT
        # =========================

        export_state = self.hass.states.get(self.export_entity)

        if export_state:
            try:
                current_export = float(export_state.state)
            except:
                current_export = None

            if current_export is not None:
                if self.state.last_export_index == 0:
                    self.state.last_export_index = current_export
                else:
                    delta = current_export - self.state.last_export_index
                    if delta > 0:
                        self.state.export_energy[bucket] += delta
                        self.financial_model.apply_delta(bucket, 0, delta)
                    self.state.last_export_index = current_export

        await self.async_save_state()

        return self.state

