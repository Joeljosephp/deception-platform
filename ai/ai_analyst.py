import os
import json
import urllib.request
import urllib.error
import logging

logger = logging.getLogger(__name__)

def _load_env():
    try:
        # Look for .env in the project root (one directory up from 'ai')
        env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        os.environ[k.strip()] = v.strip()
    except Exception:
        pass

def analyze_with_ai(report):
    """
    Attempt to use the Gemini LLM API for analysis.
    Fallback to the rule-based engine on any failure.
    """
    _load_env()
    
    api_key = os.environ.get("GEMINI_API_KEY", "").strip().strip('"').strip("'")
    # Default to gemini-flash-latest if not provided
    model = os.environ.get("GEMINI_MODEL", "gemini-flash-latest").strip()

    if not api_key:
        logger.warning("GEMINI_API_KEY missing, using fallback.")
        return analyze_with_rule_based_fallback(report)

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    
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
        "Content-Type": "application/json"
    }

    data = {
        "contents": [
            {
                "parts": [
                    {"text": f"{system_prompt}\n\nIncident Report:\n{report}"}
                ]
            }
        ],
        "generationConfig": {
            "response_mime_type": "application/json"
        }
    }

    req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers=headers, method="POST")

    try:
        logger.info("AI analysis requested from Gemini.")
        with urllib.request.urlopen(req, timeout=30) as response:
            response_data = response.read().decode("utf-8")
            response_json = json.loads(response_data)
            
            # Gemini returns text in response_json['candidates'][0]['content']['parts'][0]['text']
            content = response_json["candidates"][0]["content"]["parts"][0]["text"]
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

def chat_with_ai(prompt):
    _load_env()
    api_key = os.environ.get("GEMINI_API_KEY", "").strip().strip('"').strip("'")
    model = os.environ.get("GEMINI_MODEL", "gemini-flash-latest").strip()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            response_data = response.read().decode("utf-8")
            response_json = json.loads(response_data)
            content = response_json["candidates"][0]["content"]["parts"][0]["text"]
            return {"answer": content}
    except Exception as e:
        logger.error(f"Gemini API chat failed: {e}")
        return {"answer": "I'm sorry, my connection is down right now. I cannot answer your question."}


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