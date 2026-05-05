document.addEventListener('DOMContentLoaded', () => {
    const startBtn = document.getElementById('startBtn');
    const stopBtn = document.getElementById('stopBtn');
    const reportBtn = document.getElementById('reportBtn');
    const statusIndicator = document.getElementById('statusIndicator');
    const statusText = document.getElementById('statusText');
    const alertList = document.getElementById('alertList');

    // Check initial status
    fetchStatus();
    
    // Connect to Server-Sent Events for live alerts
    const sse = new EventSource('/api/alerts');
    sse.onmessage = function(event) {
        try {
            const data = JSON.parse(event.data);
            addAlert(data.title, data.message, data.severity);
        } catch(e) {
            console.error("Error parsing alert:", e);
        }
    };

    startBtn.addEventListener('click', async () => {
        try {
            await fetch('/api/start', { method: 'POST' });
            fetchStatus();
        } catch (e) {
            console.error(e);
        }
    });

    stopBtn.addEventListener('click', async () => {
        try {
            await fetch('/api/stop', { method: 'POST' });
            fetchStatus();
        } catch (e) {
            console.error(e);
        }
    });

    reportBtn.addEventListener('click', () => {
        window.location.href = '/api/report';
    });

    async function fetchStatus() {
        try {
            const res = await fetch('/api/status');
            const data = await res.json();
            updateUI(data.active);
        } catch (e) {
            console.error("Could not fetch status");
        }
    }

    function updateUI(isActive) {
        if (isActive) {
            statusIndicator.classList.add('active');
            statusText.textContent = "Monitoring Active";
            startBtn.disabled = true;
            stopBtn.disabled = false;
        } else {
            statusIndicator.classList.remove('active');
            statusText.textContent = "Monitoring Inactive";
            startBtn.disabled = false;
            stopBtn.disabled = true;
        }
    }

    function addAlert(title, message, severity) {
        // Remove placeholder if present
        const placeholder = document.querySelector('.item-placeholder');
        if (placeholder) {
            placeholder.remove();
        }

        const alertEl = document.createElement('div');
        alertEl.className = `alert ${severity}`;
        
        let icon = "ℹ️";
        if (severity === "warning") icon = "⚡";
        if (severity === "critical") icon = "⚠️";

        alertEl.innerHTML = `
            <strong>${icon} ${title}</strong>
            <span>${message}</span>
        `;
        
        alertList.prepend(alertEl);
        
        // Keep list reasonable size
        if (alertList.children.length > 50) {
            alertList.removeChild(alertList.lastChild);
        }
    }
});
