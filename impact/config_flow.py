from homeassistant import config_entries
import voluptuous as vol
from homeassistant.helpers import selector
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


# =========================
# CONFIG FLOW INITIAL
# =========================

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 5

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title="Tarif Impact Belgique",
                data=user_input,
            )

        return self._show_form()

    def _show_form(self):
        schema = vol.Schema({
            vol.Required("import_entity"): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="sensor")
            ),
            vol.Required("export_entity"): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="sensor")
            ),

            vol.Required(
                "start_month_of_year",
                default=1
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
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

    @staticmethod
    def async_get_options_flow(config_entry):
        return ImpactOptionsFlow(config_entry)


# =========================
# OPTIONS FLOW (MODIFICATION)
# =========================

class ImpactOptionsFlow(config_entries.OptionsFlow):

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:

            # Fusion ancienne data + nouvelles options
            new_data = {**self.config_entry.data, **user_input}

            self.hass.config_entries.async_update_entry(
                self.config_entry,
                data=new_data,
            )

            await self.hass.config_entries.async_reload(
                self.config_entry.entry_id
            )

            return self.async_create_entry(title="", data={})

        current = self.config_entry.data

        schema = vol.Schema({
            vol.Required(
                "start_month_of_year",
                default=current.get("start_month_of_year", 1)
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=[
                        {"value": k, "label": v}
                        for k, v in MONTHS.items()
                    ]
                )
            ),

            vol.Required(
                "compensation_enabled",
                default=current.get("compensation_enabled", True)
            ): bool,

            vol.Required(
                "grd",
                default=current.get("grd", "ORES")
            ): vol.In(GRD_OPTIONS),

            vol.Required(
                "override_transport",
                default=current.get("override_transport", False)
            ): bool,

            vol.Required(
                "transport_pic",
                default=current.get("transport_pic", 0.0)
            ): float,

            vol.Required(
                "transport_medium",
                default=current.get("transport_medium", 0.0)
            ): float,

            vol.Required(
                "transport_eco",
                default=current.get("transport_eco", 0.0)
            ): float,

            vol.Required(
                "energy_pic",
                default=current.get("energy_pic", 0.25)
            ): float,

            vol.Required(
                "energy_medium",
                default=current.get("energy_medium", 0.22)
            ): float,

            vol.Required(
                "energy_eco",
                default=current.get("energy_eco", 0.18)
            ): float,

            vol.Required(
                "injection_price",
                default=current.get("injection_price", 0.10)
            ): float,
        })

        return self.async_show_form(
            step_id="init",
            data_schema=schema,
        )
