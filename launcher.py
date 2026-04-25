import webbrowser
import tkinter as tk
import time
import sys
import os
import subprocess
import socket
from pathlib import Path


def is_port_free(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return sock.connect_ex(("127.0.0.1", port)) != 0


def resolve_server_port():
    env_port = os.getenv("BINGO_PORT")
    if env_port and env_port.isdigit():
        forced_port = int(env_port)
        if 1 <= forced_port <= 65535:
            return forced_port

    candidate_ports = []

    candidate_ports.extend([8080, 5000, 8000, 8888])

    for port in candidate_ports:
        if 1 <= port <= 65535 and is_port_free(port):
            return port

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as temp:
        temp.bind(("", 0))
        return temp.getsockname()[1]


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


def run_embedded_server():
    port = None
    if len(sys.argv) >= 3 and sys.argv[2].isdigit():
        port = int(sys.argv[2])
    from app import start_bingo_server
    start_bingo_server(port)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Bingo - Panel de Inicio")
        self.root.geometry("460x300")
        self.root.resizable(False, False)
        self.proc = None
        self.server_port = resolve_server_port()

        wrapper = tk.Frame(root, bg="#f7f9fc", padx=18, pady=18)
        wrapper.pack(fill=tk.BOTH, expand=True)

        title = tk.Label(
            wrapper,
            text="Bingo para Escritorio",
            font=("Segoe UI", 16, "bold"),
            fg="#133b5c",
            bg="#f7f9fc"
        )
        title.pack(pady=(4, 8))

        self.info_label = tk.Label(
            wrapper,
            text=f"Puerto sugerido: {self.server_port}",
            font=("Segoe UI", 10),
            fg="#355c7d",
            bg="#f7f9fc"
        )
        self.info_label.pack(pady=(0, 12))

        self.start_btn = tk.Button(
            wrapper,
            text="Iniciar servidor",
            command=self.start_server,
            width=22,
            height=2,
            bg="#1f9d55",
            fg="white",
            activebackground="#14773f",
            relief=tk.FLAT
        )
        self.start_btn.pack(pady=8)

        self.stop_btn = tk.Button(
            wrapper,
            text="Parar servidor",
            command=self.stop_server,
            width=22,
            height=2,
            bg="#d64545",
            fg="white",
            activebackground="#a63434",
            relief=tk.FLAT,
            state=tk.DISABLED
        )
        self.stop_btn.pack(pady=8)

        self.status_label = tk.Label(
            wrapper,
            text="Estado: detenido",
            font=("Segoe UI", 10, "bold"),
            fg="#7f1d1d",
            bg="#f7f9fc"
        )
        self.status_label.pack(pady=(10, 0))

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def start_server(self):
        if self.proc is None or self.proc.poll() is not None:
            if not is_port_free(self.server_port):
                self.server_port = resolve_server_port()

            env = os.environ.copy()
            env["BINGO_PORT"] = str(self.server_port)

            if getattr(sys, "frozen", False):
                cmd = [sys.executable, "--serve", str(self.server_port)]
                workdir = os.path.dirname(sys.executable)
            else:
                cmd = [sys.executable, "app.py"]
                workdir = str(Path(__file__).resolve().parent)

            creation_flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
            self.proc = subprocess.Popen(cmd, env=env, cwd=workdir, creationflags=creation_flags)
            time.sleep(2)
            ip = get_local_ip()
            url = f"http://{ip}:{self.server_port}"
            webbrowser.open(url)
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.status_label.config(text=f"Estado: activo en {ip}:{self.server_port}", fg="#166534")
            self.info_label.config(text="Se abrio el navegador automaticamente.")

    def stop_server(self):
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.proc.kill()
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.status_label.config(text="Estado: detenido", fg="#7f1d1d")
            self.info_label.config(text=f"Puerto sugerido: {self.server_port}")

    def on_close(self):
        self.stop_server()
        self.root.destroy()

if __name__ == '__main__':
    if len(sys.argv) >= 2 and sys.argv[1] == "--serve":
        run_embedded_server()
        sys.exit(0)

    root = tk.Tk()
    app = App(root)
    root.mainloop()