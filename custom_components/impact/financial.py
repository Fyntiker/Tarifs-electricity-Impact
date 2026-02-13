class ImpactFinancialModel:
    def __init__(self, config, state):
        self.config = config
        self.state = state

    def apply_delta(self, bucket, delta_import, delta_export):

        # Transport (toujours brut import)
        transport_price = self.config["transport_prices"][bucket]
        self.state.transport_cost += delta_import * transport_price

        # Energie
        energy_price = self.config["energy_prices"][bucket]
        injection_price = self.config["injection_prices"][bucket]

        if not self.config["compensation_enabled"]:
            # Pas de compensation
            self.state.energy_cost += delta_import * energy_price
            self.state.injection_revenue += delta_export * injection_price
        else:
            # Compensation uniquement sur énergie
            net = (
                self.state.import_energy[bucket]
                - self.state.export_energy[bucket]
            )

            if net > 0:
                self.state.energy_cost += delta_import * energy_price
            # Sinon rien à ajouter (énergie compensée)

            # Injection éventuelle rémunérée si surplus
            if net < 0:
                surplus = abs(net)
                self.state.injection_revenue += surplus * injection_price

    def get_balance(self):
        return (
            self.state.transport_cost
            + self.state.energy_cost
            - self.state.injection_revenue
        )
