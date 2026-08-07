from .honeytoken_manager import generate_api_key
from .security_engine import process_access


token = generate_api_key()


result = process_access(
    username="attacker",
    source_ip="192.168.1.100",
    token_value=token["value"]
)


print(result)