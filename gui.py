import tkinter as tk
from tkinter import scrolledtext
from tracker import Tracker
from summarizer import summarize_day
import time

class IntervalScribeGUI:
    def __init__(self, root):
        # Modern dark theme colors
        BG_COLOR = "#23272e"
        FG_COLOR = "#f8f8f2"
        ACCENT_COLOR = "#61dafb"
        BUTTON_COLOR = "#282c34"
        BUTTON_ACTIVE = "#3c4048"
        START_COLOR = "#43d17a"
        STOP_COLOR = "#e06c75"
        FONT = ("Segoe UI", 12)
        TITLE_FONT = ("Segoe UI", 20, "bold")
        BUTTON_FONT = ("Segoe UI", 12, "bold")
        ENTRY_BG = "#2c313c"
        ENTRY_FG = FG_COLOR
        FRAME_BG = "#282c34"

        self.root = root
        self.root.title("IntervalScribe AI")
        self.root.minsize(900, 650)
        self.root.configure(bg=BG_COLOR)
        self.tracker = None
        self.tracker_thread = None
        self.is_running = False
        self.start_time = None
        self.timer_updater = None

        # Title label
        title_label = tk.Label(root, text="🕒 IntervalScribe AI", font=TITLE_FONT, fg=ACCENT_COLOR, bg=BG_COLOR)
        title_label.pack(pady=(18, 0))

        # Timer label
        self.timer_var = tk.StringVar(value="Elapsed: 00:00:00")
        self.timer_label = tk.Label(root, textvariable=self.timer_var, font=("Segoe UI", 14), fg=ACCENT_COLOR, bg=BG_COLOR)
        self.timer_label.pack(pady=(0, 10))

        # Controls frame
        controls_frame = tk.LabelFrame(root, text="Controls", padx=16, pady=14, bg=FRAME_BG, fg=ACCENT_COLOR, font=FONT, bd=2, relief="groove", labelanchor="nw")
        controls_frame.pack(fill="x", padx=28, pady=16)

        # Interval
        tk.Label(controls_frame, text="Interval (minutes):", font=FONT, bg=FRAME_BG, fg=FG_COLOR).grid(row=0, column=0, sticky="w", padx=7)
        self.interval_var = tk.StringVar(value="1")
        interval_entry = tk.Entry(controls_frame, textvariable=self.interval_var, width=5, font=FONT, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=ENTRY_FG, relief="flat", highlightthickness=1, highlightbackground=ACCENT_COLOR)
        interval_entry.grid(row=0, column=1, sticky="w", padx=7)

        # Show Timing
        self.show_timing_var = tk.BooleanVar(value=True)
        timing_cb = tk.Checkbutton(controls_frame, text="Show Timing", variable=self.show_timing_var, font=FONT, bg=FRAME_BG, fg=FG_COLOR, activebackground=FRAME_BG, activeforeground=ACCENT_COLOR, selectcolor=FRAME_BG)
        timing_cb.grid(row=0, column=2, sticky="w", padx=7)

        # Show OCR
        self.show_ocr_var = tk.BooleanVar(value=False)
        ocr_cb = tk.Checkbutton(controls_frame, text="Show OCR", variable=self.show_ocr_var, font=FONT, bg=FRAME_BG, fg=FG_COLOR, activebackground=FRAME_BG, activeforeground=ACCENT_COLOR, selectcolor=FRAME_BG)
        ocr_cb.grid(row=0, column=3, sticky="w", padx=7)

        # Start/Stop buttons
        self.start_button = tk.Button(controls_frame, text="Start", command=self.start, bg=START_COLOR, fg=BG_COLOR, font=BUTTON_FONT, width=10, relief="flat", bd=0, activebackground=ACCENT_COLOR, activeforeground=BG_COLOR, cursor="hand2")
        self.start_button.grid(row=0, column=4, padx=16)
        self.stop_button = tk.Button(controls_frame, text="Stop", command=self.stop, state=tk.DISABLED, bg=STOP_COLOR, fg=BG_COLOR, font=BUTTON_FONT, width=10, relief="flat", bd=0, activebackground=ACCENT_COLOR, activeforeground=BG_COLOR, cursor="hand2")
        self.stop_button.grid(row=0, column=5, padx=16)

        # Clear button
        self.clear_button = tk.Button(controls_frame, text="Clear", command=self.clear_log, bg=BUTTON_COLOR, fg=ACCENT_COLOR, font=BUTTON_FONT, width=10, relief="flat", bd=0, activebackground=BUTTON_ACTIVE, activeforeground=ACCENT_COLOR, cursor="hand2")
        self.clear_button.grid(row=0, column=6, padx=16)

        # Summarize Day button
        self.summarize_button = tk.Button(controls_frame, text="Summarize Day", command=self.summarize_day, bg=ACCENT_COLOR, fg=BG_COLOR, font=BUTTON_FONT, width=14, relief="flat", bd=0, activebackground=START_COLOR, activeforeground=BG_COLOR, cursor="hand2")
        self.summarize_button.grid(row=0, column=7, padx=16)
        self.summarize_button.bind("<Enter>", lambda e: self.summarize_button.config(bg=START_COLOR))
        self.summarize_button.bind("<Leave>", lambda e: self.summarize_button.config(bg=ACCENT_COLOR))

        # Add hover effects for buttons
        self.start_button.bind("<Enter>", lambda e: self.start_button.config(bg=ACCENT_COLOR))
        self.start_button.bind("<Leave>", lambda e: self.start_button.config(bg=START_COLOR))
        self.stop_button.bind("<Enter>", lambda e: self.stop_button.config(bg=ACCENT_COLOR))
        self.stop_button.bind("<Leave>", lambda e: self.stop_button.config(bg=STOP_COLOR))
        self.clear_button.bind("<Enter>", lambda e: self.clear_button.config(bg=ACCENT_COLOR))
        self.clear_button.bind("<Leave>", lambda e: self.clear_button.config(bg=BUTTON_COLOR))

        # Log area
        self.log_area = scrolledtext.ScrolledText(root, width=100, height=30, state=tk.DISABLED, font=("Fira Mono", 13), bg=BG_COLOR, fg=FG_COLOR, insertbackground=ACCENT_COLOR, relief="flat", borderwidth=2, highlightthickness=1, highlightbackground=ACCENT_COLOR, padx=12, pady=12)
        self.log_area.pack(fill="both", expand=True, padx=28, pady=(0, 24))

        # Hide Stop button by default
        self.stop_button.grid_remove()

    def log(self, message):
        self.log_area.config(state=tk.NORMAL)
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state=tk.DISABLED)

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.start_button.config(state=tk.DISABLED)
            self.start_button.grid_remove()  # Hide Start button
            self.stop_button.grid()         # Show Stop button
            self.stop_button.config(state=tk.NORMAL)
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
        self.start_button.config(state=tk.NORMAL)
        self.start_button.grid()           # Show Start button
        self.stop_button.grid_remove()     # Hide Stop button
        self.stop_button.config(state=tk.DISABLED)
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
        self.log_area.config(state=tk.NORMAL)
        self.log_area.delete(1.0, tk.END)
        self.log_area.config(state=tk.DISABLED)

    def log_and_accumulate(self, message):
        self.log(message)

    def summarize_day(self):
        if self.tracker:
            bullets = self.tracker.get_bullets()
        else:
            bullets = []
        summary = summarize_day(bullets)
        self.log("[Day Summary]\n" + summary)

    def minimize_window(self):
        self.root.iconify()
