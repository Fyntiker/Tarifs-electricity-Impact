from homeassistant import config_entries
import voluptuous as vol

from homeassistant.helpers.selector import (
    EntitySelector,
    EntitySelectorConfig,
    SelectSelector,
    SelectSelectorConfig,
)

from .const import DOMAIN


GRD_OPTIONS = [
    "AIEG",
    "AIESH",
    "ORES",
    "RESA",
    "REW",
]

MONTHS = {
    1: "Janvier",
    2: "Février",
    3: "Mars",
    4: "Avril",
    5: "Mai",
    6: "Juin",
    7: "Juillet",
    8: "Août",
    9: "Septembre",
    10: "Octobre",
    11: "Novembre",
    12: "Décembre",
}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 6

    async def async_step_user(self, user_input=None):

        if user_input is not None:
            return self.async_create_entry(
                title="Tarif Impact Belgique",
                data=user_input,
            )

        schema = vol.Schema({
            vol.Required("import_entity"): EntitySelector(
                EntitySelectorConfig(domain="sensor")
            ),
            vol.Required("export_entity"): EntitySelector(
                EntitySelectorConfig(domain="sensor")
            ),

            vol.Required(
                "start_month_of_year",
                default=1
            ): SelectSelector(
                SelectSelectorConfig(
                    options=[
                        {"value": k, "label": v}
                        for k, v in MONTHS.items()
                    ]
                )
            ),

            vol.Required("compensation_enabled", default=True): bool,
            vol.Required("grd", default="ORES"): vol.In(GRD_OPTIONS),
            vol.Required("override_transport", default=False): bool,

            vol.Required("transport_pic", default=0.0): float,
            vol.Required("transport_medium", default=0.0): float,
            vol.Required("transport_eco", default=0.0): float,

            vol.Required("energy_pic", default=0.25): float,
            vol.Required("energy_medium", default=0.22): float,
            vol.Required("energy_eco", default=0.18): float,

            vol.Required("injection_price", default=0.10): float,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
        )
