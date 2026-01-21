import time
import threading
import sys
import os
import win32clipboard
import win32con
from io import BytesIO

from PIL import Image, ImageGrab
from rembg import remove
from pynput import keyboard
import pystray

class FlawlessBackgroundRemover:
    def __init__(self):
        self.last_clipboard_hash = None
        self.memory_image_bytes = None
        self.is_ready_to_paste = False
        self.running = True
        self.ignore_next_change = False 
        self.lock = threading.Lock()
        try:
            self.CF_PNG = win32clipboard.RegisterClipboardFormat("PNG")
        except Exception as e:
            print(f"Format Error: {e}")
            self.CF_PNG = 0

    def get_clipboard_hash(self):
        try:
            img = ImageGrab.grabclipboard()
            if isinstance(img, Image.Image):
                return hash(img.tobytes())
        except:
            pass
        return None

    def set_clipboard_transparent(self, png_data):
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            if self.CF_PNG:
                win32clipboard.SetClipboardData(self.CF_PNG, png_data)
            win32clipboard.CloseClipboard()
        except Exception as e:
            print(f"Error setting transparent clipboard: {e}")

    def restore_original_to_clipboard(self, original_img):
        if original_img is None:
            return
        
        try:
            with BytesIO() as bio:
                original_img.convert("RGB").save(bio, "BMP")
                data = bio.getvalue()[14:] 
            
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32con.CF_DIB, data)
            win32clipboard.CloseClipboard()
        except Exception as e:
            print(f"Error getting original img: {e}")

    def process_background(self, img):
        print(">> Processing")
        try:
            output = remove(img)
            
            with BytesIO() as bio:
                output.save(bio, format="PNG")
                png_bytes = bio.getvalue()
            
            with self.lock:
                self.memory_image_bytes = png_bytes
                self.is_ready_to_paste = True
                
            print(f"Done, image is in memory\nPress Ctrl+Alt+V anytime .")
            self.update_tray("Ready (Ctrl+Alt+V)")
            
        except Exception as e:
            print(f"Error while processing: {e}")

    def monitor_loop(self):
        print("Monitoring, copy an img (Ctrl+C).")
        
        while self.running:
            time.sleep(0.5) 
            
            if self.ignore_next_change:
                continue

            current_hash = self.get_clipboard_hash()
            
            if current_hash is None or current_hash == self.last_clipboard_hash:
                continue
                
            print("New img copied, processing...")
            self.last_clipboard_hash = current_hash
            self.is_ready_to_paste = False 
            self.update_tray("Processing...")
            
            img = ImageGrab.grabclipboard()
            if img:
                threading.Thread(target=self.process_background, args=(img,), daemon=True).start()

    def on_hotkey_paste(self):
        if not self.is_ready_to_paste or not self.memory_image_bytes:
            print("No img stored")
            return

        print("Pasting transparent img")
        
        original_img = ImageGrab.grabclipboard()
        
        self.ignore_next_change = True
        
        with self.lock:
            self.set_clipboard_transparent(self.memory_image_bytes)
        
        k = keyboard.Controller()
        time.sleep(0.05) 
        
        k.release(keyboard.Key.alt)
        
        k.press(keyboard.Key.ctrl)
        k.press('v')
        k.release('v')
        k.release(keyboard.Key.ctrl)
        
        time.sleep(0.2)
        
        if original_img:
            self.restore_original_to_clipboard(original_img)
        else:
            try:
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.CloseClipboard()
            except: pass

        threading.Timer(0.5, self.reset_ignore_flag).start()
        
    def reset_ignore_flag(self):
        self.ignore_next_change = False

    def create_tray(self):
        icon_path = "icon.png"
        if os.path.exists(icon_path):
            try:
                icon = Image.open(icon_path)
                icon = icon.resize((64, 64)) 
            except Exception as e:
                print(f"Nu am putut încărca icon.png: {e}")
                icon = Image.new('RGB', (64, 64), color='cyan')
        else:
            print("⚠️ icon.png nu a fost găsit. Folosesc iconița default.")
            icon = Image.new('RGB', (64, 64), color='cyan')

        menu = pystray.Menu(pystray.MenuItem("Exit", self.exit_app))
        self.tray = pystray.Icon("BGRemover", icon, "BG Remover", menu)
        
    def update_tray(self, text):
        if self.tray: self.tray.title = text

    def exit_app(self, icon=None, item=None):
        self.running = False
        self.tray.stop()
        sys.exit()

    def run(self):
        self.create_tray()
        
        hk = keyboard.GlobalHotKeys({'<ctrl>+<alt>+v': self.on_hotkey_paste})
        hk.start()
        
        threading.Thread(target=self.monitor_loop, daemon=True).start()
        
        print("Ready")
        self.tray.run()

if __name__ == "__main__":
    app = FlawlessBackgroundRemover()
    app.run()