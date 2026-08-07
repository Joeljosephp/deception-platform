from .incident_report import generate_report
from .ai_analyst import analyze_with_ai


def analyze_security_events(events):
    """
    Analyze security events received from Django.

    Parameters:
        events (list): List of SecurityEvent dictionaries

    Returns:
        dict: Structured AI analysis result
    """

    risk = 0
    findings = []

    print("=" * 60)
    print("RISK ANALYSIS")
    print("=" * 60)

    for event in events:

        asset = event.get("asset", "")
        action = event.get("action", "")

        # Honeytoken Access
        if asset == "fake_api_key":
            print("Honeytoken Access Detected (+40)")
            risk += 40
            findings.append("Honeytoken Access")

        # Fake Document Opened
        if asset == "salary.xlsx":
            print("Fake Confidential Document Opened (+30)")
            risk += 30
            findings.append("Fake Document Opened")

        # Admin API Scan
        if action == "scan":
            print("Admin API Scan Detected (+30)")
            risk += 30
            findings.append("Admin API Scan")

    # --------------------------
    # Threat Classification
    # --------------------------

    if risk >= 80:
        threat = "CRITICAL"

    elif risk >= 50:
        threat = "HIGH"

    elif risk >= 20:
        threat = "MEDIUM"

    else:
        threat = "LOW"

    # --------------------------
    # Generate Incident Report
    # --------------------------

    report = generate_report(
        risk,
        threat,
        findings
    )

    print(report)

    # --------------------------
    # Gemini AI Analysis
    # --------------------------

    try:
        ai_response = analyze_with_ai(report)

    except Exception as e:
        ai_response = f"Gemini Error: {e}"

    # --------------------------
    # MITRE Mapping
    # --------------------------

    mitre = []

    if "Honeytoken Access" in findings:
        mitre.append({
            "id": "T1552",
            "technique": "Unsecured Credentials"
        })

    if "Fake Document Opened" in findings:
        mitre.append({
            "id": "T1213",
            "technique": "Data from Information Repositories"
        })

    if "Admin API Scan" in findings:
        mitre.append({
            "id": "T1595",
            "technique": "Active Scanning"
        })

    # --------------------------
    # Recommended Actions
    # --------------------------

    if threat == "CRITICAL":

        actions = [
            "Isolate Session",
            "Alert Administrator",
            "Investigate User"
        ]

    elif threat == "HIGH":

        actions = [
            "Monitor User Activity"
        ]

    elif threat == "MEDIUM":

        actions = [
            "Increase Monitoring"
        ]

    else:

        actions = [
            "Continue Monitoring"
        ]

    # --------------------------
    # Return Result to Django
    # --------------------------

    result = {
        "risk_score": risk,
        "threat_level": threat,
        "evidence": findings,
        "mitre": mitre,
        "recommended_actions": actions,
        "report": report,
        "ai_summary": ai_response
    }

    return result


# ==========================================================
# TESTING WITHOUT DJANGO
# ==========================================================

if __name__ == "__main__":

    sample_events = [

        {
            "timestamp": "2026-08-07T17:30:00Z",
            "user": "john",
            "source_ip": "192.168.1.50",
            "action": "access",
            "asset": "fake_api_key",
            "event_type": "honeytoken_access"
        },

        {
            "timestamp": "2026-08-07T17:31:00Z",
            "user": "john",
            "source_ip": "192.168.1.50",
            "action": "open",
            "asset": "salary.xlsx",
            "event_type": "fake_document"
        },

        {
            "timestamp": "2026-08-07T17:32:00Z",
            "user": "john",
            "source_ip": "192.168.1.50",
            "action": "scan",
            "asset": "admin_api",
            "event_type": "network_scan"
        }

    ]

    result = analyze_security_events(sample_events)

    print("\n")
    print("=" * 60)
    print("RETURNED TO DJANGO")
    print("=" * 60)

    print(result)