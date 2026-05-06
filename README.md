# 🚀 TransferHub

A high-speed, secure local network file transfer tool built with Python and Flask. 

Bypass the cloud entirely. **TransferHub** allows you to seamlessly send massive media files directly from your mobile device to your PC's Desktop over your local WiFi network. 

## ✨ Features
* **Zero Cloud Dependency:** 100% local area network (LAN) transfers for maximum speed.
* **Instant Device Pairing:** Automatically generates a terminal QR code to scan with your phone.
* **Secure Access:** Simple PIN-based authentication to prevent unauthorized network uploads.
* **Modern Web UI:** Responsive, mobile-first design with Drag-and-Drop support.
* **Real-time Tracking:** Asynchronous upload progress bar powered by Vanilla JS (`XMLHttpRequest`).
* **Smart File Handling:** Auto-detects PC IP, routes directly to the Desktop, and auto-renames duplicate files to prevent overwriting.

## 🛠️ Tech Stack
* **Backend:** Python 3, Flask, Werkzeug
* **Frontend:** HTML5, CSS3, Vanilla JavaScript
* **Utilities:** `qrcode` (Terminal rendering), `os` & `socket` (System pathing and IP detection)

## 📸 Screenshots
<img width="1920" height="1080" alt="Screenshot (92)" src="https://github.com/user-attachments/assets/c9b0078e-cbe7-4518-b601-960360913c2d" />
<img width="324" height="722.4" alt="Screenshot_20260506_020012" src="https://github.com/user-attachments/assets/c5be26df-5f20-4425-b3eb-e04a14e43bc3" />


## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rishiagrahari95/TransferHub.git
   cd TransferHub
   ```

2. **Create and Activate a Virtual Environment:**
   It is recommended to use a virtual environment to keep dependencies clean. 

   **For Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
   **For macOS/Linux:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   
4. **Install Required Libraries:**
   Once the virtual environment is activated, install the necessary Python packages using pip:
   ```bash
   pip install -r requirements.txt
   ```

5. **Start the TransferHub Server:**
   Run the main application file. The server will start and a QR code will be generated in your terminal.
   ```bash
   python app.py
   ```

## 📱 How to Use
1. Start the server on your PC via the terminal (Step 4 above).
2. Ensure your mobile device is connected to the **same WiFi network**.
3. Scan the QR code that appears in your PC's terminal using your phone's camera.
4. Enter the default PIN (`2026`).
5. Select or drag-and-drop your files. They will instantly appear securely in a `WiFi_Uploads` folder on your PC's Desktop.

## 🔒 Configuration
You can easily modify the default settings by editing the variables at the top of `app.py`:
* `ACCESS_PIN`: Change the default '2026' to your preferred security code.
* `DESKTOP_PATH`: Modify the target save destination.
* `PORT`: Change the default `5000` port if it is already in use.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! 

## 📄 License
This project is licensed under the MIT License.
