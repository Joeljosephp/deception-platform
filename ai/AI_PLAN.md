# AI Module

## Purpose

Analyze security events received from the Django backend and determine the threat level using a rule-based risk engine.

---

## Input

The AI module receives a list of SecurityEvent objects from Django.

Example:

```python
[
    {
        "timestamp": "2026-08-07T17:30:00Z",
        "user": "john",
        "source_ip": "192.168.1.50",
        "action": "access",
        "asset": "fake_api_key",
        "event_type": "honeytoken_access"
    }
]
```

---

## Processing

The AI module performs:

- Read security events
- Calculate risk score
- Classify threat level
- Generate incident report
- Prepare report for future AI (Gemini)

---

## Output

Returns a Python dictionary.

Example:

```python
{
    "risk_score": 100,
    "threat_level": "CRITICAL",
    "evidence": [
        "Honeytoken Access",
        "Fake Document Opened",
        "Admin API Scan"
    ],
    "report": "Generated Incident Report"
}
```

---

## Current Status

✅ Rule-based risk engine implemented

✅ Threat classification implemented

✅ Incident report generation implemented

✅ Django integration ready

❌ Gemini AI not yet integrated