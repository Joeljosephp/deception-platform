MITRE = {

    "API_KEY": {
        "id": "T1552",
        "technique": "Unsecured Credentials"
    },

    "DATABASE": {
        "id": "T1005",
        "technique": "Data from Local System"
    },

    "DOCUMENT": {
        "id": "T1083",
        "technique": "File and Directory Discovery"
    },

    "SOURCE_CODE": {
        "id": "T1552",
        "technique": "Credentials in Files"
    }
}


def get_mitre(asset_type):
    return MITRE.get(asset_type, {})