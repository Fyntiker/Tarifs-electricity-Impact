from datetime import date

GRD_TARIFFS = {
    "ORES": [
        {
            "from": date(2025, 1, 1),
            "transport": {
                "PIC": 0.13,
                "MEDIUM": 0.10,
                "ECO": 0.08,
            }
        },
        {
            "from": date(2026, 1, 1),
            "transport": {
                "PIC": 0.14,
                "MEDIUM": 0.11,
                "ECO": 0.09,
            }
        }
    ],

    "Sibelga": [
        {
            "from": date(2025, 1, 1),
            "transport": {
                "PIC": 0.15,
                "MEDIUM": 0.12,
                "ECO": 0.09,
            }
        }
    ]
}


def get_transport_prices(grd_name):
    today = date.today()
    tariffs = GRD_TARIFFS.get(grd_name, [])

    applicable = None

    for t in tariffs:
        if today >= t["from"]:
            applicable = t

    if applicable:
        return applicable["transport"]

    return None
