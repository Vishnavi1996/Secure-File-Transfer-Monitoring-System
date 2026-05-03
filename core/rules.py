import json

# Define our authorization rules and configurations

SENSITIVE_DIRS = [
    "SensitiveData",  # Default test directory
]

SENSITIVE_EXTENSIONS = [
    ".txt", ".csv", ".pdf", ".docx", ".xlsx", ".key"
]

RESTRICTED_DESTINATIONS = [
    "SimulatedUSB",  # Simulating USB or external drive
]

def is_sensitive_file(file_path: str) -> bool:
    """Check if the file is in a sensitive directory or has a sensitive extension."""
    for s_dir in SENSITIVE_DIRS:
        if s_dir in file_path:
            return True
    
    for ext in SENSITIVE_EXTENSIONS:
        if file_path.lower().endswith(ext):
            return True
            
    return False

def is_unauthorized_transfer(src_path: str, dest_path: str) -> bool:
    """Check if a file is being moved to a restricted destination."""
    for dest in RESTRICTED_DESTINATIONS:
        if dest in dest_path:
            return True
    return False
