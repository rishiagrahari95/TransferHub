import os
import sys
import ctypes
import socket
import threading
import qrcode
from PIL import Image
import customtkinter as ctk
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from werkzeug.serving import make_server

try:
    my_app_id = 'transferhub.local.server.1'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)
except Exception:
    pass

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

DESKTOP_PATH = os.path.join(os.path.expanduser('~'), 'Desktop', 'WiFi_Uploads')
os.makedirs(DESKTOP_PATH, exist_ok=True)

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.urandom(24)
app.config['ACCESS_PIN'] = "2026"

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def get_safe_filename(filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    while os.path.exists(os.path.join(DESKTOP_PATH, new_filename)):
        new_filename = f"{base}_{counter}{ext}"
        counter += 1
    return new_filename

@app.route('/')
def index():
    from flask import render_template
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if request.form.get('pin') != app.config['ACCESS_PIN']:
        return jsonify({'error': 'Invalid PIN'}), 401
        
    if 'files' not in request.files:
        return jsonify({'error': 'No files detected'}), 400

    files = request.files.getlist('files')
    saved_files = []
    for file in files:
        if file.filename == '': continue
        safe_name = get_safe_filename(secure_filename(file.filename))
        save_path = os.path.join(DESKTOP_PATH, safe_name)
        try:
            file.save(save_path)
            file_size_mb = round(os.path.getsize(save_path) / (1024 * 1024), 2)
            saved_files.append({'name': safe_name, 'size': file_size_mb})
        except Exception as e:
            return jsonify({'error': f'Failed to save {safe_name}'}), 500
    return jsonify({'message': 'Success', 'files': saved_files}), 200

class ServerThread(threading.Thread):
    def __init__(self, app, host, port):
        threading.Thread.__init__(self)
        self.server = make_server(host, port, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()

class TransferHubApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("TransferHub - Local Server")
        self.geometry("600x450")
        self.resizable(False, False)
        
        try:
            self.iconbitmap(resource_path("app_icon.ico"))
        except Exception:
            pass

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.server_thread = None
        self.is_running = False
        self.local_ip = get_local_ip()

        self.build_ui()

    def build_ui(self):
        self.left_frame = ctk.CTkFrame(self, width=280, corner_radius=10)
        self.left_frame.pack(side="left", fill="y", padx=20, pady=20)

        self.title_label = ctk.CTkLabel(self.left_frame, text="🚀 TransferHub", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=(20, 5))

        self.subtitle_label = ctk.CTkLabel(self.left_frame, text="WiFi File Transfer", text_color="gray")
        self.subtitle_label = ctk.CTkLabel(self.left_frame, text="by Rishi Agrahari", text_color="gray")
        self.subtitle_label.pack(pady=(0, 20))

        self.status_label = ctk.CTkLabel(self.left_frame, text="🔴 Offline", text_color="#EF4444", font=ctk.CTkFont(size=16, weight="bold"))
        self.status_label.pack(pady=10)

        self.settings_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        self.settings_frame.pack(pady=10, fill="x", padx=20)

        ctk.CTkLabel(self.settings_frame, text=f"IP: {self.local_ip}", font=ctk.CTkFont(size=14)).pack(anchor="w", pady=(0, 10))
        
        self.port_label = ctk.CTkLabel(self.settings_frame, text="Port:", font=ctk.CTkFont(size=14))
        self.port_label.pack(anchor="w")
        self.port_input = ctk.CTkEntry(self.settings_frame, width=150, height=28)
        self.port_input.insert(0, "5000") # Default Port
        self.port_input.pack(anchor="w", pady=(0, 10))

        self.pin_label = ctk.CTkLabel(self.settings_frame, text="Access PIN:", font=ctk.CTkFont(size=14))
        self.pin_label.pack(anchor="w")
        self.pin_input = ctk.CTkEntry(self.settings_frame, width=150, height=28)
        self.pin_input.insert(0, "2026") # Default PIN
        self.pin_input.pack(anchor="w")

        self.toggle_btn = ctk.CTkButton(self.left_frame, text="Start Server", command=self.toggle_server, fg_color="#2563EB", hover_color="#1D4ED8")
        self.toggle_btn.pack(pady=20)

        self.right_frame = ctk.CTkFrame(self, corner_radius=10)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=(0, 20), pady=20)

        self.qr_placeholder = ctk.CTkLabel(self.right_frame, text="Start server to\nview QR Code", text_color="gray", font=ctk.CTkFont(size=16))
        self.qr_placeholder.pack(expand=True)

    def generate_qr(self, server_url):
        qr = qrcode.QRCode(box_size=10, border=2)
        qr.add_data(server_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white").get_image()
        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(250, 250))
        return ctk_img

    def toggle_server(self):
        if not self.is_running:
            try:
                current_port = int(self.port_input.get().strip())
            except ValueError:
                current_port = 5000
                self.port_input.delete(0, 'end')
                self.port_input.insert(0, "5000")

            current_pin = self.pin_input.get().strip()
            if not current_pin:
                current_pin = "2026"
                self.pin_input.insert(0, "2026")

            app.config['ACCESS_PIN'] = current_pin
            server_url = f"http://{self.local_ip}:{current_port}"

            self.server_thread = ServerThread(app, '0.0.0.0', current_port)
            self.server_thread.start()
            
            self.port_input.configure(state="disabled", fg_color="#374151")
            self.pin_input.configure(state="disabled", fg_color="#374151")
            
            self.status_label.configure(text="🟢 Online", text_color="#10B981")
            self.toggle_btn.configure(text="Stop Server", fg_color="#EF4444", hover_color="#DC2626")
            
            qr_image = self.generate_qr(server_url)
            self.qr_placeholder.configure(text="", image=qr_image)
            
            self.is_running = True
        else:
            self.server_thread.shutdown()
            self.server_thread.join()
            
            self.port_input.configure(state="normal", fg_color=["#F9F9FA", "#343638"])
            self.pin_input.configure(state="normal", fg_color=["#F9F9FA", "#343638"])
            
            self.status_label.configure(text="🔴 Offline", text_color="#EF4444")
            self.toggle_btn.configure(text="Start Server", fg_color="#2563EB", hover_color="#1D4ED8")
            
            self.qr_placeholder.configure(text="Start server to\nview QR Code", image="")
            
            self.is_running = False

    def on_closing(self):
        if self.is_running:
            self.server_thread.shutdown()
        self.destroy()

if __name__ == "__main__":
    gui = TransferHubApp()
    gui.protocol("WM_DELETE_WINDOW", gui.on_closing)
    gui.mainloop()