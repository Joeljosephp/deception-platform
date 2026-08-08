# CIPHREX Architecture

CIPHREX uses a deterministic security analysis engine to calculate risk scores, classify threats, map observed activity to MITRE ATT&CK techniques, and generate incident reports. These reports are passed to an LLM-based analyst layer for contextual interpretation, explanation of suspicious behavior, and recommended investigative actions. The LLM does not determine the authoritative risk score; it acts as an analyst-assistance layer.

## System Components

- **Frontend**: Displays dashboard, threats, and attackers information to the user. Expects structured JSON containing AI analysis.
- **Django**: The core backend framework handling requests, views, and integrations.
- **Django REST Framework**: Provides the REST API endpoints (`/api/events/`, `/api/analysis/`, etc.) that power the frontend.
- **SQLite**: The lightweight database used for storing security events and attacker models.
- **Risk Engine**: Deterministic rule-based engine that calculates Risk Score and Threat Level based on events (e.g., honeytoken access, admin API scans).
- **MITRE ATT&CK Mapping**: Deterministic assignment of techniques like T1552 or T1595 to observed behaviors.
- **LLM Analyst**: Powered by Google Gemini, this layer provides human-readable explanations (`threat_summary`, `why_suspicious`, `recommended_response`, `analyst_assessment`) based on the incident report. It falls back to a rule-based AI analyst simulation if the API is unavailable.
- **Gemini API**: Cloud provider used for LLM inference. Accessed server-side via Python (Django backend). API Keys and configurations are managed purely through environment variables (`GEMINI_API_KEY`, `GEMINI_MODEL`).
