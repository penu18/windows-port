# windows-port

A simple Python GUI application for managing Windows Firewall ports (open/close for TCP, UDP, or both) using the `netsh` command.

## Features

- Add new firewall rules for TCP, UDP, or both protocols
- Delete existing rules
- Check and list open firewall ports
- Simple graphical interface built with Tkinter

---

## Security Warnings (First Run)

Since this application modifies system firewall settings, **Windows will prompt security warnings**. Here's how to safely proceed:

### 1. Windows Defender SmartScreen

If you downloaded the `.exe` version (e.g., `port.exe`) and run it for the first time, SmartScreen may block it.

#### Initial warning:

![SmartScreen Initial](https://raw.githubusercontent.com/penu18/windows-port/refs/heads/main/screenshots/smartscreen_warning_initial.png)

#### Expand and proceed:

Click on **"More info"**, then **"Run anyway"**.

![SmartScreen Expanded](https://raw.githubusercontent.com/penu18/windows-port/refs/heads/main/screenshots/smartscreen_warning_expanded.png)

> 🛡 This is a standard behavior for unsigned applications. You can safely proceed if you trust the source (this GitHub repository).

---

### 2. User Account Control (UAC)

After bypassing SmartScreen, Windows will prompt with UAC to confirm admin access:

![UAC Prompt](https://raw.githubusercontent.com/penu18/windows-port/refs/heads/main/screenshots/uac_prompt_unknown_publisher.png)

> 🔐 This is **required** for modifying firewall rules. If you deny, the application won't function properly.

---

## Application Interface

Once allowed, the Port Manager application launches:

![Port Manager UI](https://raw.githubusercontent.com/penu18/windows-port/refs/heads/main/screenshots/port_manager_main_ui.png)

You can:
- Enter a port number
- Choose TCP, UDP, or Both
- Add/Delete rules
- Check currently open ports

---

## Requirements

- Windows 10 or 11
- Python 3.x (for development use)
- Administrator privileges (required to modify firewall rules)

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Development (Run from source)

To run or modify the project:

```bash
git clone https://github.com/penu18/windows-port.git
cd windows-port
python main.py
