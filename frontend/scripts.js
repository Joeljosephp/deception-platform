const API_URL =
    "http://127.0.0.1:8000/api/events/?format=json";

const AI_URL =
    "http://127.0.0.1:8000/api/analysis/";

const DASHBOARD_URL =
    "http://127.0.0.1:8000/api/dashboard/";


// ==========================================================
// Load Recent Security Events
// ==========================================================

async function loadEvents() {

    try {

        const response = await fetch(API_URL);

        if (!response.ok) {
            throw new Error(
                `Events API returned ${response.status}`
            );
        }

        const events = await response.json();

        const container =
            document.getElementById("recent-events");

        container.innerHTML = "";

        if (events.length === 0) {

            container.innerHTML =
                "<p>No security events found.</p>";

            // Also clear timeline
            loadThreatTimeline([]);

            return;
        }

        // --------------------------------------------------
        // Recent Events
        // --------------------------------------------------

        events.forEach(event => {

            container.innerHTML += `
                <div class="event">

                    <span class="event-icon">🔴</span>

                    <div>

                        <strong>
                            ${event.event_type}
                        </strong>

                        <br>

                        <small>
                            User: ${event.user}<br>
                            Severity: ${event.severity || "Unknown"}<br>
                            Asset: ${event.asset}<br>
                            ${formatTimestamp(event.timestamp)}
                        </small>

                    </div>

                </div>
            `;

        });


        // --------------------------------------------------
        // Build Timeline From Same Events
        // --------------------------------------------------

        loadThreatTimeline(events);

    }

    catch (error) {

        console.error(
            "Events Error:",
            error
        );

        document.getElementById(
            "recent-events"
        ).innerHTML =
            "<p>Could not connect to Django backend.</p>";

        document.getElementById(
            "threat-timeline"
        ).innerHTML =
            "<p>Could not load threat timeline.</p>";
    }
}


// ==========================================================
// Format Timestamp
// ==========================================================

function formatTimestamp(timestamp) {

    if (!timestamp) {
        return "Unknown time";
    }

    const date = new Date(timestamp);

    if (isNaN(date.getTime())) {
        return timestamp;
    }

    return date.toLocaleString();
}


// ==========================================================
// Load Dynamic Threat Timeline
// ==========================================================

function loadThreatTimeline(events) {

    const container =
        document.getElementById("threat-timeline");

    if (!container) {
        return;
    }

    container.innerHTML = "";


    // --------------------------------------------------
    // No Events
    // --------------------------------------------------

    if (!events || events.length === 0) {

        container.innerHTML =
            "<p>No security activity detected.</p>";

        return;
    }


    // --------------------------------------------------
    // Show Events In Chronological Order
    // --------------------------------------------------

    const timelineEvents = [...events].sort(
        (a, b) =>
            new Date(a.timestamp) -
            new Date(b.timestamp)
    );


    timelineEvents.forEach(event => {

        const date =
            new Date(event.timestamp);

        const time =
            date.toLocaleTimeString([], {
                hour: "2-digit",
                minute: "2-digit"
            });


        let title =
            event.event_type || "Security Event";

        let description =
            `${event.action || "Activity"} detected on ${event.asset || "unknown asset"}`;


        // --------------------------------------------------
        // Honeytoken Access
        // --------------------------------------------------

        if (
            event.event_type ===
            "honeytoken_access"
        ) {

            title =
                "Honeytoken Accessed";

            description =
                `Deceptive credential accessed by ${event.user}`;
        }


        // --------------------------------------------------
        // Fake Document
        // --------------------------------------------------

        else if (
            event.event_type ===
            "fake_document"
        ) {

            title =
                "Fake Document Accessed";

            description =
                `Deceptive document ${event.asset} was accessed by ${event.user}`;
        }


        // --------------------------------------------------
        // Network Scan
        // --------------------------------------------------

        else if (
            event.event_type ===
            "network_scan"
        ) {

            title =
                "Network Scan Detected";

            description =
                `Suspicious scanning activity from ${event.source_ip}`;
        }


        // --------------------------------------------------
        // Generic Scan
        // --------------------------------------------------

        else if (
            event.action === "scan"
        ) {

            title =
                "Suspicious Scan Detected";

            description =
                `Scanning activity detected from ${event.source_ip}`;
        }


        // --------------------------------------------------
        // Generic Event
        // --------------------------------------------------

        else {

            title =
                event.event_type ||
                "Security Event";

            description =
                `${event.action || "Activity"} performed by ${event.user || "unknown user"} on ${event.asset || "unknown asset"}`;
        }


        // --------------------------------------------------
        // Add Timeline Item
        // --------------------------------------------------

        container.innerHTML += `

            <div class="timeline-item">

                <span class="timeline-time">
                    ${time}
                </span>

                <div>

                    <strong>
                        ${title}
                    </strong>

                    <small>
                        ${description}
                    </small>

                </div>

            </div>

        `;

    });
}


// ==========================================================
// Load AI Threat Analysis
// ==========================================================

