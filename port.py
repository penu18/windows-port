import sys, os, tkinter as tk
from tkinter import ttk
import subprocess, threading, ctypes, socket

# Check for admin privileges
def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except Exception:
            return False

# Restart as administrator if not already
if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable,
        ' '.join([f'"{arg}"' for arg in sys.argv]), None, 1
    )
    sys.exit()

# Validate port number
def is_valid_port(port):
    try:
        port = int(port)
        return 1 <= port <= 65535
    except:
        return False

# Check if a rule exists
def rule_exists(port, protocol):
    try:
        name = f"Port{protocol}-{port}"
        result = subprocess.run(
            f'netsh advfirewall firewall show rule name="{name}"',
            shell=True, capture_output=True, text=True
        )
        return name in result.stdout and 'No rules match' not in result.stdout
    except:
        return False

# Get all firewall port rules
def get_all_ports():
    try:
        result = subprocess.run(
            'netsh advfirewall firewall show rule name=all',
            shell=True, capture_output=True, text=True
        )
        lines = result.stdout.splitlines()
        rules = [line for line in lines if line.strip().startswith('Rule Name:') and ("PortTCP-" in line or "PortUDP-" in line)]
        ports = set()
        for rule in rules:
            if "PortTCP-" in rule:
                ports.add((rule.split('PortTCP-')[1], 'TCP'))
            if "PortUDP-" in rule:
                ports.add((rule.split('PortUDP-')[1], 'UDP'))
        return sorted(ports, key=lambda x: int(x[0]))
    except:
        return []

# Check if port is open
def is_port_open(port, protocol='TCP'):
    sock_type = socket.SOCK_STREAM if protocol == 'TCP' else socket.SOCK_DGRAM
    try:
        with socket.socket(socket.AF_INET, sock_type) as s:
            s.settimeout(1)
            return s.connect_ex(('127.0.0.1', int(port))) == 0
    except:
        return False

# Main Application
class PortManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Port Manager")
        self.geometry("500x600")
        self.resizable(False, False)
        self.bg_color = "#f4f7fb"
        self.fg_color = "#222"
        self.listbox_bg = "#ffffff"
        self.listbox_fg = "#000000"
        self.configure(bg=self.bg_color)

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.configure_styles()
        self.create_widgets()
        self.refresh_port_list()

    def configure_styles(self):
        self.style.configure('TButton', font=("Segoe UI", 12), padding=6, background="#2586e6", foreground="white")
        self.style.map('TButton', background=[('active', '#1d6fc2')])
        self.style.configure('TLabel', font=("Segoe UI", 11), background=self.bg_color, foreground=self.fg_color)
        self.style.configure('Header.TLabel', font=("Segoe UI", 18, "bold"), background=self.bg_color)

    def create_widgets(self):
        ttk.Label(self, text="Port Manager", style='Header.TLabel').pack(pady=(20, 4))
        self.message_var = tk.StringVar()
        self.message_label = ttk.Label(self, textvariable=self.message_var)
        self.message_label.pack()

        # Entry Fields
        entry_frame = tk.Frame(self, bg=self.bg_color)
        entry_frame.pack(pady=10)

        self.port_entry = ttk.Entry(entry_frame, font=("Segoe UI", 13), width=12, justify="center")
        self.port_entry.pack(side="left", padx=5)
        self.port_entry.bind('<Return>', lambda e: self.add_port())

        self.protocol_var = tk.StringVar(value="Both")
        ttk.OptionMenu(entry_frame, self.protocol_var, "Both", "TCP", "UDP", "Both").pack(side="left", padx=5)

        ttk.Button(entry_frame, text="Add", command=self.add_port).pack(side="left", padx=5)
        ttk.Button(entry_frame, text="Delete", command=self.delete_selected_port).pack(side="left", padx=5)

        # Extra buttons
        extra_frame = tk.Frame(self, bg=self.bg_color)
        extra_frame.pack()
        ttk.Button(extra_frame, text="Check", command=self.check_selected_port).pack(side="left", padx=5)

        ttk.Label(self, text="Ports").pack(pady=(12, 0))

        self.port_listbox = tk.Listbox(self, font=("Segoe UI", 12), height=15, bg=self.listbox_bg, fg=self.listbox_fg)
        self.port_listbox.pack(padx=20, pady=10, fill="both", expand=True)
        self.port_listbox.bind('<Delete>', lambda e: self.delete_selected_port())

    def show_message(self, msg, color="#e63c3c", duration=2500):
        self.message_label.configure(foreground=color)
        self.message_var.set(msg)
        self.after(duration, lambda: self.message_var.set(""))

    def add_port(self):
        port = self.port_entry.get().strip()
        proto_sel = self.protocol_var.get()
        if not is_valid_port(port):
            return self.show_message("Invalid port.")
        def task():
            protos = ["TCP", "UDP"] if proto_sel == "Both" else [proto_sel]
            if any(rule_exists(port, p) for p in protos):
                return self.show_message("Rule already exists.", "#e6a23c")
            try:
                for p in protos:
                    subprocess.run(
                        f'netsh advfirewall firewall add rule name=Port{p}-{port} '
                        f'protocol={p} dir=in action=allow localport={port}',
                        shell=True, check=True
                    )
                self.show_message("Port rule added!", "#27ae60")
                self.refresh_port_list()
                self.port_entry.delete(0, tk.END)
            except Exception as e:
                self.show_message(f"Error: {e}")
        threading.Thread(target=task).start()

    def delete_selected_port(self):
        sel = self.port_listbox.curselection()
        if not sel:
            return self.show_message("Please select a port.")
        value = self.port_listbox.get(sel[0])
        try:
            port, protos = value.split()
            protocols = protos.strip("()").split('/')
        except:
            return self.show_message("Invalid entry format.")
        def task():
            deleted = False
            for p in protocols:
                if rule_exists(port, p):
                    subprocess.run(
                        f'netsh advfirewall firewall delete rule name=Port{p}-{port} '
                        f'protocol={p} localport={port}', shell=True)
                    deleted = True
            if deleted:
                self.show_message("Port rule deleted.", "#27ae60")
                self.refresh_port_list()
            else:
                self.show_message("No matching rule found.", "#e6a23c")
        threading.Thread(target=task).start()

    def refresh_port_list(self):
        def task():
            ports = get_all_ports()
            self.port_listbox.delete(0, tk.END)
            port_dict = {}
            for port, proto in ports:
                port_dict.setdefault(port, []).append(proto)
            for port, protos in sorted(port_dict.items(), key=lambda x: int(x[0])):
                self.port_listbox.insert(tk.END, f"{port} ({'/'.join(sorted(protos))})")
        threading.Thread(target=task).start()

    def check_selected_port(self):
        sel = self.port_listbox.curselection()
        if not sel:
            return self.show_message("Please select a port.")
        value = self.port_listbox.get(sel[0])
        try:
            port, protos = value.split()
            protocols = protos.strip("()").split('/')
        except:
            return self.show_message("Invalid entry format.")
        def task():
            results = []
            for proto in protocols:
                is_open = is_port_open(port, proto)
                results.append(f"{proto}: {'Open' if is_open else 'Closed'}")
            self.show_message(f"{port} - {' | '.join(results)}", "#1abc9c")
        threading.Thread(target=task).start()

if __name__ == "__main__":
    PortManagerApp().mainloop()