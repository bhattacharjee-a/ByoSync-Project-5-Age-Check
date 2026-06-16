# project_log.py
import logging
from constants import LOG_FILE, DEBUG_MODE

level = logging.DEBUG if DEBUG_MODE else logging.INFO

logger = logging.getLogger()                                        
logger.setLevel(level)                                              
file_handler = logging.FileHandler(LOG_FILE, mode="a")            
file_handler.setLevel(level)

# ---------- Console Handler ----------
console_handler = logging.StreamHandler()
console_handler.setLevel(level)

# ---------- Formatter ----------
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"                    # "TIME | LEVEL | TEXT"
)

file_handler.setFormatter(formatter)                               
console_handler.setFormatter(formatter)                             

# ---------- Attach Handlers ----------

if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

#print("✅ Logging configured")   # DEBUG CONFIRMATION
