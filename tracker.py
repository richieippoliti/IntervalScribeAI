import threading
import time
from datetime import datetime, timedelta
from PIL import Image
import pytesseract
import mss
from summarizer import summarize_text, extract_bullets

class Tracker:
    def __init__(self, interval=1, show_timing=True, show_ocr=False, log_callback=None, minimize_callback=None):
        self.interval = interval
        self.show_timing = show_timing
        self.show_ocr = show_ocr
        self.log_callback = log_callback
        self.minimize_callback = minimize_callback
        self.is_running = False
        self.thread = None
        self.bullets = []

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self.run, daemon=True)
            self.thread.start()

    def stop(self):
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=1)

    def run(self):
        while self.is_running:
            start_time = time.time()
            if self.minimize_callback:
                self.minimize_callback()
            img_capture_start = time.time()
            img = self.capture_screen()
            img_capture_end = time.time()
            if self.show_timing:
                self.log(f"[Timing] Screen capture took {img_capture_end - img_capture_start:.2f} seconds.")

            ocr_start = time.time()
            text = self.extract_text(img)
            ocr_end = time.time()
            if self.show_timing:
                self.log(f"[Timing] OCR took {ocr_end - ocr_start:.2f} seconds.")
            if self.show_ocr:
                self.log("\n========== OCR TEXT START ==========")
                ocr_text_single_line = text.replace('\n', ' ').replace('\r', ' ').strip()
                self.log(ocr_text_single_line)
                self.log("=========== OCR TEXT END ===========\n")

            summarize_start = time.time()
            summary = summarize_text(text)
            summarize_end = time.time()
            if self.show_timing:
                self.log(f"[Timing] Summarization took {summarize_end - summarize_start:.2f} seconds.")

            self.bullets.extend(extract_bullets(summary))
            total_time = time.time() - start_time
            self.log(f"{datetime.now().strftime('%H:%M:%S')}: {summary}")
            if self.show_timing:
                self.log(f"[Timing] Total cycle time: {total_time:.2f} seconds.\n")
                next_run = datetime.now() + timedelta(minutes=self.interval)
                self.log(f"Next run at: {next_run.strftime('%I:%M:%S %p')}")
            for _ in range(int(self.interval * 60 * 10)):
                if not self.is_running:
                    break
                time.sleep(0.1)

    def capture_screen(self):
        with mss.mss() as sct:
            monitor = sct.monitors[0]
            sct_img = sct.grab(monitor)
            img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
        return img

    def extract_text(self, image):
        return pytesseract.image_to_string(image)

    def log(self, message):
        if self.log_callback:
            self.log_callback(message)

    def get_bullets(self):
        return self.bullets 