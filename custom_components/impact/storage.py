from homeassistant.helpers.storage import Store

STORAGE_VERSION = 1
STORAGE_KEY = "impact_state"

class ImpactStorage:
    def __init__(self, hass):
        self.store = Store(hass, STORAGE_VERSION, STORAGE_KEY)

    async def async_load(self):
        return await self.store.async_load()

    async def async_save(self, data):
        await self.store.async_save(data)
