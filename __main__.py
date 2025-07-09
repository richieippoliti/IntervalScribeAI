import customtkinter as ctk
from gui import IntervalScribeGUI

if __name__ == '__main__':
    ctk.set_appearance_mode("light")  # or "dark"
    ctk.set_default_color_theme("blue")  # or "green", "dark-blue", etc.
    root = ctk.CTk()
    app = IntervalScribeGUI(root)
    root.mainloop() 