from datetime import datetime


def create_incident(
        username,
        token,
        source_ip
):

    incident = {

        "incident_id":
            "INC-" + datetime.now().strftime("%Y%m%d%H%M%S"),

        "username": username,

        "source_ip": source_ip,

        "asset": token["type"],

        "token_value": token["value"],

        "event":
            "Honeytoken Access",

        "severity":
            "Critical",

        "timestamp":
            datetime.now().isoformat(),

        "status":
            "Open"
    }

    return incident 