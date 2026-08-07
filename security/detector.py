# detector.py
from .rules import RULES

def detect(asset_name):
    if asset_name in RULES:
        return {
            "detected": True,
            "severity": RULES[asset_name]["severity"],
            "risk_score": RULES[asset_name]["risk_score"]
        }

    return {
        "detected": False,
        "severity": "None",
        "risk_score": 0
    }