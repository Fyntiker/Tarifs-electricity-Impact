from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    buckets = ["PIC", "MEDIUM", "ECO"]

    entities = []

    for bucket in buckets:
        entities.append(ImpactImportSensor(coordinator, bucket))
        entities.append(ImpactExportSensor(coordinator, bucket))

    entities.append(ImpactTransportCostSensor(coordinator))
    entities.append(ImpactEnergyCostSensor(coordinator))
    entities.append(ImpactTotalBalanceSensor(coordinator))
    entities.append(ImpactDailyBalanceSensor(coordinator))
    entities.append(ImpactMonthlyBalanceSensor(coordinator))
    entities.append(ImpactYearlyBalanceSensor(coordinator))

    async_add_entities(entities)


# =========================
# ENERGY
# =========================

class ImpactImportSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, bucket):
        super().__init__(coordinator)
        self._bucket = bucket
        self._attr_name = f"Impact Import {bucket}"
        self._attr_unique_id = f"impact_import_{bucket.lower()}"
        self._attr_unit_of_measurement = "kWh"

    @property
    def state(self):
        return round(self.coordinator.data.import_energy[self._bucket], 4)


class ImpactExportSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, bucket):
        super().__init__(coordinator)
        self._bucket = bucket
        self._attr_name = f"Impact Export {bucket}"
        self._attr_unique_id = f"impact_export_{bucket.lower()}"
        self._attr_unit_of_measurement = "kWh"

    @property
    def state(self):
        return round(self.coordinator.data.export_energy[self._bucket], 4)


# =========================
# COSTS TOTAL
# =========================

class ImpactTransportCostSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Impact Transport Cost"
        self._attr_unique_id = "impact_transport_cost"
        self._attr_unit_of_measurement = "€"

    @property
    def state(self):
        return round(self.coordinator.data.transport_cost, 4)


class ImpactEnergyCostSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Impact Energy Cost"
        self._attr_unique_id = "impact_energy_cost"
        self._attr_unit_of_measurement = "€"

    @property
    def state(self):
        return round(self.coordinator.data.energy_cost, 4)


class ImpactTotalBalanceSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Impact Total Balance"
        self._attr_unique_id = "impact_total_balance"
        self._attr_unit_of_measurement = "€"

    @property
    def state(self):
        return round(
            self.coordinator.data.transport_cost
            + self.coordinator.data.energy_cost
            - self.coordinator.data.injection_revenue,
            4
        )


# =========================
# PERIOD BALANCES
# =========================

class ImpactDailyBalanceSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Impact Daily Balance"
        self._attr_unique_id = "impact_daily_balance"
        self._attr_unit_of_measurement = "€"

    @property
    def state(self):
        delta = self.coordinator.data.get_period_delta("day")
        if not delta:
            return 0
        return round(
            delta["transport_cost"]
            + delta["energy_cost"]
            - delta["injection_revenue"],
            4
        )


class ImpactMonthlyBalanceSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Impact Monthly Balance"
        self._attr_unique_id = "impact_monthly_balance"
        self._attr_unit_of_measurement = "€"

    @property
    def state(self):
        delta = self.coordinator.data.get_period_delta("month")
        if not delta:
            return 0
        return round(
            delta["transport_cost"]
            + delta["energy_cost"]
            - delta["injection_revenue"],
            4
        )


class ImpactYearlyBalanceSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Impact Yearly Balance"
        self._attr_unique_id = "impact_yearly_balance"
        self._attr_unit_of_measurement = "€"

    @property
    def state(self):
        delta = self.coordinator.data.get_period_delta("year")
        if not delta:
            return 0
        return round(
            delta["transport_cost"]
            + delta["energy_cost"]
            - delta["injection_revenue"],
            4
        )
