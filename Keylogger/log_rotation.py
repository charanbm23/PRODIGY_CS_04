
import os
import time
from datetime import datetime, timedelta
import shutil

def rotate_logs():
    log_dir = "logs"
    retention_days = 30
    
    # Get current time
    now = datetime.now()
    
    # Check each log file
    for filename in os.listdir(log_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(log_dir, filename)
            file_time = datetime.fromtimestamp(os.path.getctime(filepath))
            
            # Delete if older than retention period
            if now - file_time > timedelta(days=retention_days):
                os.remove(filepath)
                
    # Check screenshots
    screenshot_dir = "screenshots"
    for filename in os.listdir(screenshot_dir):
        if filename.endswith(".png"):
            filepath = os.path.join(screenshot_dir, filename)
            file_time = datetime.fromtimestamp(os.path.getctime(filepath))
            
            if now - file_time > timedelta(days=retention_days):
                os.remove(filepath)

if __name__ == "__main__":
    while True:
        rotate_logs()
        time.sleep(86400)  # Check once per day
