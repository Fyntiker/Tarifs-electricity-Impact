import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_IMPORT_ENTITY, CONF_EXPORT_ENTITY

class ImpactConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title="Impact Tariff",
                data=user_input
            )

        schema = vol.Schema({
            vol.Required(CONF_IMPORT_ENTITY): str,
            vol.Optional(CONF_EXPORT_ENTITY): str,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema
        )
