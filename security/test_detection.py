from .honeytoken_manager import (
    generate_api_key,
    check_token
)


token = generate_api_key()

print("Generated:")
print(token)


print("\nChecking token:")

result = check_token(
    token["value"]
)

print(result)