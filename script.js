document.addEventListener('DOMContentLoaded', () => {
    const startBtn = document.getElementById('startBtn');
    const stopBtn = document.getElementById('stopBtn');
    const reportBtn = document.getElementById('reportBtn');
    const simulateBtn = document.getElementById('simulateBtn');
    const statusIndicator = document.getElementById('statusIndicator');
    const statusText = document.getElementById('statusText');
    const alertList = document.getElementById('alertList');

    let monitoringActive = false;

    function updateUI(isActive) {
        if (isActive) {
            statusIndicator.classList.add('active');
            statusIndicator.style.background = '#10b981';
            statusText.textContent = "Monitoring Active";
            startBtn.disabled = true;
            stopBtn.disabled = false;
        } else {
            statusIndicator.classList.remove('active');
            statusIndicator.style.background = '#ef4444';
            statusText.textContent = "Monitoring Inactive";
            startBtn.disabled = false;
            stopBtn.disabled = true;
        }
    }

    function addAlert(title, message, severity) {
        const placeholder = document.querySelector('.item-placeholder');
        if (placeholder) placeholder.remove();
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
        if (alertList.children.length > 50) {
            alertList.removeChild(alertList.lastChild);
        }
    }

    startBtn.addEventListener('click', () => {
        monitoringActive = true;
        updateUI(true);
        addAlert("System", "Started monitoring SensitiveData", "info");
        addAlert("Sensitive File Activity", "Sensitive file created: example.txt", "info");
    });

    stopBtn.addEventListener('click', () => {
        monitoringActive = false;
        updateUI(false);
        addAlert("System", "Stopped monitoring", "info");
    });

    simulateBtn.addEventListener('click', () => {
        addAlert("Simulated Breach", "Sensitive data movement was detected.", "critical");
        addAlert("System", "Unauthorized transfer simulation completed.", "warning");
    });

    reportBtn.addEventListener('click', () => {
        addAlert("Audit Report", "Audit report download simulated.", "info");
        alert("Audit report would be downloaded in a real deployment.");
    });

    // Initialize UI
    updateUI(false);
});
