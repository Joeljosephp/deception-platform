from .honeytoken_manager import generate_api_key
from .security_engine import process_access
from .behavior import analyze_behavior


# Generate fake asset
token = generate_api_key()

print("\nGenerated Honeytoken:")
print(token)


# Simulate attacker accessing it
incident = process_access(
    username="attacker",
    source_ip="192.168.1.100",
    token_value=token["value"]
)


print("\nIncident Created:")
print(incident)


# Simulate multiple attacks
events = [
    {"asset": "API_KEY"},
    {"asset": "DATABASE"},
    {"asset": "SOURCE_CODE"}
]


profile = analyze_behavior(events)


print("\nAttacker Profile:")
print(profile)