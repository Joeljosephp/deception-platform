def analyze_behavior(events):

    accessed_assets = [
        event["asset"]
        for event in events
    ]


    if len(accessed_assets) >= 3:

        return {
            "profile": "Possible Lateral Movement",
            "confidence": 90
        }


    if "API_KEY" in accessed_assets:

        return {
            "profile": "Credential Harvester",
            "confidence": 75
        }


    return {
        "profile": "Unknown Activity",
        "confidence": 40
    }