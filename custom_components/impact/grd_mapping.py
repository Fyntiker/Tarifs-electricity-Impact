from datetime import date

GRD_TARIFFS = {
    "AIEG": [
        {
            "from": date(2026, 1, 1),
            "transport": {
                "ECO": 0.0456,
                "MEDIUM": 0.0982,
                "PIC": 0.1508,
            }
        }
    ],
    "AIESH": [
        {
            "from": date(2026, 1, 1),
            "transport": {
                "ECO": 0.0550,
                "MEDIUM": 0.1228,
                "PIC": 0.1907,
            }
        }
    ],
    "ORES": [
        {
            "from": date(2026, 1, 1),
            "transport": {
                "ECO": 0.0509,
                "MEDIUM": 0.1083,
                "PIC": 0.1657,
            }
        }
    ],
    "RESA": [
        {
            "from": date(2026, 1, 1),
            "transport": {
                "ECO": 0.0499,
                "MEDIUM": 0.1005,
                "PIC": 0.1511,
            }
        }
    ],
    "REW": [
        {
            "from": date(2026, 1, 1),
            "transport": {
                "ECO": 0.0552,
                "MEDIUM": 0.1132,
                "PIC": 0.1711,
            }
        }
    ],
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
