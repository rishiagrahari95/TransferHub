import os
import socket
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import qrcode

# --- congfig ---
UPLOAD_FOLDER = 'uploads'
LOG_FOLDER = 'logs'
ACCESS_PIN = "2026" 
MAX_CONTENT_LENGTH = 5 * 1024 * 1024 * 1024 

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.urandom(24)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(LOG_FOLDER, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_FOLDER, 'transfer.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_local_ip():
    """Detect local LAN IP to bind the server."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def get_unique_filename(filename):
    """Prevent overwriting by auto-renaming duplicates."""
    base, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], new_filename)):
        new_filename = f"{base}_{counter}{ext}"
        counter += 1
    return new_filename

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    # --- auth ---
    pin = request.form.get('pin')
    if pin != ACCESS_PIN:
        logging.warning("Failed upload attempt: Invalid PIN.")
        return jsonify({'error': 'Invalid PIN'}), 401

    if 'files' not in request.files:
        return jsonify({'error': 'No files provided'}), 400

    files = request.files.getlist('files')
    saved_files = []

    for file in files:
        if file.filename == '':
            continue
            
        original_name = secure_filename(file.filename)
        safe_name = get_unique_filename(original_name)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_name)
        
        try:
            file.save(file_path)
            file_size = os.path.getsize(file_path)
            saved_files.append({
                'name': safe_name,
                'size': round(file_size / (1024 * 1024), 2)
            })
            logging.info(f"Successfully saved: {safe_name} ({file_size} bytes)")
        except Exception as e:
            logging.error(f"Error saving {safe_name}: {str(e)}")
            return jsonify({'error': f'Failed to save {safe_name}'}), 500

    return jsonify({'message': 'Upload successful', 'files': saved_files}), 200

if __name__ == '__main__':
    local_ip = get_local_ip()
    port = 5000
    url = f"http://{local_ip}:{port}"
    
    print("="*50)
    print(f"🚀 SERVER RUNNING AT: {url}")
    print(f"🔒 ACCESS PIN: {ACCESS_PIN}")
    print("="*50)
    print("Scan this QR code with your mobile device:")
    
    # --- qr --- 
    qr = qrcode.QRCode()
    qr.add_data(url)
    qr.print_ascii(invert=True)
    
    print("="*50)
    print("Press CTRL+C to quit")
    
    app.run(host='0.0.0.0', port=port, debug=False)
