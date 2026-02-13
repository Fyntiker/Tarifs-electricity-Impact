class ImpactFinancialModel:
    def __init__(self, config, state):
        self.config = config
        self.state = state

    def apply_delta(self, bucket, delta_import, delta_export):

        transport_price = self.config["transport_prices"][bucket]
        energy_price = self.config["energy_prices"][bucket]
        injection_price = self.config["injection_prices"][bucket]

        # =========================
        # TRANSPORT (toujours brut import)
        # =========================
        if delta_import > 0:
            self.state.transport_cost += delta_import * transport_price

        # =========================
        # ENERGIE
        # =========================

        if not self.config["compensation_enabled"]:
            # Pas de compensation
            if delta_import > 0:
                self.state.energy_cost += delta_import * energy_price

            if delta_export > 0:
                self.state.injection_revenue += delta_export * injection_price

        else:
            # Compensation par bucket
            net = (
                self.state.import_energy[bucket]
                - self.state.export_energy[bucket]
            )

            if net > 0:
                # On facture uniquement le net positif
                self.state.energy_cost = sum(
                    max(
                        self.state.import_energy[b]
                        - self.state.export_energy[b],
                        0
                    ) * self.config["energy_prices"][b]
                    for b in ["PIC", "MEDIUM", "ECO"]
                )
            else:
                # Si surplus net négatif
                surplus = abs(net)
                self.state.injection_revenue += surplus * injection_price

    def get_balance(self):
        return (
            self.state.transport_cost
            + self.state.energy_cost
            - self.state.injection_revenue
        )
