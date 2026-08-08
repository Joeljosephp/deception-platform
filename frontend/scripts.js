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

                    <span class="event-icon"><i data-lucide="alert-circle" style="color: #ef4444; width: 16px; height: 16px;"></i></span>

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
        
        let suspiciousArray = ai.ai_summary && ai.ai_summary.why_suspicious ? ai.ai_summary.why_suspicious : [];
        if (!Array.isArray(suspiciousArray)) suspiciousArray = [suspiciousArray];

        const suspiciousHTML =
            suspiciousArray.length > 0

                ? suspiciousArray
                    .map(
                        reason =>
                            `<li>${reason}</li>`
                    )
                    .join("")

                : "<li>No suspicious behavior explanation available.</li>";


        // --------------------------------------------------
        // Recommended Response
        // --------------------------------------------------
        
        let recommendedArray = ai.ai_summary && ai.ai_summary.recommended_response ? ai.ai_summary.recommended_response : [];
        if (!Array.isArray(recommendedArray)) recommendedArray = [recommendedArray];

        const recommendedHTML =
            recommendedArray.length > 0

                ? recommendedArray
                    .map(
                        action =>
                            `<button class="remediation-btn" onclick="executeRemediation('${action.replace(/'/g, "\\'")}', this)">
                                <i data-lucide="zap" style="width: 16px; height: 16px; display: inline-block; vertical-align: middle; margin-right: 4px;"></i>
                                Execute: ${action}
                            </button>`
                    )
                    .join("")

                : "<p>No recommended actions available.</p>";


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

        const aiPanel = document.querySelector(".ai-panel");
        if (aiPanel) {
            if (ai.threat_level === "CRITICAL") {
                aiPanel.classList.add("critical-glow");
            } else {
                aiPanel.classList.remove("critical-glow");
            }
        }

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

                <div class="remediation-container">
                    ${recommendedHTML}
                </div>

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

        // Initialize scroll reveal on new AI panel
        initScrollReveal();

        // Initialize Lucide icons
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }

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


        document.getElementById("alert-count").textContent =
            stats.alerts;

        document.getElementById("incident-count").textContent =
            stats.incidents;

        // Initialize scroll reveal on new stats
        initScrollReveal();

        // Initialize Chart with REAL data
        if (typeof initChart === "function" && stats.chart_data) {
            initChart(stats.chart_data);
        }

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

// ==========================================================
// Remediation Execution Animation
// ==========================================================

window.executeRemediation = function(action, buttonElement) {
    
    if (buttonElement) {
        buttonElement.disabled = true;
        buttonElement.style.opacity = '0.5';
        buttonElement.style.cursor = 'not-allowed';
    }

    // Create terminal overlay
    const overlay = document.createElement("div");
    overlay.className = "terminal-overlay";
    
    const terminal = document.createElement("div");
    terminal.className = "terminal-window";
    
    terminal.innerHTML = `
        <div class="terminal-header">
            <span style="display: flex; gap: 6px;">
                <span style="width: 12px; height: 12px; border-radius: 50%; background-color: #ef4444;"></span>
                <span style="width: 12px; height: 12px; border-radius: 50%; background-color: #f59e0b;"></span>
                <span style="width: 12px; height: 12px; border-radius: 50%; background-color: #10b981;"></span>
            </span>
            <span>root@ciphrex-soc</span>
        </div>
        <div class="terminal-body" id="terminal-body">
            <p>> Initializing security protocol: ${action}</p>
        </div>
    `;
    
    overlay.appendChild(terminal);
    document.body.appendChild(overlay);

    const body = document.getElementById("terminal-body");
    
    setTimeout(() => { body.innerHTML += "<p>> Authenticating SOC admin... <span style='color:#4ade80'>SUCCESS</span></p>"; }, 600);
    setTimeout(() => { body.innerHTML += "<p>> Locating target asset in environment...</p>"; }, 1200);
    setTimeout(() => { body.innerHTML += "<p>> Deploying counter-measures...</p>"; }, 1800);
    setTimeout(() => { 
        body.innerHTML += "<p style='color: #4ade80; font-weight: bold;'>> ACTION COMPLETED SUCCESSFULLY.</p>"; 
        
        if (buttonElement) {
            buttonElement.innerHTML = `<i data-lucide="check" style="width: 16px; height: 16px; display: inline-block; vertical-align: middle; margin-right: 4px;"></i> Executed`;
            buttonElement.style.backgroundColor = '#10b981';
            buttonElement.style.borderColor = '#10b981';
            buttonElement.style.color = '#ffffff';
            buttonElement.style.opacity = '1';
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            }
        }
    }, 2400);
    
    setTimeout(() => { 
        body.innerHTML += "<button class='terminal-close-btn' onclick='document.body.removeChild(this.parentElement.parentElement.parentElement)'>Close Terminal</button>"; 
    }, 2800);
};

