from .honeytoken_manager import generate_api_key
from .incident import create_incident


token = generate_api_key()


incident = create_incident(
    username="attacker",
    source_ip="192.168.1.50",
    token=token
)


print(incident)