async function loadAIAnalysis() {

    try {

        const response =
            await fetch(AI_URL);

        if (!response.ok) {
            throw new Error(
                `AI API returned ${response.status}`
            );
        }

        const ai =
            await response.json();

        const container =
            document.getElementById("ai-analysis");


        // --------------------------------------------------
        // Evidence
        // --------------------------------------------------

        const evidenceHTML =
            ai.evidence &&
            ai.evidence.length > 0

                ? ai.evidence
                    .map(
                        item =>
                            `<li>${item}</li>`
                    )
                    .join("")

                : "<li>No evidence available.</li>";


        // --------------------------------------------------
        // Why Suspicious
        // --------------------------------------------------

        const suspiciousHTML =
            ai.ai_summary &&
            ai.ai_summary.why_suspicious &&
            ai.ai_summary.why_suspicious.length > 0

                ? ai.ai_summary.why_suspicious
                    .map(
                        reason =>
                            `<li>${reason}</li>`
                    )
                    .join("")

                : "<li>No suspicious behavior explanation available.</li>";


        // --------------------------------------------------
        // Recommended Response
        // --------------------------------------------------

        const recommendedHTML =
            ai.ai_summary &&
            ai.ai_summary.recommended_response &&
            ai.ai_summary.recommended_response.length > 0

                ? ai.ai_summary.recommended_response
                    .map(
                        action =>
                            `<li>${action}</li>`
                    )
                    .join("")

                : "<li>No recommended actions available.</li>";


        // --------------------------------------------------
        // MITRE ATT&CK
        // --------------------------------------------------

        const mitreHTML =
            ai.mitre &&
            ai.mitre.length > 0

                ? ai.mitre
                    .map(
                        technique =>
                            `
                            <li>
                                <strong>
                                    ${technique.id}
                                </strong>
                                -
                                ${technique.technique}
                            </li>
                            `
                    )
                    .join("")

                : "<li>No MITRE ATT&CK techniques identified.</li>";


        // --------------------------------------------------
        // Threat Summary
        // --------------------------------------------------

        const threatSummary =
            ai.ai_summary &&
            ai.ai_summary.threat_summary

                ? ai.ai_summary.threat_summary

                : "No AI threat summary available.";


        // --------------------------------------------------
        // Analyst Assessment
        // --------------------------------------------------

        const analystAssessment =
            ai.ai_summary &&
            ai.ai_summary.analyst_assessment

                ? ai.ai_summary.analyst_assessment

                : "No analyst assessment available.";


        // --------------------------------------------------
        // Render AI Analysis
        // --------------------------------------------------

        container.innerHTML = `

            <div class="ai-summary">

                <h3>Threat Level</h3>

                <p>
                    <strong>
                        ${ai.threat_level}
                    </strong>
                </p>


                <h3>Risk Score</h3>

                <p>
                    <strong>
                        ${ai.risk_score} / 100
                    </strong>
                </p>

            </div>


            <div class="ai-explanation">

                <h3>Threat Summary</h3>

                <p>
                    ${threatSummary}
                </p>


                <h3>Why This Is Suspicious</h3>

                <ul>
                    ${suspiciousHTML}
                </ul>

            </div>


            <div class="ai-recommendation">

                <h3>Analyst Assessment</h3>

                <p>
                    ${analystAssessment}
                </p>


                <h3>Recommended Response</h3>

                <ul>
                    ${recommendedHTML}
                </ul>

            </div>


            <div class="ai-evidence">

                <h3>Evidence</h3>

                <ul>
                    ${evidenceHTML}
                </ul>

            </div>


            <div class="ai-mitre">

                <h3>MITRE ATT&CK</h3>

                <ul>
                    ${mitreHTML}
                </ul>

            </div>

        `;

    }

    catch (error) {

        console.error(
            "AI Analysis Error:",
            error
        );

        document.getElementById(
            "ai-analysis"
        ).innerHTML =
            "<p>Unable to load AI analysis.</p>";
    }
}


// ==========================================================
// Load Dashboard Statistics
// ==========================================================

async function loadDashboardStats() {

    try {

        const response =
            await fetch(DASHBOARD_URL);

        if (!response.ok) {
            throw new Error(
                `Dashboard API returned ${response.status}`
            );
        }

        const stats =
            await response.json();


        // --------------------------------------------------
        // Active Decoys
        // --------------------------------------------------

        document.getElementById(
            "active-decoys"
        ).textContent =
            stats.active_decoys;


        // --------------------------------------------------
        // Threats
        // --------------------------------------------------

        document.getElementById(
            "threat-count"
        ).textContent =
            stats.threats;


        // --------------------------------------------------
        // Alerts
        // --------------------------------------------------

        document.getElementById(
            "alert-count"
        ).textContent =
            stats.alerts;


        // --------------------------------------------------
        // Incidents
        // --------------------------------------------------

        document.getElementById(
            "incident-count"
        ).textContent =
            stats.incidents;

    }

    catch (error) {

        console.error(
            "Dashboard Stats Error:",
            error
        );


        document.getElementById(
            "active-decoys"
        ).textContent = "—";


        document.getElementById(
            "threat-count"
        ).textContent = "—";


        document.getElementById(
            "alert-count"
        ).textContent = "—";


        document.getElementById(
            "incident-count"
        ).textContent = "—";
    }
}


// ==========================================================
// Start Loading Dashboard
// ==========================================================

loadEvents();

loadAIAnalysis();

loadDashboardStats();