const API_URL = "http://127.0.0.1:8000/api/events/?format=json";

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

    } catch (error) {
        console.error(error);

        document.getElementById("recent-events").innerHTML =
            "<p>Could not connect to Django backend.</p>";
    }
}

loadEvents();