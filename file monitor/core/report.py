import os
import json
from . import db
from . import crypto

def generate_report(output_file: str = "security_report.txt") -> bool:
    """Extracts, decrypts logs, and generates a report file."""
    logs = db.get_all_logs()
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("SECURE FILE TRANSFER MONITORING SYSTEM - AUDIT REPORT\n")
        f.write("=" * 60 + "\n\n")
        
        suspicious_count = 0
        total_count = len(logs)
        
        # We will iterate through logs twice: once for summary, once for details
        detailed_entries = []
        
        for row in logs:
            log_id, timestamp, encrypted_data = row
            decrypted_json_str = crypto.decrypt(encrypted_data)
            
            if decrypted_json_str == "<Decryption Failed>":
                detailed_entries.append(f"[{timestamp}] ERROR: Could not decrypt log entry {log_id}")
                continue
                
            try:
                data = json.loads(decrypted_json_str)
                event_type = data.get("event_type", "Unknown")
                file_path = data.get("file_path", "")
                dest_path = data.get("dest_path", "")
                is_suspicious = data.get("is_suspicious", False)
                details = data.get("details", "")
                
                if is_suspicious:
                    suspicious_count += 1
                
                status_flag = "[!] SUSPICIOUS" if is_suspicious else "[ ] NORMAL"
                
                entry = f"{status_flag} {timestamp} - {event_type}\n"
                entry += f"    Source: {file_path}\n"
                if dest_path:
                    entry += f"    Dest:   {dest_path}\n"
                entry += f"    Details: {details}\n"
                detailed_entries.append(entry)
                
            except json.JSONDecodeError:
                detailed_entries.append(f"[{timestamp}] ERROR: Invalid JSON in decrypted log {log_id}")
        
        f.write("SUMMARY\n")
        f.write("-" * 20 + "\n")
        f.write(f"Total Events Logged: {total_count}\n")
        f.write(f"Suspicious Events:   {suspicious_count}\n\n")
        
        f.write("DETAILED EVENT LOG\n")
        f.write("-" * 20 + "\n")
        for entry in detailed_entries:
            f.write(entry + "\n")
            
    return True
