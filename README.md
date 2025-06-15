# windows-port

A simple Python GUI application for managing Windows Firewall ports (open/close for TCP, UDP, or both) using the `netsh` command.

## Features

- Add new firewall rules for TCP, UDP, or both protocols
- Delete existing rules
- Check and list open firewall ports
- Simple graphical interface built with Tkinter

## Screenshots

### Application Interface

![Port Manager](https://github.com/penu18/windows-port/blob/main/screenshots/port_o9VfwW1D9F.png)

---

### User Account Control (UAC)

When launching the executable (`port.exe`), Windows will prompt for administrator privileges. This is required to allow firewall modifications.

![UAC Prompt](https://github.com/penu18/windows-port/blob/main/screenshots/consent_K0nMxS7OIq.png)

This is a **normal and expected behavior**. Since the app modifies Windows Firewall rules, it must run with elevated permissions.

---

### Windows Defender SmartScreen

Because this app is not signed with a verified digital certificate, Windows SmartScreen may display a warning like the following:

![SmartScreen](https://github.com/penu18/windows-port/blob/main/screenshots/db6abe92-14f8-4040-a320-cb4e3be8e656.png)

Click `More info`, then `Run anyway` to proceed:

![SmartScreen Run](https://github.com/penu18/windows-port/blob/main/screenshots/65b2ae00-a7fc-46ae-a7c6-4d294d224aa6.png)

This message appears because the app is from an **unknown publisher**, which is expected for unsigned personal projects.

---

## Requirements

- Python 3.x (for development version)
- Admin privileges (UAC prompt)
- Windows 10/11

## Development

To run or build the app yourself:

```bash
git clone https://github.com/penu18/windows-port.git
cd windows-port
python main.py
