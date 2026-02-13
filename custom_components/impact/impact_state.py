from dataclasses import dataclass, field
from typing import Dict, Optional
from datetime import datetime


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

    last_reset: Optional[datetime] = None

    def reset(self):
        self.import_energy = {b: 0.0 for b in BUCKETS}
        self.export_energy = {b: 0.0 for b in BUCKETS}
        self.transport_cost = 0.0
        self.energy_cost = 0.0
        self.injection_revenue = 0.0
        self.last_reset = datetime.utcnow()

    def to_dict(self):
        return {
            "import_energy": self.import_energy,
            "export_energy": self.export_energy,
            "transport_cost": self.transport_cost,
            "energy_cost": self.energy_cost,
            "injection_revenue": self.injection_revenue,
            "last_import_index": self.last_import_index,
            "last_export_index": self.last_export_index,
            "last_reset": self.last_reset.isoformat()
            if self.last_reset else None,
        }

    @classmethod
    def from_dict(cls, data):
        state = cls()
        state.import_energy = data.get("import_energy", state.import_energy)
        state.export_energy = data.get("export_energy", state.export_energy)
        state.transport_cost = data.get("transport_cost", 0.0)
        state.energy_cost = data.get("energy_cost", 0.0)
        state.injection_revenue = data.get("injection_revenue", 0.0)
        state.last_import_index = data.get("last_import_index", 0.0)
        state.last_export_index = data.get("last_export_index", 0.0)

        if data.get("last_reset"):
            state.last_reset = datetime.fromisoformat(data["last_reset"])

        return state
