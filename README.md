# Secure File Transfer Monitoring System

A comprehensive, cybersecurity-focused system designed to monitor file activities, detect unauthorized transfers, verify file integrity, and enforce Data Loss Prevention (DLP) rules. The system provides real-time observability across three distinct interfaces: Web, Desktop, and CLI.

## Key Features

1. **File Monitoring**: Utilizes `watchdog` to track `Created`, `Modified`, `Moved`, and `Deleted` events in real-time.
2. **File Integrity Verification**: Computes SHA-256 hashes of files before and after events to detect tampering or corruption.
3. **Sensitive File Detection**: Rules engine detects movement of sensitive data (e.g., to simulated USB drives/restricted destinations) and flags unauthorized access.
4. **Encrypted Hidden Logging**: Audit logs are heavily protected. They are encrypted using AES (via `cryptography`) and stored in an SQLite database. Logs are entirely hidden from the UI until a secure report is generated.
5. **Real-time Alerting**: Live alerts are broadcasted instantly to the Web, CLI, and Desktop interfaces via an internal pub/sub system.
6. **Multi-Interface Delivery**: 
    - **Web Dashboard**: FastAPI backend with a premium, dynamic HTML/JS frontend using Server-Sent Events (SSE).
    - **Desktop GUI**: Python Tkinter application featuring a dark-themed monitoring console.
    - **CLI**: Command-line interface for terminal-based observability.

## Prerequisites

- Python 3.8+
- The required dependencies listed below.

## Installation

1. Clone or download this repository.
2. Install the required Python packages:
```bash
pip install watchdog cryptography fastapi uvicorn colorama websockets psutil sse-starlette
```

## Usage

You can interact with the Secure File Transfer Monitoring System through three different interfaces.

### 1. Web Dashboard (Recommended)

The Web App provides a modern, glassmorphism-styled dashboard with real-time alert streaming.

```bash
python web_app.py
```
After starting the server, open your browser and navigate to `http://127.0.0.1:8080`.

### 2. Desktop Application

The Desktop App provides a standalone Tkinter GUI for local monitoring.

```bash
python desktop_app.py
```

### 3. Command Line Interface (CLI)

The CLI provides terminal-based, color-coded alerts.

```bash
# Start monitoring and viewing live alerts
python cli.py start
python cli.py stop

# Generate the audit report
python cli.py report
```

## How It Works

1. **Initialization**: When you start monitoring, the system creates `SensitiveData` and `SimulatedUSB` directories if they do not exist. It monitors `SensitiveData` by default.
2. **Simulation**: Try creating a `.txt` file inside `SensitiveData`. You will see an `INFO` alert.
3. **Unauthorized Transfer**: Try moving that file into `SimulatedUSB`. The system will flag this as a `CRITICAL` alert for an unauthorized transfer.
4. **Audit Reporting**: During active monitoring, logs are encrypted and stored in `logs.db`. To view the complete history (including SHA-256 hashes), click "Download Report" in the Web/Desktop app, or run `python cli.py report`. This action decrypts the data and generates a readable text report.

## Technologies Used

- **Python**: Core language
- **watchdog**: Real-time filesystem event monitoring
- **hashlib**: SHA-256 file integrity hashing
- **cryptography (Fernet/AES)**: Secure encryption for database logs
- **FastAPI / Uvicorn / SSE**: Web backend and real-time streaming
- **Tkinter**: Desktop GUI
- **SQLite**: Local database storage
