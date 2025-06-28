import multiprocessing
import webbrowser
import tkinter as tk
import time
import sys
import os
import subprocess

def run_flask():
    # Usar subprocess para mejor control
    subprocess.run([sys.executable, "app.py"])

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Bingo Server Control")
        self.proc = None

        self.start_btn = tk.Button(root, text="Iniciar servidor", command=self.start_server, width=20, height=2, bg="#aaffaa")
        self.start_btn.pack(pady=10)

        self.stop_btn = tk.Button(root, text="Parar servidor", command=self.stop_server, width=20, height=2, bg="#ffaaaa", state=tk.DISABLED)
        self.stop_btn.pack(pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def start_server(self):
        if self.proc is None or not self.proc.is_alive():
            self.proc = multiprocessing.Process(target=run_flask)
            self.proc.start()
            time.sleep(2)  # Espera a que el servidor arranque
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                s.connect(('8.8.8.8', 80))
                ip = s.getsockname()[0]
            except Exception:
                ip = '127.0.0.1'
            finally:
                s.close()
            url = f"http://{ip}:5000"
            webbrowser.open(url)
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)

    def stop_server(self):
        if self.proc and self.proc.is_alive():
            self.proc.terminate()
            self.proc.join(timeout=3)
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)

    def on_close(self):
        self.stop_server()
        self.root.destroy()

if __name__ == '__main__':
    multiprocessing.freeze_support()  # Necesario para PyInstaller en Windows
    root = tk.Tk()
    app = App(root)
    root.mainloop()