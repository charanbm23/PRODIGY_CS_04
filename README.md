# Simple Keylogger

A basic keylogger implementation for educational purposes. This project demonstrates keyboard monitoring concepts while emphasizing ethical considerations and proper usage.

## ⚠️ Ethical Warning

This keylogger is intended for educational purposes only. Always:
- Obtain proper consent before monitoring keyboard activity
- Use only on systems you own or have explicit permission to monitor
- Follow applicable laws and regulations
- Respect privacy and data protection requirements

## Features

- Captures keystrokes with timestamps
- Tracks active window for each keystroke
- Organizes logs by date
- Handles clipboard changes
- Takes screenshots at configurable intervals
- Simple start/stop functionality (ESC key to stop or via GUI)
- Clear ethical warnings and consent requirements
- GUI interface for easy control
- Email logging functionality (optional)
- Stealth mode option
- Auto-start on boot capability
- Executable build support
- Log encryption (optional)
- Automatic log rotation and cleanup
- Debug output for troubleshooting

## Installation

1. Ensure Python 3.6+ is installed
2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### GUI Mode
1. Run the GUI interface:
```bash
python gui.py
```

2. Configure options:
   - Enable/disable auto-start
   - Set up email logging
   - Toggle clipboard tracking
   - Adjust screenshot interval
   - Enable/disable stealth mode
   - Start/stop logging

### Command Line Mode
1. Run the keylogger:
```bash
python keylogger.py
```

2. Press ENTER to start logging after reading the ethical warning
3. Press ESC to stop logging

## Log Files

- Logs are stored in the `logs` directory in your project folder
- Each day gets a new log file (format: `keylog_YYYY-MM-DD.txt`)
- Each entry includes timestamp, window title, and key pressed
- The log file is created as soon as the keylogger starts
- If log encryption is enabled, logs may require decryption
- Screenshots are stored in the `screenshots` directory

## Troubleshooting

- **No log file appears:**
  - Make sure you typed something after starting the keylogger
  - Check the terminal for `[DEBUG]` or `[ERROR]` messages
  - Ensure you have write permissions to the project directory
  - Try manually creating the `logs` directory
  - Make sure you are running the keylogger from the correct folder
- **Debug output:**
  - The keylogger prints debug information about log file creation and errors
  - Use this output to diagnose issues with file paths or permissions

## Building Executable

To create a standalone executable:
```bash
python build.py
```

The executable will be created in the `dist` directory.

## Project Structure

- `keylogger.py`: Core keylogger implementation
- `gui.py`: GUI interface
- `auto_setup.py`: Automatic setup script
- `build.py`: Executable builder
- `requirements.txt`: Project dependencies
- `logs/`: Directory containing log files
- `screenshots/`: Directory containing screenshots

## Email Configuration

To use email logging:
1. Enable email logging in the GUI
2. Enter your Gmail address and password
3. Make sure to use an App Password if 2FA is enabled

## Legal Disclaimer

This software is provided for educational purposes only. The user assumes all responsibility for its use and must ensure compliance with all applicable laws and regulations regarding privacy and data protection. 
