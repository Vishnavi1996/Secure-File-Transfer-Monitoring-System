import time
import os
import hashlib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from . import db
from . import rules
from . import alerts

def get_file_hash(filepath: str) -> str:
    """Calculate SHA256 hash of a file."""
    if not os.path.exists(filepath) or os.path.isdir(filepath):
        return ""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception:
        return ""

class SecurityMonitorHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        self._process_event("Created", event.src_path)

    def on_modified(self, event):
        if event.is_directory:
            return
        self._process_event("Modified", event.src_path)

    def on_deleted(self, event):
        if event.is_directory:
            return
        self._process_event("Deleted", event.src_path)

    def on_moved(self, event):
        if event.is_directory:
            return
        self._process_event("Moved", event.src_path, dest_path=event.dest_path)

    def _process_event(self, event_type: str, src_path: str, dest_path: str = ""):
        # Ignore db files to prevent infinite loops
        if src_path.endswith('.db') or src_path.endswith('.db-journal'):
            return
            
        file_hash = get_file_hash(dest_path if dest_path else src_path)
        is_suspicious = False
        details = f"Hash: {file_hash}"

        # Rule Checks
        if rules.is_sensitive_file(src_path):
            if event_type == "Moved" and dest_path:
                if rules.is_unauthorized_transfer(src_path, dest_path):
                    is_suspicious = True
                    details += f" | UNAUTHORIZED TRANSFER detected to {dest_path}"
                    alerts.trigger_alert(
                        "Unauthorized Transfer",
                        f"Sensitive file moved to restricted destination: {os.path.basename(src_path)}",
                        "critical"
                    )
            elif event_type in ["Created", "Modified"]:
                alerts.trigger_alert(
                    "Sensitive File Activity",
                    f"Sensitive file {event_type.lower()}: {os.path.basename(src_path)}",
                    "info"
                )

        if event_type == "Deleted" and rules.is_sensitive_file(src_path):
             alerts.trigger_alert(
                 "Sensitive File Deleted",
                 f"File deleted: {os.path.basename(src_path)}",
                 "warning"
             )

        db.log_event(
            event_type=event_type,
            file_path=src_path,
            src_path=src_path,
            dest_path=dest_path,
            is_suspicious=is_suspicious,
            details=details
        )

# Global observer
observer = None

def start_monitoring(path: str = "."):
    global observer
    db.init_db()
    if observer is not None and observer.is_alive():
        return
    
    event_handler = SecurityMonitorHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    alerts.trigger_alert("System", f"Started monitoring {path}", "info")

def stop_monitoring():
    global observer
    if observer is not None:
        observer.stop()
        observer.join()
        observer = None
        alerts.trigger_alert("System", "Stopped monitoring", "info")
