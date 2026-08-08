import os
import json
import urllib.request
import urllib.error
import logging

logger = logging.getLogger(__name__)

def analyze_with_ai(report):
    """
    Attempt to use the Groq LLM API for analysis.
    Fallback to the rule-based engine on any failure.
    """
    api_key = os.environ.get("GROQ_API_KEY")
    model = os.environ.get("GROQ_MODEL")

    if not api_key or not model:
        logger.warning("GROQ_API_KEY or GROQ_MODEL missing, using fallback.")
        return analyze_with_rule_based_fallback(report)

    url = "https://api.groq.com/openai/v1/chat/completions"
    
    system_prompt = """You are a cybersecurity incident analyst.

Analyze only the security evidence provided to you.
Do not invent events, users, IP addresses, vulnerabilities, MITRE techniques, or evidence.

The risk score and threat level have already been calculated by a deterministic security engine.
Do not change the supplied risk score or threat level.

Your task is to explain:
1. What the activity indicates.
2. Why the evidence is suspicious.
3. What a security analyst should investigate next.
4. The overall analyst assessment.

Return ONLY valid JSON using this schema:
{
  "threat_summary": "string",
  "why_suspicious": ["string"],
  "recommended_response": ["string"],
  "analyst_assessment": "string"
}"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": report}
        ],
        "response_format": {"type": "json_object"}
    }

    req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers=headers, method="POST")

    try:
        logger.info("AI analysis requested.")
        with urllib.request.urlopen(req, timeout=10) as response:
            response_data = response.read().decode("utf-8")
            response_json = json.loads(response_data)
            
            content = response_json["choices"][0]["message"]["content"]
            result = json.loads(content)
            
            # Simple schema validation
            required_keys = {"threat_summary", "why_suspicious", "recommended_response", "analyst_assessment"}
            if isinstance(result, dict) and required_keys.issubset(result.keys()):
                logger.info("AI provider response received.")
                return result
            else:
                logger.warning("AI output validation failed, AI fallback triggered.")
                return analyze_with_rule_based_fallback(report)
    except Exception as e:
        logger.warning(f"AI API call failed: {e}. AI fallback triggered.")
        return analyze_with_rule_based_fallback(report)


def analyze_with_rule_based_fallback(report):
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