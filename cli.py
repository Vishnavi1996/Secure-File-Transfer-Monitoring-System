import argparse
import sys
import time
import json
import os
from colorama import init, Fore, Style

from core import monitor, report, alerts

init(autoreset=True)

def print_alert(alert_json_str):
    """Callback to print alerts to the console."""
    try:
        alert_data = json.loads(alert_json_str)
        title = alert_data.get("title", "")
        message = alert_data.get("message", "")
        severity = alert_data.get("severity", "info")
        
        color = Fore.WHITE
        if severity == "critical":
            color = Fore.RED + Style.BRIGHT
        elif severity == "warning":
            color = Fore.YELLOW
        elif severity == "info":
            color = Fore.CYAN
            
        print(f"{color}[ALERT] {title}: {message}")
    except Exception as e:
        print(f"Error parsing alert: {e}")

def main():
    parser = argparse.ArgumentParser(description="Secure File Transfer Monitoring System CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Start command
    start_parser = subparsers.add_parser("start", help="Start monitoring the directory")
    
    # Stop command
    stop_parser = subparsers.add_parser("stop", help="Stop monitoring") # Note: stop via CLI for a background process is complex, here we just run it in foreground.
    
    # Report command
    report_parser = subparsers.add_parser("report", help="Generate a security report")
    report_parser.add_argument("--output", default="security_report.txt", help="Output file name")
    
    args = parser.parse_args()
    
    if args.command == "start":
        os.makedirs("SensitiveData", exist_ok=True)
        os.makedirs("SimulatedUSB", exist_ok=True)
        print(Fore.GREEN + "Starting Security Monitor... Press Ctrl+C to stop.")
        alerts.subscribe(print_alert)
        monitor.start_monitoring("SensitiveData")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print(Fore.YELLOW + "\nStopping Monitor...")
            monitor.stop_monitoring()
            print(Fore.GREEN + "Monitor stopped.")
            sys.exit(0)
            
    elif args.command == "stop":
        print(Fore.YELLOW + "Note: The monitor runs in the foreground. To stop it, press Ctrl+C in the terminal where it was started.")
            
    elif args.command == "report":
        print(Fore.CYAN + f"Generating report to {args.output}...")
        report.generate_report(args.output)
        print(Fore.GREEN + "Report generated successfully. You can now view the decrypted logs.")
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
