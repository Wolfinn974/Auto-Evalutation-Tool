import os
from datetime import datetime

LOG_DIR = "logs"
SYSTEM_LOG = os.path.join(LOG_DIR, "system.log")

class Logger:
    """
    Simple logger with timestamp + automatic log directory creation.
    Suitable for your engine, silent for students.
    """

    def __init__(self):
        if not os.path.isdir(LOG_DIR):
            os.mkdir(LOG_DIR)

        # Create system.log if missing
        if not os.path.exists(SYSTEM_LOG):
            with open(SYSTEM_LOG, "w", encoding="utf-8") as f:
                f.write("=== SYSTEM LOG ===\n")

    def log(self, message):
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        line = f"{timestamp} {message}"

        # Append to log file
        with open(SYSTEM_LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")

        # Optional: also print to dev console
        # (CAN BE DISABLED IN V2 VIA CONFIG)
        print(f"[LOG] {line}")


# ---------------------------------------------------------
# GLOBAL LOGGER INSTANCE
# ---------------------------------------------------------

logger = Logger()

def log(message):
    """
    Global helper function to log messages.
    Used everywhere in the engine.
    """
    logger.log(message)


# ---------------------------------------------------------
# TIME HELPERS (OPTIONAL FOR V2)
# ---------------------------------------------------------

def format_seconds(sec):
    """
    Converts a number of seconds into m:ss format.
    Example: 125 -> '2m 05s'
    """
    m = sec // 60
    s = sec % 60
    return f"{m}m {s:02d}s"


# ---------------------------------------------------------
# SAFE PRINT (FOR STUDENTS)
# ---------------------------------------------------------

def safe_print(*args, **kwargs):
    """
    Wrapper in case you want to filter output later.
    For example: avoid printing logs to students,
    or color student-facing messages.
    """
    print(*args, **kwargs)