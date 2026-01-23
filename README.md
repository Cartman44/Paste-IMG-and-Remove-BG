# Paste-IMG-and-Remove-BG
A lightweight but powerful Python utility that monitors your clipboard for images, removes backgrounds automatically locally using AI, and allows you to paste the transparent result anywhere using Ctrl+Alt+V.
=======
Flawless Background Remover ✂️
A lightweight but powerful Windows utility that automatically removes backgrounds from images in your clipboard using AI locally. Copy an image, wait a second, and paste the transparent result anywhere.

<img src="assets/demo.gif" width="600" />

🚀 Features
Automatic Detection: Monitors your clipboard for new images.

AI-Powered: Uses the rembg library (U2-Net) for high-quality background removal.

Background Processing: Process images silently.

Non-Destructive: Restores your original copied image to the clipboard after pasting.

System Tray Integration: Runs quietly in the background with status updates.

Global Hotkey: Use Ctrl + Alt + V to paste the transparent PNG.

🛠️ How it Works

Copy: You copy an image (from a browser, folder, or screenshot).

Process: The app detects the image and processes it in the background using AI.

Paste: When the tray icon says "Ready," press Ctrl + Alt + V.

Restore: The app temporarily swaps the clipboard to the transparent PNG, triggers a "Paste" command, and immediately puts your original image back.

📦 Installation & Setup
1. Clone the Repository
git clone https://github.com/Cartman44/Paste-IMG-and-Remove-BG#
2. Install Dependencies
Ensure you have Python 3.9+ installed. Install the core requirements:
pip install -r requirements.txt
3. GPU Acceleration (Optional but Recommended)
By default, the AI processing runs on your CPU. If you have an NVIDIA GPU, you can make the removal process significantly faster (near-instant) by installing the ONNX Runtime with CUDA support, but might require additional configuration, since CUDA versions might be differ:
pip install onnxruntime-gpu

🖥️ Usage
Run the script with the .bat file.

First Run: The app will download the AI model (approx. 170MB). This happens only once.

The Workflow:

Copy any image (Ctrl + C).

Press Ctrl + Alt + V in your target app.

📋 Requirements
The project relies on the following libraries:

Pillow: Image manipulation.

rembg: AI-based background removal.

pynput: Global hotkey listening.

pystray: System tray icon and menu.

pywin32: Windows clipboard handling.

📜 License

:0
