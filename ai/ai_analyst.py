def analyze_with_ai(report):
    """
    Generate a security analyst assessment based on
    the actual evidence contained in the incident report.
    """

    report_lower = report.lower()

    threat_summary = "Suspicious security activity detected."

    why_suspicious = []

    recommended_response = []

    # --------------------------------------------------
    # HONEYTOKEN ACCESS
    # --------------------------------------------------

    honeytoken_detected = "honeytoken access" in report_lower

    if honeytoken_detected:

        why_suspicious.append(
            "A honeytoken credential was accessed."
        )

        recommended_response.extend([
            "Investigate the user",
            "Monitor the source IP"
        ])

    # --------------------------------------------------
    # FAKE DOCUMENT
    # --------------------------------------------------

    document_detected = "fake document opened" in report_lower

    if document_detected:

        why_suspicious.append(
            "A deceptive confidential document was opened."
        )

        recommended_response.append(
            "Review access to the affected document"
        )

    # --------------------------------------------------
    # ADMIN API SCAN
    # --------------------------------------------------

    scan_detected = "admin api scan" in report_lower

    if scan_detected:

        why_suspicious.append(
            "Administrative API scanning was detected."
        )

        recommended_response.extend([
            "Investigate the source IP",
            "Review API access logs"
        ])

    # --------------------------------------------------
    # HONEYTOKEN + API SCAN
    # --------------------------------------------------

    if honeytoken_detected and scan_detected:

        threat_summary = (
            "The activity indicates suspicious reconnaissance "
            "combined with attempted access to a deceptive credential."
        )

        why_suspicious.append(
            "The combination of credential access and API scanning "
            "suggests possible reconnaissance and credential abuse."
        )

    # --------------------------------------------------
    # HONEYTOKEN ONLY
    # --------------------------------------------------

    elif honeytoken_detected:

        threat_summary = (
            "A deceptive credential was accessed, indicating "
            "potential unauthorized credential discovery or use."
        )

    # --------------------------------------------------
    # FAKE DOCUMENT ONLY
    # --------------------------------------------------

    elif document_detected:

        threat_summary = (
            "A deceptive confidential document was opened, "
            "indicating possible unauthorized information discovery."
        )

    # --------------------------------------------------
    # API SCAN ONLY
    # --------------------------------------------------

    elif scan_detected:

        threat_summary = (
            "Administrative API scanning was detected, "
            "indicating possible reconnaissance activity."
        )

    # --------------------------------------------------
    # FALLBACK
    # --------------------------------------------------

    else:

        threat_summary = (
            "The observed event requires further investigation."
        )

        why_suspicious.append(
            "The event contains activity that should be reviewed."
        )

    # --------------------------------------------------
    # THREAT LEVEL RESPONSE
    # --------------------------------------------------

    if "threat level : critical" in report_lower:

        recommended_response.extend([
            "Isolate the affected session",
            "Alert the security administrator"
        ])

    elif "threat level : high" in report_lower:

        recommended_response.append(
            "Increase monitoring of the affected user"
        )

    elif "threat level : medium" in report_lower:

        recommended_response.append(
            "Increase monitoring of the affected asset"
        )

    else:

        recommended_response.append(
            "Continue monitoring"
        )

    # Remove duplicate actions
    recommended_response = list(dict.fromkeys(recommended_response))

    # --------------------------------------------------
    # ANALYST ASSESSMENT
    # --------------------------------------------------

    if honeytoken_detected and scan_detected:

        assessment = (
            "The combination of deceptive credential access and "
            "administrative scanning represents a stronger indication "
            "of malicious reconnaissance."
        )

    elif honeytoken_detected:

        assessment = (
            "Access to a honeytoken is a strong indicator of "
            "unauthorized activity and should be investigated."
        )

    elif document_detected:

        assessment = (
            "Access to a deceptive confidential document may indicate "
            "unauthorized information discovery."
        )

    elif scan_detected:

        assessment = (
            "Administrative API scanning may indicate reconnaissance "
            "against the application's infrastructure."
        )

    else:

        assessment = (
            "The observed activity should be reviewed for additional "
            "indicators of compromise."
        )

    return {
        "threat_summary": threat_summary,
        "why_suspicious": why_suspicious,
        "recommended_response": recommended_response,
        "analyst_assessment": assessment
    }