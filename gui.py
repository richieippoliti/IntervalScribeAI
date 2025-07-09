import customtkinter as ctk
from tkinter import messagebox
from tracker import Tracker
from summarizer import summarize_day
import time
import threading

BG_COLOR = "#f7fafd"
CARD_COLOR = "#ffffff"
ACCENT_COLOR = "#5fa8d3"
BUTTON_COLOR = "#e3eaf2"
FG_COLOR = "#222831"
START_COLOR = "#5fa8d3"
STOP_COLOR = "#393e46"
FRAME_BG = "#e3eaf2"
FONT = ("Segoe UI", 12)
TITLE_FONT = ("Segoe UI", 20, "bold")
BUTTON_FONT = ("Segoe UI", 12, "bold")
LOG_FONT = ("Fira Mono", 13)

class IntervalScribeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("IntervalScribe AI")
        self.root.minsize(900, 650)
        self.tracker = None
        self.tracker_thread = None
        self.is_running = False
        self.start_time = None
        self.timer_updater = None

        # Top bar with title only
        topbar = ctk.CTkFrame(root, fg_color=BG_COLOR, corner_radius=0)
        topbar.pack(fill="x", padx=0, pady=0)
        ctk.CTkLabel(topbar, text="🕒 IntervalScribe AI", font=TITLE_FONT, text_color=ACCENT_COLOR).pack(side="left", padx=24, pady=18)

        # Main content area
        card = ctk.CTkFrame(root, fg_color=CARD_COLOR, corner_radius=18)
        card.pack(fill="both", expand=True, padx=36, pady=36)
        self.timer_var = ctk.StringVar(value="Elapsed: 00:00:00")
        self.timer_label = ctk.CTkLabel(card, textvariable=self.timer_var, font=("Segoe UI", 14), text_color=ACCENT_COLOR)
        self.timer_label.pack(pady=(0, 10))

        # Controls card
        controls_frame = ctk.CTkFrame(card, fg_color=FRAME_BG, corner_radius=14)
        controls_frame.pack(fill="x", padx=24, pady=12)
        controls_label = ctk.CTkLabel(controls_frame, text="Controls", font=FONT, text_color=ACCENT_COLOR)
        controls_label.grid(row=0, column=0, columnspan=8, sticky="w", pady=(0, 10))
        ctk.CTkLabel(controls_frame, text="Interval (minutes):", font=FONT, text_color=FG_COLOR).grid(row=1, column=0, sticky="w", padx=7)
        self.interval_var = ctk.StringVar(value="1")
        interval_entry = ctk.CTkEntry(controls_frame, textvariable=self.interval_var, width=60, font=FONT)
        interval_entry.grid(row=1, column=1, sticky="w", padx=7)
        self.show_timing_var = ctk.BooleanVar(value=True)
        timing_cb = ctk.CTkCheckBox(controls_frame, text="Show Timing", variable=self.show_timing_var, font=FONT, text_color=FG_COLOR)
        timing_cb.grid(row=1, column=2, sticky="w", padx=7)
        self.show_ocr_var = ctk.BooleanVar(value=False)
        ocr_cb = ctk.CTkCheckBox(controls_frame, text="Show OCR", variable=self.show_ocr_var, font=FONT, text_color=FG_COLOR)
        ocr_cb.grid(row=1, column=3, sticky="w", padx=7)
        self.start_button = ctk.CTkButton(controls_frame, text="Start", command=self.start, fg_color=START_COLOR, text_color=BG_COLOR, font=BUTTON_FONT, width=100, corner_radius=8)
        self.start_button.grid(row=1, column=4, padx=16)
        self.stop_button = ctk.CTkButton(controls_frame, text="Stop", command=self.stop, state="disabled", fg_color=STOP_COLOR, text_color="#fff", font=BUTTON_FONT, width=100, corner_radius=8)
        self.stop_button.grid(row=1, column=5, padx=16)
        self.clear_button = ctk.CTkButton(controls_frame, text="Clear", command=self.clear_log, fg_color=BUTTON_COLOR, text_color=ACCENT_COLOR, font=BUTTON_FONT, width=100, corner_radius=8)
        self.clear_button.grid(row=1, column=6, padx=16)
        self.summarize_button = ctk.CTkButton(controls_frame, text="Summarize Day", command=self.summarize_day, fg_color=ACCENT_COLOR, text_color="#fff", font=BUTTON_FONT, width=140, corner_radius=8)
        self.summarize_button.grid(row=1, column=7, padx=16)
        self.stop_button.grid_remove()

        # Log card
        log_card = ctk.CTkFrame(card, fg_color=CARD_COLOR, corner_radius=14)
        log_card.pack(fill="both", expand=True, padx=24, pady=(0, 24))
        ctk.CTkLabel(log_card, text="Activity Log", font=("Segoe UI", 14, "bold"), text_color=ACCENT_COLOR).pack(anchor="w", padx=8, pady=(8, 0))
        self.log_area = ctk.CTkTextbox(log_card, width=1000, height=320, font=LOG_FONT, fg_color=BG_COLOR, text_color=FG_COLOR, border_width=2, border_color=ACCENT_COLOR, corner_radius=10)
        self.log_area.pack(fill="both", expand=True, padx=8, pady=8)
        self.log_area.configure(state="disabled")

    def log(self, message):
        self.log_area.configure(state="normal")
        self.log_area.insert(ctk.END, message + "\n")
        self.log_area.see(ctk.END)
        self.log_area.configure(state="disabled")

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.start_button.configure(state="disabled")
            self.start_button.grid_remove()
            self.stop_button.grid()
            self.stop_button.configure(state="normal")
            self.start_time = time.time()
            self.update_timer()
            self.tracker = Tracker(
                interval=int(self.interval_var.get()),
                show_timing=self.show_timing_var.get(),
                show_ocr=self.show_ocr_var.get(),
                log_callback=self.log_and_accumulate,
                minimize_callback=self.minimize_window
            )
            self.tracker.start()

    def stop(self):
        self.log("[Info] Application stopped.")
        self.is_running = False
        self.start_button.configure(state="normal")
        self.start_button.grid()
        self.stop_button.grid_remove()
        self.stop_button.configure(state="disabled")
        self.start_time = None
        self.timer_var.set("Elapsed: 00:00:00")
        if self.timer_updater:
            self.root.after_cancel(self.timer_updater)
            self.timer_updater = None
        if self.tracker:
            self.tracker.stop()

    def update_timer(self):
        if self.is_running and self.start_time is not None:
            elapsed = int(time.time() - self.start_time)
            h = elapsed // 3600
            m = (elapsed % 3600) // 60
            s = elapsed % 60
            self.timer_var.set(f"Elapsed: {h:02d}:{m:02d}:{s:02d}")
            self.timer_updater = self.root.after(1000, self.update_timer)

    def clear_log(self):
        self.log_area.configure(state="normal")
        self.log_area.delete(1.0, ctk.END)
        self.log_area.configure(state="disabled")

    def log_and_accumulate(self, message):
        self.log(message)

    def summarize_day(self):
        def run_summary():
            if self.tracker:
                bullets = self.tracker.get_bullets()
            else:
                bullets = []
            summary = summarize_day(bullets)
            self.root.after(0, lambda: self.log("[Day Summary]\n" + summary))
        threading.Thread(target=run_summary, daemon=True).start()

    def minimize_window(self):
        self.root.iconify()
