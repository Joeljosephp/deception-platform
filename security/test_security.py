from .detector import detect
from .mitre import get_mitre
from .containment import contain

asset = "fake_api_key"

print(detect(asset))
print(get_mitre(asset))
print(contain("attacker"))