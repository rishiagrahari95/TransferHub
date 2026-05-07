# 🚀 TransferHub

A high-speed, secure local network file transfer application built with Python, Flask, and CustomTkinter. 

**TransferHub** allows you to seamlessly send massive raw media files (like heavy videos or raw photos) directly from your mobile device to your PC's Desktop over your local WiFi network. Bypassing the cloud entirely means you get maximum router speeds with zero data limits.

---

## 🎉 **NEW: Standalone Windows App Released!**
You no longer need to install Python or use the terminal to run TransferHub. 
👉 **[Download the latest TransferHub.exe here](https://github.com/rishiagrahari95/TransferHub/releases)**

---

## ✨ Key Features
* **Zero Cloud Dependency:** 100% local area network (LAN) transfers for maximum speed and privacy.
* **Modern Desktop GUI:** Beautiful dark-mode interface built with CustomTkinter.
* **Instant Device Pairing:** Automatically generates a UI QR code to scan with your phone.
* **Custom Security & Routing:** Dynamic PIN and Port configuration directly from the app.
* **Mobile-First Web UI:** Responsive browser interface with Drag-and-Drop support.
* **Real-time Tracking:** Asynchronous upload progress bar powered by Vanilla JS.
* **Smart File Handling:** Routes directly to a `WiFi_Uploads` folder on your Desktop and auto-renames duplicate files to prevent overwriting.

## 📸 Screenshots
<img width="1920" height="1080" alt="Screenshot (98)" src="https://github.com/user-attachments/assets/4e44e889-a12c-4528-896a-1f6d06ab5ff5" />
<img width="1920" height="1080" alt="Screenshot (97)" src="https://github.com/user-attachments/assets/a31576bf-87cb-41f5-9fbb-46b2cb51b9b3" />
<img width="216" height="481.6" alt="Screenshot_20260506_020012" src="https://github.com/user-attachments/assets/c5be26df-5f20-4425-b3eb-e04a14e43bc3" />
---

## 📥 Installation & Setup

### Option 1: For Regular Users (Recommended)
1. Go to the [Releases Page](https://github.com/rishiagrahari95/TransferHub/releases).
2. Download the latest `TransferHub.exe` file.
3. Double-click the `.exe` to run the app. (No installation or Python required!)

### Option 2: For Developers (Build from Source)
If you want to view the code, modify the app, or build it yourself:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rishiagrahari95/TransferHub.git
   cd TransferHub
   ```

2. **Create a Virtual Environment & Install Dependencies:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run the App:**
   ```bash
   python desktop_gui.pyw
   ```

4. **Build the `.exe` yourself (using PyInstaller):**
   ```bash
   pyinstaller --noconsole --onefile --icon="app_icon.ico" --add-data "app_icon.ico;." --add-data "templates;templates" --add-data "static;static" desktop_gui.pyw
   ```

---

## 📱 How to Use
1. Open **TransferHub** on your PC.
2. (Optional) Change the default Port (`5000`) or Access PIN (`2026`) in the settings.
3. Click **Start Server**.
4. Ensure your mobile device is connected to the **same WiFi network** as your PC.
5. Open your phone's camera and **scan the QR code** displayed on your PC screen.
6. Enter the Access PIN in your mobile browser.
7. Select or drag-and-drop your files. They will instantly appear in the `WiFi_Uploads` folder on your PC's Desktop.

## 🛠️ Tech Stack
* **Backend:** Python 3, Flask, Werkzeug
* **Desktop UI:** CustomTkinter
* **Frontend:** HTML5, CSS3, Vanilla JavaScript
* **Utilities:** `qrcode` (Image generation), `os` & `socket` (System pathing and IP detection), `PyInstaller` (Packaging)

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/rishiagrahari95/TransferHub/issues).

## 📄 License
This project is licensed under the MIT License.
