import random
import string
from datetime import datetime


honeytokens = []


def generate_api_key():

    key = "AKIA" + ''.join(
        random.choices(
            string.ascii_uppercase + string.digits,
            k=16
        )
    )

    token = {
        "type": "API_KEY",
        "value": key,
        "created": datetime.now().isoformat(),
        "status": "ACTIVE"
    }

    honeytokens.append(token)

    return token



def check_token(value):

    for token in honeytokens:

        if token["value"] == value:

            return {
                "detected": True,
                "type": token["type"],
                "severity": "Critical"
            }

    return {
        "detected": False
    }



def list_tokens():

    return honeytokens