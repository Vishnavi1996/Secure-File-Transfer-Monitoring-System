let lastAlertCount = 0;

async function checkStatus() {
    const res = await fetch('/status');
    const data = await res.json();

    document.getElementById("statusText").innerText =
        data.monitoring ? "Monitoring Active" : "Monitoring Inactive";
}

async function loadAlerts() {
    const res = await fetch('/alerts');
    const data = await res.json();

    // ⛔ Prevent re-render duplicates
    if (data.length === lastAlertCount) return;

    lastAlertCount = data.length;

    const alertList = document.getElementById("alertList");
    alertList.innerHTML = "";

    data.slice().reverse().forEach(a => {
        const alertEl = document.createElement('div');

        // 🔥 Apply box style
        alertEl.className = "alert";

        // 🔥 Choose icon + type based on message
        let icon = "ℹ️";
        let title = "System";

        if (a.message.includes("created")) {
            icon = "📁";
            title = "File Created";
        } else if (a.message.includes("modified")) {
            icon = "⚡";
            title = "File Modified";
        } else if (a.message.includes("deleted")) {
            icon = "⚠️";
            title = "File Deleted";
        } else if (a.message.includes("Monitoring")) {
            icon = "🛡️";
            title = "System";
        }

        alertEl.innerHTML = `
            <strong>${icon} ${title}</strong>
            <span>${a.message} (${a.time})</span>
        `;

        alertList.appendChild(alertEl);
    });
}

// Buttons
document.getElementById("startBtn").onclick = async () => {
    await fetch('/start', { method: 'POST' });
    checkStatus();
};

document.getElementById("stopBtn").onclick = async () => {
    await fetch('/stop', { method: 'POST' });
    checkStatus();
};

document.getElementById("reportBtn").onclick = () => {
    window.location.href = '/download';
};

// Auto refresh
setInterval(() => {
    checkStatus();
    loadAlerts();
}, 3000);

// Initial load
checkStatus();
loadAlerts();