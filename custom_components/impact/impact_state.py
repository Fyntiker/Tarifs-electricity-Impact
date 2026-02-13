from dataclasses import dataclass, field
from typing import Dict

BUCKETS = ["PIC", "MEDIUM", "ECO"]


@dataclass
class ImpactState:
    import_energy: Dict[str, float] = field(
        default_factory=lambda: {b: 0.0 for b in BUCKETS}
    )
    export_energy: Dict[str, float] = field(
        default_factory=lambda: {b: 0.0 for b in BUCKETS}
    )

    transport_cost: float = 0.0
    energy_cost: float = 0.0
    injection_revenue: float = 0.0

    last_import_index: float = 0.0
    last_export_index: float = 0.0

    period_snapshots: dict = field(default_factory=dict)

    # =========================
    # STORAGE
    # =========================

    def to_dict(self):
        return {
            "import_energy": self.import_energy,
            "export_energy": self.export_energy,
            "transport_cost": self.transport_cost,
            "energy_cost": self.energy_cost,
            "injection_revenue": self.injection_revenue,
            "last_import_index": self.last_import_index,
            "last_export_index": self.last_export_index,
            "period_snapshots": self.period_snapshots,
        }

    @classmethod
    def from_dict(cls, data: dict):
        state = cls()

        state.import_energy = data.get("import_energy", state.import_energy)
        state.export_energy = data.get("export_energy", state.export_energy)
        state.transport_cost = data.get("transport_cost", 0.0)
        state.energy_cost = data.get("energy_cost", 0.0)
        state.injection_revenue = data.get("injection_revenue", 0.0)
        state.last_import_index = data.get("last_import_index", 0.0)
        state.last_export_index = data.get("last_export_index", 0.0)
        state.period_snapshots = data.get("period_snapshots", {})

        return state

    # =========================
    # SNAPSHOTS
    # =========================

    def take_snapshot(self, period_name):
        self.period_snapshots[period_name] = {
            "transport_cost": self.transport_cost,
            "energy_cost": self.energy_cost,
            "injection_revenue": self.injection_revenue,
        }

    def get_period_delta(self, period_name):
        snapshot = self.period_snapshots.get(period_name)

        if not snapshot:
            return None

        return {
            "transport_cost": self.transport_cost - snapshot["transport_cost"],
            "energy_cost": self.energy_cost - snapshot["energy_cost"],
            "injection_revenue": self.injection_revenue - snapshot["injection_revenue"],
        }
