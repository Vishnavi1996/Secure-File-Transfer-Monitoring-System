import json
from typing import List, Callable

# Simple in-memory alert pub-sub
_subscribers: List[Callable] = []

def subscribe(callback: Callable):
    """Subscribe a callback function to alerts."""
    if callback not in _subscribers:
        _subscribers.append(callback)

def unsubscribe(callback: Callable):
    """Unsubscribe a callback function from alerts."""
    if callback in _subscribers:
        _subscribers.remove(callback)

def publish_alert(alert_data: dict):
    """Publish an alert to all subscribers."""
    # Ensure standard format for alerts
    alert_json = json.dumps(alert_data)
    for callback in list(_subscribers):
        try:
            callback(alert_json)
        except Exception as e:
            print(f"Error publishing to subscriber: {e}")

def trigger_alert(title: str, message: str, severity: str = "warning"):
    """Helper to format and publish an alert."""
    alert = {
        "title": title,
        "message": message,
        "severity": severity,  # info, warning, critical
    }
    publish_alert(alert)