// ==========================================================
// Chat Logic
// ==========================================================

window.sendChatMessage = async function() {
    const input = document.getElementById("chat-input");
    const history = document.getElementById("chat-history");
    const question = input.value.trim();
    
    if (!question) return;
    
    // Clear initial text
    if (history.innerHTML.includes("Ask me anything")) {
        history.innerHTML = "";
    }
    
    // Add user message
    history.innerHTML += `<div class="chat-msg user">${question}</div>`;
    input.value = "";
    
    // Add typing indicator
    const typingId = "typing-" + Date.now();
    history.innerHTML += `<div id="${typingId}" class="chat-msg ai">CIPHREX-AI is typing...</div>`;
    history.scrollTop = history.scrollHeight;
    
    try {
        const response = await fetch("http://127.0.0.1:8000/api/chat/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: question })
        });
        
        const result = await response.json();
        
        // Replace typing indicator with response
        document.getElementById(typingId).innerHTML = result.answer.replace(/\n/g, '<br>');
        
    } catch (error) {
        console.error("Chat error:", error);
        document.getElementById(typingId).innerHTML = "Sorry, I encountered a network error.";
        document.getElementById(typingId).style.color = "#ef4444";
    }
    
    history.scrollTop = history.scrollHeight;
};

// ==========================================================
// Scroll Reveal Observer
// ==========================================================

window.initScrollReveal = function() {
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.reveal-on-scroll, .content-section, .stat-card').forEach(el => {
        if (!el.classList.contains('reveal-on-scroll')) {
            el.classList.add('reveal-on-scroll');
        }
        observer.observe(el);
    });
};

// Initialize on page load
document.addEventListener("DOMContentLoaded", initScrollReveal);

// ==========================================================
// Mouse-Tracking Glow Effect (Optimized for 60fps)
// ==========================================================

let isTicking = false;
document.addEventListener("mousemove", e => {
    if (!isTicking) {
        window.requestAnimationFrame(() => {
            document.querySelectorAll(".stat-card, .content-section").forEach(card => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                card.style.setProperty("--x", `${x}px`);
                card.style.setProperty("--y", `${y}px`);
            });
            isTicking = false;
        });
        isTicking = true;
    }
});

// ==========================================================
// Chart.js Initialization
// ==========================================================
let threatChartInstance = null;

window.initChart = function(chartData) {
    const ctx = document.getElementById('threatChart');
    if (!ctx) return;
    
    // Extract real data from backend
    const labels = chartData.map(d => d.time);
    const dataPoints = chartData.map(d => d.count);

    // Glowing gradient
    const gradient = ctx.getContext('2d').createLinearGradient(0, 0, 0, 300);
    gradient.addColorStop(0, 'rgba(99, 102, 241, 0.5)'); // Indigo
    gradient.addColorStop(1, 'rgba(16, 185, 129, 0.0)'); // Emerald fade

    if (threatChartInstance) {
        threatChartInstance.destroy();
    }

    threatChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Detected Threats',
                data: dataPoints,
                borderColor: '#6366f1',
                borderWidth: 2,
                backgroundColor: gradient,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: '#10b981',
                pointBorderColor: '#fff',
                pointRadius: 3,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(17, 24, 39, 0.9)',
                    titleColor: '#fff',
                    bodyColor: '#e5e7eb',
                    borderColor: '#374151',
                    borderWidth: 1
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#9ca3af' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#9ca3af', maxTicksLimit: 8 }
                }
            }
        }
    });
};