const ATTACKERS_URL =
    "http://127.0.0.1:8000/api/attackers/";


// =====================================================
// Load Attackers
// =====================================================

async function loadAttackers() {

    try {

        const response = await fetch(ATTACKERS_URL);

        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }

        const attackers = await response.json();

        const container =
            document.getElementById("attackers-list");

        container.innerHTML = "";


        if (attackers.length === 0) {

            container.innerHTML =
                "<p>No attackers found.</p>";

            return;
        }


        attackers.forEach(attacker => {

            const card = document.createElement("div");

            // =================================================
            // Attacker Card Styling
            // =================================================

            card.style.display = "flex";
            card.style.justifyContent = "space-between";
            card.style.alignItems = "center";
            card.style.backgroundColor = "#111827";
            card.style.border = "1px solid #263244";
            card.style.borderRadius = "10px";
            card.style.padding = "20px";
            card.style.marginBottom = "15px";
            card.style.gap = "20px";


            // =================================================
            // Attacker Information
            // =================================================

            const info = document.createElement("div");

            info.innerHTML = `

                <h3 style="
                    margin-bottom: 10px;
                    color: #e5e7eb;
                ">
                    🔴 ${attacker.name}
                </h3>

                <p style="
                    color: #9ca3af;
                    margin-bottom: 6px;
                ">
                    Source IP:
                    ${attacker.source_ip}
                </p>

                <p style="
                    color: #9ca3af;
                ">
                    Status:
                    ${attacker.status}
                </p>

            `;


            // =================================================
            // Button Container
            // =================================================

            const buttons = document.createElement("div");

            buttons.style.display = "flex";
            buttons.style.flexDirection = "column";
            buttons.style.gap = "10px";
            buttons.style.minWidth = "240px";


            // =================================================
            // Honeytoken Button
            // =================================================

            const honeytokenButton =
                createAttackButton(
                    "🪪 Honeytoken Attack",
                    attacker.id,
                    "honeytoken"
                );


            // =================================================
            // Document Button
            // =================================================

            const documentButton =
                createAttackButton(
                    "📄 Fake Document Attack",
                    attacker.id,
                    "document"
                );


            // =================================================
            // Scan Button
            // =================================================

            const scanButton =
                createAttackButton(
                    "🔎 Admin API Scan",
                    attacker.id,
                    "scan"
                );


            // Add buttons

            buttons.appendChild(honeytokenButton);
            buttons.appendChild(documentButton);
            buttons.appendChild(scanButton);


            // Add information + buttons

            card.appendChild(info);
            card.appendChild(buttons);

            container.appendChild(card);

        });

    }

    catch (error) {

        console.error(
            "Attacker loading error:",
            error
        );

        document.getElementById(
            "attackers-list"
        ).innerHTML = `
            <p style="color: #ef4444;">
                Unable to load attackers.
            </p>
        `;

    }

}


// =====================================================
// Create Attack Button
// =====================================================

function createAttackButton(
    text,
    attackerId,
    attackType
) {

    const button =
        document.createElement("button");


    button.textContent = text;


    // =================================================
    // DIRECT BUTTON CSS
    // =================================================

    button.style.display = "block";

    button.style.width = "240px";

    button.style.backgroundColor =
        "#172033";

    button.style.color =
        "#e5e7eb";

    button.style.border =
        "1px solid #6366f1";

    button.style.borderRadius =
        "8px";

    button.style.padding =
        "12px 16px";

    button.style.fontFamily =
        "Arial, sans-serif";

    button.style.fontSize =
        "14px";

    button.style.fontWeight =
        "bold";

    button.style.cursor =
        "pointer";

    button.style.textAlign =
        "center";

    button.style.transition =
        "all 0.2s ease";


    // =================================================
    // Hover
    // =================================================

    button.addEventListener(
        "mouseenter",
        function () {

            button.style.backgroundColor =
                "#263244";

            button.style.borderColor =
                "#818cf8";

            button.style.color =
                "#ffffff";

            button.style.transform =
                "translateY(-2px)";
        }
    );


    // =================================================
    // Mouse Leave
    // =================================================

    button.addEventListener(
        "mouseleave",
        function () {

            button.style.backgroundColor =
                "#172033";

            button.style.borderColor =
                "#6366f1";

            button.style.color =
                "#e5e7eb";

            button.style.transform =
                "translateY(0)";
        }
    );


    // =================================================
    // Click
    // =================================================

    button.addEventListener(
        "click",
        function () {

            simulateAttack(
                attackerId,
                attackType
            );

        }
    );


    return button;
}


// =====================================================
// Simulate Attack
// =====================================================

async function simulateAttack(
    attackerId,
    attackType
) {

    try {

        const response = await fetch(

            `http://127.0.0.1:8000/api/attackers/${attackerId}/simulate/`,

            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

                    attack_type:
                        attackType,

                    timestamp:
                        new Date().toISOString(),

                    incident_id:
                        `INC-${attackerId}-${Date.now()}`
                })
            }
        );


        const result =
            await response.json();


        if (!response.ok) {

            throw new Error(
                result.error ||
                `HTTP error: ${response.status}`
            );

        }


        console.log(
            "Attack simulation result:",
            result
        );


        showAttackResult(result);

    }

    catch (error) {

        console.error(
            "Attack simulation error:",
            error
        );

        alert(
            "Attack simulation failed: " +
            error.message
        );

    }

}


// =====================================================
// Display AI Result
// =====================================================

function showAttackResult(result) {

    const ai =
        result.ai_analysis;

    const summary =
        ai.ai_summary;


    const resultSection =
        document.getElementById(
            "attack-result-section"
        );

    const resultContainer =
        document.getElementById(
            "attack-result"
        );


    if (!resultSection || !resultContainer) {

        alert(
            `Attack simulated successfully!\n\n` +
            `Attacker: ${result.attacker.name}\n` +
            `Attack: ${result.event.event_type}\n` +
            `Risk Score: ${ai.risk_score}/100\n` +
            `Threat Level: ${ai.threat_level}\n\n` +
            `${summary.threat_summary}`
        );

        return;
    }


    resultSection.style.display =
        "block";


    resultContainer.innerHTML = `

        <div style="
            background:#172033;
            padding:20px;
            border-radius:10px;
            border:1px solid #263244;
        ">

            <h3 style="
                margin-bottom:15px;
            ">
                ${result.attacker.name}
            </h3>


            <p>
                <strong>Attack:</strong>
                ${result.event.event_type}
            </p>


            <p>
                <strong>Risk Score:</strong>
                ${ai.risk_score}/100
            </p>


            <p>
                <strong>Threat Level:</strong>
                ${ai.threat_level}
            </p>


            <h3 style="
                margin-top:20px;
                margin-bottom:8px;
            ">
                AI Summary
            </h3>

            <p>
                ${summary.threat_summary}
            </p>


            <h3 style="
                margin-top:20px;
                margin-bottom:8px;
            ">
                Analyst Assessment
            </h3>

            <p>
                ${summary.analyst_assessment}
            </p>

        </div>

    `;

}


// =====================================================
// Start
// =====================================================

loadAttackers();