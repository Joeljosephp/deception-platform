from .honeytoken_manager import check_token
from .incident import create_incident
from .mitre import get_mitre
from .containment import contain
from .telemetry import collect_event


def process_access(username, source_ip, token_value):

    detection = check_token(token_value)

    if detection["detected"]:

        incident = create_incident(
            username,
            {
                "type": detection["type"],
                "value": token_value
            },
            source_ip
        )


        incident["mitre"] = get_mitre(
            detection["type"]
        )


        incident["response"] = contain(
            username
        )


        # ADD HERE
        telemetry = collect_event(incident)

        incident["telemetry"] = telemetry


        return incident


    return {
        "message": "No threat detected"
    }