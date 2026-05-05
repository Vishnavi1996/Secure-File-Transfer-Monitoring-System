import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import json
import os

from core import monitor, report, alerts

class SecurityDesktopApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Secure File Transfer Monitor")
        self.geometry("700x500")
        self.configure(bg="#1e1e2e")  # Dark premium theme
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TButton", padding=6, relief="flat", background="#89b4fa", foreground="#11111b", font=("Helvetica", 10, "bold"))
        style.map("TButton", background=[("active", "#b4befe")])
        style.configure("TLabel", background="#1e1e2e", foreground="#cdd6f4", font=("Helvetica", 12))
        style.configure("Title.TLabel", font=("Helvetica", 16, "bold"), foreground="#f38ba8")
        
        # Title
        title_label = ttk.Label(self, text="🛡️ Security Monitor Dashboard", style="Title.TLabel")
        title_label.pack(pady=20)
        
        # Status Label
        self.status_var = tk.StringVar(value="Status: Inactive")
        status_label = ttk.Label(self, textvariable=self.status_var)
        status_label.pack(pady=5)
        
        # Alert Box
        self.alert_box = scrolledtext.ScrolledText(self, width=80, height=15, bg="#181825", fg="#cdd6f4", font=("Consolas", 10), bd=0)
        self.alert_box.pack(pady=10, padx=20)
        self.alert_box.config(state=tk.DISABLED)
        
        # Buttons Frame
        btn_frame = tk.Frame(self, bg="#1e1e2e")
        btn_frame.pack(pady=15)
        
        self.start_btn = ttk.Button(btn_frame, text="Start Monitoring", command=self.start_monitoring)
        self.start_btn.grid(row=0, column=0, padx=10)
        
        self.stop_btn = ttk.Button(btn_frame, text="Stop Monitoring", command=self.stop_monitoring, state=tk.DISABLED)
        self.stop_btn.grid(row=0, column=1, padx=10)
        
        self.report_btn = ttk.Button(btn_frame, text="Download Report", command=self.download_report)
        self.report_btn.grid(row=0, column=2, padx=10)
        
        # Subscribe to alerts
        alerts.subscribe(self.handle_alert)
        
    def start_monitoring(self):
        # Create directories if they don't exist
        os.makedirs("SensitiveData", exist_ok=True)
        os.makedirs("SimulatedUSB", exist_ok=True)
        
        threading.Thread(target=monitor.start_monitoring, args=("SensitiveData",), daemon=True).start()
        self.status_var.set("Status: Active (Monitoring 'SensitiveData')")
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.append_alert("System started monitoring.")
        
    def stop_monitoring(self):
        threading.Thread(target=monitor.stop_monitoring, daemon=True).start()
        self.status_var.set("Status: Inactive")
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.append_alert("System stopped monitoring.")
        
    def download_report(self):
        report_path = "desktop_security_report.txt"
        success = report.generate_report(report_path)
        if success:
            messagebox.showinfo("Report Generated", f"Audit report successfully decrypted and saved to:\n{os.path.abspath(report_path)}")
        else:
            messagebox.showerror("Error", "Failed to generate report.")
            
    def handle_alert(self, alert_json_str):
        # Must update GUI from main thread
        self.after(0, self._process_alert, alert_json_str)
        
    def _process_alert(self, alert_json_str):
        try:
            alert_data = json.loads(alert_json_str)
            title = alert_data.get("title", "")
            message = alert_data.get("message", "")
            severity = alert_data.get("severity", "info")
            
            prefix = "[INFO]"
            if severity == "critical":
                prefix = "[CRITICAL] ⚠️"
                # Optional: Show popup for critical alerts
                messagebox.showwarning("Security Alert", f"{title}\n{message}")
            elif severity == "warning":
                prefix = "[WARNING] ⚡"
                
            self.append_alert(f"{prefix} {title}: {message}")
        except Exception:
            pass
            
    def append_alert(self, text):
        self.alert_box.config(state=tk.NORMAL)
        self.alert_box.insert(tk.END, text + "\n")
        self.alert_box.see(tk.END)
        self.alert_box.config(state=tk.DISABLED)

if __name__ == "__main__":
    app = SecurityDesktopApp()
    app.mainloop()
