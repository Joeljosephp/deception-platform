from .telemetry import collect_event, get_events


incident = {

    "severity":"Critical",

    "event":"Honeytoken Access",

    "source_ip":"192.168.1.100",

    "username":"attacker",

    "asset":"API_KEY"

}


event = collect_event(incident)


print(event)

print("\nAll Events:")
print(get_events())