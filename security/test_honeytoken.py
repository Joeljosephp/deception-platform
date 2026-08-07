from .honeytoken_manager import generate_api_key, list_tokens


token = generate_api_key()

print(token)

print(list_tokens())