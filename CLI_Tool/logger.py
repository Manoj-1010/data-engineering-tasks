import datetime
import os

class DualLogger:
    """Handles logging output to both the CLI console and a timestamped file."""
    
    def __init__(self):
        # Create a log file with the startup timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_filename = f"datatool_run_{timestamp}.log"
        self.file = open(self.log_filename, "a", encoding="utf-8")
        self.log(f"Session started. Logging to {self.log_filename}\n")

    def log(self, message: str):
        """Prints to console and writes to the log file."""
        print(message)
        self.file.write(str(message) + "\n")
        self.file.flush() # Ensure it writes to disk immediately

    def close(self):
        """Closes the log file when the program exits."""
        self.log("\nSession ended.")
        self.file.close()
