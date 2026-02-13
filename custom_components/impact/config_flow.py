from homeassistant import config_entries
import voluptuous as vol
from homeassistant.helpers import selector

from .const import DOMAIN


GRD_OPTIONS = [
    "ORES",
    "RESa",
    "AIEG",
    "AIESH",
    "Sibelga",
]


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 2

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title="Belgian Impact Tariff",
                data=user_input,
            )

        schema = vol.Schema({
            vol.Required("import_entity"): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="sensor")
            ),
            vol.Required("export_entity"): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="sensor")
            ),
            vol.Required("start_month_of_year", default=1):
                vol.All(int, vol.Range(min=1, max=12)),

            vol.Required("compensation_enabled", default=True): bool,

            vol.Required("grd", default="ORES"):
                vol.In(GRD_OPTIONS),

            # Prix transport
            vol.Required("transport_pic", default=0.12): float,
            vol.Required("transport_medium", default=0.09): float,
            vol.Required("transport_eco", default=0.07): float,

            # Prix énergie
            vol.Required("energy_pic", default=0.25): float,
            vol.Required("energy_medium", default=0.22): float,
            vol.Required("energy_eco", default=0.18): float,

            # Injection
            vol.Required("injection_price", default=0.10): float,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
        )
