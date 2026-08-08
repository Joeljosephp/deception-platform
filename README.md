# CIPHREX - AI Deception Intelligence Platform

CIPHREX is a deception-based Security Operations Center (SOC) platform that leverages deterministic security analysis and LLM-assisted (Google Gemini) incident reporting. The platform is designed to simulate attacker behavior, detect unauthorized access to deceptive assets (honeytokens, fake documents), and provide intelligent analysis and remediation recommendations.

## Features

- **Interactive Dashboard**: Real-time visualization of simulated threats, active decoys, and security alerts.
- **Attacker Simulation**: Generate live security events by simulating attacker behaviors (e.g., Honeytoken access, Fake Document access, Admin API scanning).
- **Risk & Threat Engine**: Deterministic calculation of risk scores based on accessed assets and actions.
- **LLM AI Analyst**: Integration with the Google Gemini API to provide human-readable threat summaries, explanations of suspicious behavior, and recommended actions. Includes a deterministic fallback engine if the AI API is unavailable.
- **Chat with CIPHREX-AI**: Ask the AI assistant questions directly from the dashboard.

## Tech Stack

- **Backend**: Django, Django REST Framework, SQLite
- **Frontend**: HTML5, CSS3, JavaScript, Chart.js, Lucide Icons
- **AI**: Google Gemini API

## Setup & Installation

1. **Clone the repository** and navigate to the project root:
   ```bash
   cd deception-platform
   ```

2. **Create a virtual environment** and activate it:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   Create a `.env` file in the root directory and add your Gemini API Key:
   ```env
   GEMINI_API_KEY=your_google_gemini_api_key
   GEMINI_MODEL=gemini-flash-latest
   ```

5. **Apply Migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the application**:
   Open a browser and navigate to `http://127.0.0.1:8000/`.

## Architecture

For more details on the system components, see [docs/architecture.md](docs/architecture.md).
