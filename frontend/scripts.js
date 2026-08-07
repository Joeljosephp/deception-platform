const API_URL = "http://127.0.0.1:8000/api/events/?format=json";
const AI_URL = "http://127.0.0.1:8000/api/analysis/";

// =========================
// Load Recent Events
// =========================
async function loadEvents() {
    try {

        const response = await fetch(API_URL);
        const events = await response.json();

        const container = document.getElementById("recent-events");

        container.innerHTML = "";

        if (events.length === 0) {
            container.innerHTML = "<p>No security events found.</p>";
            return;
        }

        events.forEach(event => {

            container.innerHTML += `
                <div class="event">
                    <span class="event-icon">🔴</span>
                    <div>
                        <strong>${event.event_type}</strong><br>

                        <small>
                            User: ${event.user}<br>
                            Severity: ${event.severity}<br>
                            Asset: ${event.asset}<br>
                            ${event.timestamp}
                        </small>
                    </div>
                </div>
            `;

        });

    }
    catch (error) {

        console.error("Events Error:", error);

        document.getElementById("recent-events").innerHTML =
            "<p>Could not connect to Django backend.</p>";

    }
}


// =========================
// Load AI Analysis
// =========================
async function loadAIAnalysis() {

    try {

        const response = await fetch(AI_URL);
        const ai = await response.json();

        const container = document.getElementById("ai-analysis");

        container.innerHTML = `
            <div class="ai-summary">

                <div>
                    <span>Threat Level</span>
                    <strong>${ai.threat_level}</strong>
                </div>

                <div>
                    <span>Risk Score</span>
                    <strong>${ai.risk_score}</strong>
                </div>

            </div>

            <div class="ai-explanation">

                <h3>Evidence</h3>

                <ul>
                    ${ai.evidence.map(item => `<li>${item}</li>`).join("")}
                </ul>

            </div>

            <div class="ai-recommendation">

                <h3>MITRE ATT&CK</h3>

                <ul>
                    ${ai.mitre.map(item =>
                        `<li>${item.id} - ${item.technique}</li>`
                    ).join("")}
                </ul>

                <h3>Recommended Actions</h3>

                <ul>
                    ${ai.recommended_actions.map(action =>
                        `<li>${action}</li>`
                    ).join("")}
                </ul>

            </div>
        `;

    }
    catch (error) {

        console.error("AI Error:", error);

        document.getElementById("ai-analysis").innerHTML =
            "<p>Unable to load AI analysis.</p>";

    }

}


// =========================
// Start Loading
// =========================
loadEvents();
loadAIAnalysis();