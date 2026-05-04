from fastapi import FastAPI, BackgroundTasks, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
import asyncio
import json
import os

from core import monitor, report, alerts

app = FastAPI(title="Secure File Transfer Monitoring System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the directory where this file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Serve static files for the frontend
static_dir = os.path.join(BASE_DIR, "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def read_root():
    static_index = os.path.join(BASE_DIR, "static", "index.html")
    if os.path.exists(static_index):
        return FileResponse(static_index)
    return {"message": "Welcome to Secure File Transfer Monitoring System"}

@app.post("/api/start")
def start_monitor():
    sensitive_data_dir = os.path.join(BASE_DIR, "SensitiveData")
    simulated_usb_dir = os.path.join(BASE_DIR, "SimulatedUSB")
    os.makedirs(sensitive_data_dir, exist_ok=True)
    os.makedirs(simulated_usb_dir, exist_ok=True)
    monitor.start_monitoring(sensitive_data_dir)
    return {"status": "Monitoring Started"}

@app.post("/api/stop")
def stop_monitor():
    monitor.stop_monitoring()
    return {"status": "Monitoring Stopped"}

@app.get("/api/status")
def get_status():
    is_active = monitor.observer is not None and monitor.observer.is_alive()
    return {"active": is_active}

@app.post("/api/simulate")
def simulate_breach():
    import time
    sensitive_data_dir = os.path.join(BASE_DIR, "SensitiveData")
    os.makedirs(sensitive_data_dir, exist_ok=True)
    file_path = os.path.join(sensitive_data_dir, f"simulated_leak_{int(time.time())}.txt")
    with open(file_path, "w") as f:
        f.write("Simulated sensitive data access for demonstration purposes.")
    return {"status": "Simulated breach triggered", "file": file_path}

@app.get("/api/report")
def download_report():
    report_file = os.path.join(BASE_DIR, "web_security_report.txt")
    success = report.generate_report(report_file)
    if success and os.path.exists(report_file):
        return FileResponse(report_file, media_type="text/plain", filename="Security_Audit_Report.txt")
    raise HTTPException(status_code=500, detail="Failed to generate report")

@app.get("/api/alerts")
async def stream_alerts(request: Request):
    """Server-Sent Events endpoint to stream alerts to the frontend."""
    async def event_generator():
        q = asyncio.Queue()
        loop = asyncio.get_running_loop()
        
        def callback(alert_json_str):
            try:
                loop.call_soon_threadsafe(q.put_nowait, alert_json_str)
            except Exception:
                pass
                
        alerts.subscribe(callback)
        
        try:
            while True:
                if await request.is_disconnected():
                    break
                    
                try:
                    alert_json_str = await asyncio.wait_for(q.get(), timeout=1.0)
                    yield alert_json_str
                except asyncio.TimeoutError:
                    pass
        finally:
            alerts.unsubscribe(callback)
            
    return EventSourceResponse(event_generator())

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
