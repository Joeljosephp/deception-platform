from datetime import datetime


events = []


def collect_event(incident):

    telemetry = {

        "event_id":
        len(events) + 1,

        "timestamp":
        datetime.now().isoformat(),

        "severity":
        incident["severity"],

        "event":
        incident["event"],

        "source_ip":
        incident["source_ip"],

        "username":
        incident["username"],

        "asset":
        incident["asset"]

    }

    events.append(telemetry)

    return telemetry



def get_events():

    return events