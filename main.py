import customtkinter as ctk
from tkinter import filedialog, messagebox
import pywhatkit as kt
from datetime import datetime
import threading
import os
import sys

# Aesthetic Configuration
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class WhatsAppSchedulerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Configuration
        self.title("Aura - Modern WhatsApp Scheduler")
        self.geometry("600x750")
        self.resizable(False, False)
        
        # Grid Configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=0)

        # Variables
        self.phone_var = ctk.StringVar()
        self.hour_var = ctk.StringVar(value=datetime.now().strftime("%H"))
        # Default to 2 minutes later for convenience
        next_min = (datetime.now().minute + 2) % 60
        self.minute_var = ctk.StringVar(value=f"{next_min:02d}")

        self.setup_ui()

    def setup_ui(self):
        # 1. Header Section
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(25, 15))
        
        title = ctk.CTkLabel(self.header_frame, text="AURA SCHEDULER", font=("Roboto Medium", 28))
        title.pack()
        
        subtitle = ctk.CTkLabel(self.header_frame, text="Advanced WhatsApp Automation", font=("Roboto", 12), text_color="gray60")
        subtitle.pack()

        # 2. Main Container
        self.main_frame = ctk.CTkFrame(self, fg_color="#2B2B2B", corner_radius=15)
        self.main_frame.grid(row=1, column=0, sticky="ew", padx=25, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Phone Input
        ctk.CTkLabel(self.main_frame, text="TARGET PHONE NUMBER", font=("Roboto", 11, "bold"), text_color="#A0A0A0").grid(row=0, column=0, sticky="w", padx=20, pady=(20, 5))
        self.phone_entry = ctk.CTkEntry(self.main_frame, textvariable=self.phone_var, 
                                        placeholder_text="+90 555 000 0000",
                                        height=45, font=("Roboto", 14), border_color="#3E3E3E", fg_color="#1E1E1E")
        self.phone_entry.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 15))

        # Message Input
        ctk.CTkLabel(self.main_frame, text="MESSAGE CONTENT", font=("Roboto", 11, "bold"), text_color="#A0A0A0").grid(row=2, column=0, sticky="w", padx=20, pady=(5, 5))
        self.msg_textbox = ctk.CTkTextbox(self.main_frame, height=150, font=("Roboto", 14), 
                                          fg_color="#1E1E1E", border_color="#3E3E3E", border_width=2)
        self.msg_textbox.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 15))

        # Tools Row
        self.tools_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.tools_frame.grid(row=4, column=0, sticky="ew", padx=20, pady=(0, 20))
        
        ctk.CTkButton(self.tools_frame, text="📁 Import Text", width=100, fg_color="#454545", hover_color="#555555", command=self.load_file).pack(side="left", padx=(0, 10))
        ctk.CTkButton(self.tools_frame, text="📋 Templates", width=100, fg_color="#454545", hover_color="#555555", command=self.open_templates).pack(side="left", padx=(0, 10))
        ctk.CTkButton(self.tools_frame, text="😀 Emojis", width=80, fg_color="#FFB703", hover_color="#FFC300", text_color="black", command=self.open_emojis).pack(side="right")

        # 3. Timing Section
        self.time_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.time_frame.grid(row=2, column=0, sticky="ew", padx=25, pady=10)
        
        ctk.CTkLabel(self.time_frame, text="SCHEDULE TIME (24H)", font=("Roboto", 12, "bold"), text_color="gray70").pack(anchor="w")
        
        time_inner = ctk.CTkFrame(self.time_frame, fg_color="#2B2B2B", corner_radius=10)
        time_inner.pack(fill="x", pady=5)
        
        hours = [f"{i:02d}" for i in range(24)]
        minutes = [f"{i:02d}" for i in range(60)]
        
        self.hour_combo = ctk.CTkComboBox(time_inner, values=hours, variable=self.hour_var, width=100, height=40, font=("Roboto", 16))
        self.hour_combo.pack(side="left", padx=20, pady=15)
        
        ctk.CTkLabel(time_inner, text=":", font=("Roboto", 24, "bold")).pack(side="left")
        
        self.minute_combo = ctk.CTkComboBox(time_inner, values=minutes, variable=self.minute_var, width=100, height=40, font=("Roboto", 16))
        self.minute_combo.pack(side="left", padx=20, pady=15)

        # 4. Action Button
        self.send_btn = ctk.CTkButton(self, text="SCHEDULE MESSAGE", height=55, 
                                      font=("Roboto", 16, "bold"), 
                                      fg_color="#06D6A0", hover_color="#05C593", text_color="white",
                                      command=self.initiate_send)
        self.send_btn.grid(row=3, column=0, sticky="ew", padx=25, pady=20)

        # 5. Status & Footer
        self.status_label = ctk.CTkLabel(self, text="System Ready", font=("Roboto", 12), text_color="#06D6A0")
        self.status_label.grid(row=4, column=0, pady=5)
        
        ctk.CTkButton(self, text="EXIT APPLICATION", fg_color="transparent", text_color="#EF476F", hover_color="#2B2B2B", command=self.destroy).grid(row=5, column=0, pady=10)

    # --- Logic ---

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if path:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self.msg_textbox.delete("0.0", "end")
                    self.msg_textbox.insert("0.0", f.read())
                self.status_label.configure(text="File loaded successfully", text_color="#06D6A0")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")

    def open_templates(self):
        toplevel = ctk.CTkToplevel(self)
        toplevel.title("Quick Templates")
        toplevel.geometry("300x400")
        toplevel.attributes("-topmost", True)
        
        templates = {
            "Birthday Wish": "Happy Birthday! 🎂 Hope you have an amazing day!",
            "Meeting Reminder": "Hello, just a reminder about our meeting tomorrow at [TIME]. 📅",
            "Greetings": "Hi there! Just wanted to say hello. 👋",
            "Emergency": "Please call me back as soon as possible. It's urgent. 🚨"
        }
        
        scroll = ctk.CTkScrollableFrame(toplevel)
        scroll.pack(fill="both", expand=True)
        
        def apply(text):
            self.msg_textbox.delete("0.0", "end")
            self.msg_textbox.insert("0.0", text)
            toplevel.destroy()
            
        for title, content in templates.items():
            ctk.CTkButton(scroll, text=title, command=lambda c=content: apply(c), 
                          fg_color="transparent", border_width=1, border_color="gray50").pack(pady=5, fill="x", padx=10)

    def open_emojis(self):
        toplevel = ctk.CTkToplevel(self)
        toplevel.title("Emoji Picker")
        toplevel.geometry("350x300")
        toplevel.attributes("-topmost", True)
        
        emojis = ["😀", "😂", "😍", "🥳", "😎", "🤔", "👍", "👎", "🔥", "💯", "❤️", "✅", "❌", "👋", "🎉", "💩", "👀", "🙌", "🎂", "🍕"]
        
        frame = ctk.CTkFrame(toplevel, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        def insert_emoji(e):
            self.msg_textbox.insert("insert", e)
            
        for i, em in enumerate(emojis):
            row = i // 5
            col = i % 5
            ctk.CTkButton(frame, text=em, width=40, height=40, fg_color="#333", command=lambda e=em: insert_emoji(e)).grid(row=row, column=col, padx=5, pady=5)

    def initiate_send(self):
        phone = self.phone_var.get().strip()
        msg = self.msg_textbox.get("0.0", "end").strip()
        
        try:
            h = int(self.hour_var.get())
            m = int(self.minute_var.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid time.")
            return

        if not phone or not msg:
            messagebox.showwarning("Incomplete", "Please provide both a phone number and a message.")
            return

        # Simple confirmation
        if messagebox.askyesno("Confirm Schedule", f"Send to: {phone}\nAt: {h:02d}:{m:02d}\n\nProceed?"):
             self.status_label.configure(text=f"Scheduled for {h:02d}:{m:02d}... Do not close app.", text_color="#FFB703")
             thread = threading.Thread(target=self.run_scheduler, args=(phone, msg, h, m))
             thread.daemon = True
             thread.start()

    def run_scheduler(self, phone, msg, h, m):
        try:
            # Note: pywhatkit.sendwhatmsg blocks execution until the time is reached
            # It also takes control of the mouse/keyboard at that time.
            kt.sendwhatmsg(phone, msg, h, m)
            self.status_label.configure(text="Message Sent Successfully!", text_color="#06D6A0")
        except Exception as e:
            self.status_label.configure(text=f"Failed: {e}", text_color="#EF476F")

if __name__ == "__main__":
    app = WhatsAppSchedulerApp()
    app.mainloop()
