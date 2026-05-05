from flask import Flask, render_template, jsonify, send_file
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

app = Flask(__name__)

monitoring = False
alerts = []
observer = None

WATCH_FOLDER = "SensitiveData"


# 🔥 HANDLE FILE EVENTS (NO DUPLICATES)
class MonitorHandler(FileSystemEventHandler):
    last_events = {}

    def log_event(self, event_type, file_path):
        filename = os.path.basename(file_path)
        key = f"{event_type}-{filename}"

        current_time = time.time()

        # ⛔ Ignore duplicate same event within 2 sec
        if key in self.last_events:
            if current_time - self.last_events[key] < 2:
                return

        self.last_events[key] = current_time

        alerts.append({
            "message": f"{event_type}: {filename}",
            "time": time.strftime("%H:%M:%S")
        })

    def on_created(self, event):
        if not event.is_directory:
            self.log_event("File created", event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self.log_event("File modified", event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            self.log_event("File deleted", event.src_path)


# ▶ START MONITORING
@app.route('/start', methods=['POST'])
def start():
    global monitoring, observer

    if not monitoring:
        event_handler = MonitorHandler()
        observer = Observer()
        observer.schedule(event_handler, WATCH_FOLDER, recursive=True)
        observer.start()
        monitoring = True

        # clear old alerts
        alerts.clear()

        alerts.append({
            "message": "Monitoring started",
            "time": time.strftime("%H:%M:%S")
        })

    return jsonify({"status": "active"})


# ⏹ STOP MONITORING
@app.route('/stop', methods=['POST'])
def stop():
    global monitoring, observer

    if monitoring and observer:
        observer.stop()
        observer.join()
        monitoring = False

        alerts.append({
            "message": "Monitoring stopped",
            "time": time.strftime("%H:%M:%S")
        })

    return jsonify({"status": "inactive"})


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/status')
def status():
    return jsonify({"monitoring": monitoring})


@app.route('/alerts')
def get_alerts():
    return jsonify(alerts[-10:])  # last 10 alerts


@app.route('/download')
def download():
    filename = "audit_report.txt"

    with open(filename, "w") as f:
        f.write("=== Audit Report ===\n\n")
        for a in alerts:
            f.write(f"{a['time']} - {a['message']}\n")

    return send_file(filename, as_attachment=True)


if __name__ == '__main__':
    if not os.path.exists(WATCH_FOLDER):
        os.makedirs(WATCH_FOLDER)

    app.run(debug=True)