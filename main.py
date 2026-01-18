import customtkinter as ctk
from tkinter import messagebox, filedialog
import threading
import time
import sqlite3
import phonenumbers
import os
import sys
import pandas as pd
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# --- YAPILANDIRMA ---
ctk.set_appearance_mode("Dark") # Varsayılan: Koyu Tema

class ThemeManager:
    """Temaları ve renk paletlerini yöneten sınıf."""
    def __init__(self):
        self.accent_color = "#06D6A0"  # Varsayılan Yeşil
        self.hover_color = "#05C593"
        self.name = "Yeşil"
        
        # Renk Paletleri (Açık Tema, Koyu Tema)
        self.colors = {
            "bg_main": ("#F2F2F7", "#141414"),       # Ana arka plan
            "bg_sidebar": ("#FFFFFF", "#0A0A0A"),     # Yan menü
            "bg_card": ("#FFFFFF", "#1E1E1E"),        # Kart yapıları
            "bg_card_alt": ("#F7F7F7", "#252525"),    # İkincil alanlar
            "text_main": ("#1C1C1E", "#F5F5F7"),     # Ana metin
            "text_sub": ("#8E8E93", "#98989D"),       # Alt metin
            "border": ("#D1D1D6", "#38383A"),         # Kenarlıklar
            "input_bg": ("#F2F2F7", "#2C2C2E"),       # Giriş kutuları
            "success": "#34C759",                     # Başarılı (Yeşil)
            "error": "#FF3B30"                        # Hata (Kırmızı)
        }
        
    def set_theme(self, color_name):
        """Uygulamanın vurgu rengini değiştirir."""
        themes = {
            "Yeşil":  {"acc": "#06D6A0", "hov": "#05C593"},
            "Mavi":   {"acc": "#2D9CDB", "hov": "#1A7BB7"},
            "Mor":    {"acc": "#AF52DE", "hov": "#8E2BCF"},
            "Turuncu":{"acc": "#FF9500", "hov": "#E08300"},
            "Kırmızı":{"acc": "#FF3B30", "hov": "#D63429"}
        }
        if color_name in themes:
            self.accent_color = themes[color_name]["acc"]
            self.hover_color = themes[color_name]["hov"]
            self.name = color_name

THEME = ThemeManager()

class LanguageManager:
    """Çoklu dil desteğini yöneten sınıf."""
    def __init__(self):
        self.current_lang = "tr"
        self.strings = {
            "tr": {
                "app_title": "AURA PRO",
                "sidebar_title": "AURA OS",
                "status_offline": "● Sistem Kapalı",
                "status_online": "● Sistem Aktif",
                "start_engine": "BAŞLAT",
                "stop_engine": "DURDUR",
                "live_logs": "Sistem Günlükleri",
                "tab_send": "  Gönder  ",
                "tab_contacts": "  Kişiler  ",
                "tab_history": "  Geçmiş  ",
                "tab_settings": "  Ayarlar  ",
                "recipient_label": "ALICI BİLGİLERİ",
                "message_label": "MESAJ İÇERİĞİ",
                "attach_btn": "Dosya Ekle",
                "template_btn": "Şablonlar",
                "schedule_title": "ZAMANLAYICI",
                "send_btn": "GÖREVİ OLUŞTUR",
                "quick_add_10m": "+10 Dk",
                "quick_add_1h": "+1 Saat",
                "repeat_daily": "Günlük Tekrar",
                "save_contact_btn": "Kaydet",
                "import_btn": "İçe Aktar (Excel)",
                "export_btn": "Rapor Al (Excel)",
                "settings_title": "Ayarlar",
                "group_appearance": "Görünüm",
                "group_language": "Dil",
                "theme_mode": "Tema Modu",
                "theme_color": "Vurgu Rengi",
                "version": "Sürüm v1.0.0 - Final",
                "import_success": "{} kişi başarıyla eklendi.",
                "export_success": "Rapor şuraya kaydedildi: {}",
                "error_file": "Dosya okunamadı."
            },
            "en": {
                "app_title": "AURA PRO",
                "sidebar_title": "AURA OS",
                "status_offline": "● System Offline",
                "status_online": "● System Online",
                "start_engine": "START",
                "stop_engine": "STOP",
                "live_logs": "System Logs",
                "tab_send": "  Send  ",
                "tab_contacts": "  Contacts  ",
                "tab_history": "  History  ",
                "tab_settings": "  Settings  ",
                "recipient_label": "RECIPIENT INFO",
                "message_label": "MESSAGE CONTENT",
                "attach_btn": "Attach File",
                "template_btn": "Templates",
                "schedule_title": "SCHEDULER",
                "send_btn": "CREATE TASK",
                "quick_add_10m": "+10 Min",
                "quick_add_1h": "+1 Hr",
                "repeat_daily": "Repeat Daily",
                "save_contact_btn": "Save",
                "import_btn": "Import (Excel)",
                "export_btn": "Export Report",
                "settings_title": "Settings",
                "group_appearance": "Appearance",
                "group_language": "Language",
                "theme_mode": "Theme Mode",
                "theme_color": "Accent Color",
                "version": "Version v1.0.0 - Final",
                "import_success": "Successfully imported {} contacts.",
                "export_success": "Report saved to: {}",
                "error_file": "Could not read file."
            }
        }
        self.templates = {
            "tr": {"Genel": ["Merhaba", "Nasılsın?"], "İş": ["Toplantı hatırlatması", "Lütfen geri dönüş yapın"]},
            "en": {"General": ["Hello", "How are you?"], "Business": ["Meeting reminder", "Please reply ASAP"]}
        }

    def get(self, key): return self.strings[self.current_lang].get(key, key)
    def set_lang(self, code): self.current_lang = code
    def get_templates(self): return self.templates["tr"] if self.current_lang == "tr" else self.templates["en"]

LANG = LanguageManager()
DB_NAME = "aura_data.db"

# --- VERİTABANI YÖNETİCİSİ ---
class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        """Gerekli veritabanı tablolarını oluşturur."""
        self.conn.execute('CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY, name TEXT, phone TEXT UNIQUE, tag TEXT)')
        self.conn.execute('CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY, phone TEXT, message TEXT, status TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)')
        self.conn.commit()

    def add_contact(self, name, phone, tag="General"):
        try:
            self.conn.cursor().execute("INSERT OR REPLACE INTO contacts (name, phone, tag) VALUES (?, ?, ?)", (name, phone, tag))
            self.conn.commit()
            return True
        except: return False

    def get_contacts(self):
        return self.conn.cursor().execute("SELECT name, phone, tag FROM contacts ORDER BY name").fetchall()

    def log_history(self, phone, message, status):
        self.conn.cursor().execute("INSERT INTO history (phone, message, status) VALUES (?, ?, ?)", (phone, message, status))
        self.conn.commit()

    def get_history(self):
        return self.conn.cursor().execute("SELECT timestamp, phone, status, message FROM history ORDER BY timestamp DESC LIMIT 100").fetchall()
    
    def bulk_add_contacts(self, data_list):
        """Toplu kişi ekleme işlemi yapar."""
        added_count = 0
        for name, phone, tag in data_list:
             if self.add_contact(name, phone, tag):
                 added_count += 1
        return added_count

# --- WHATSAPP SÜRÜCÜSÜ (SELENIUM) ---
class WhatsAppDriver:
    def __init__(self, status_callback=None):
        self.driver = None
        self.status_callback = status_callback
        self.is_ready = False

    def log(self, text):
        if self.status_callback: self.status_callback(text)

    def start_driver(self):
        """Tarayıcıyı başlatır ve WhatsApp Web'i açar."""
        try:
            self.log("Motor Başlatılıyor...")
            o = webdriver.ChromeOptions()
            o.add_argument(f"user-data-dir={os.path.join(os.getcwd(), 'selenium_user_data')}")
            o.add_argument("--start-maximized")
            o.add_argument("--disable-infobars")
            self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=o)
            self.driver.get("https://web.whatsapp.com")
            WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.ID, "side")))
            self.is_ready = True
            self.log("Sistem Hazır.")
        except Exception as e:
            self.log(f"Hata: {e}")
            self.is_ready = False

    def send_message(self, phone, message, media=None):
        """Mesaj ve varsa medya gönderir."""
        if not self.driver: return False
        try:
            self.driver.get(f"https://web.whatsapp.com/send?phone={phone}&text={message}")
            try:
                WebDriverWait(self.driver, 25).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-icon='send']"))).click()
            except:
                webdriver.ActionChains(self.driver).send_keys(Keys.ENTER).perform()
            
            time.sleep(3)
            
            if media:
                self.send_media(media)
            return True
        except: return False

    def send_media(self, media):
        """Dosya yükleme işlemi yapar."""
        try:
            self.driver.find_element(By.CSS_SELECTOR, "span[data-icon='plus']").click()
            time.sleep(1)
            self.driver.find_element(By.CSS_SELECTOR, "input[type='file']").send_keys(media)
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-icon='send']"))).click()
            time.sleep(2)
        except: pass

    def close(self): 
        if self.driver: self.driver.quit()

# --- ANA UYGULAMA ARAYÜZÜ ---
class AuraApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.driver = WhatsAppDriver(status_callback=self.update_status)
        self.setup_window()
        self.build_ui()

    def setup_window(self):
        self.title(LANG.get("app_title"))
        self.geometry("950x800")
        self.configure(fg_color=THEME.colors["bg_main"])
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def build_ui(self):
        """Tüm arayüzü ThemeManager renklerine göre çizer."""
        for w in self.winfo_children(): w.destroy()
        
        # Yan Menü (Sidebar)
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color=THEME.colors["bg_sidebar"])
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text=LANG.get("sidebar_title"), font=("Helvetica Neue", 20, "bold"), text_color=THEME.colors["text_main"]).pack(pady=(40, 20))
        
        self.status_lbl = ctk.CTkLabel(self.sidebar, text=LANG.get("status_offline"), text_color=THEME.colors["error"], font=("Helvetica Neue", 12, "bold"))
        self.status_lbl.pack(pady=5)

        btn_font = ("Helvetica Neue", 13, "bold")
        ctk.CTkButton(self.sidebar, text=LANG.get("start_engine"), command=self.start_engine, fg_color=THEME.colors["input_bg"], hover_color=THEME.colors["bg_card"], text_color=THEME.accent_color, font=btn_font, height=40).pack(pady=(30, 10), padx=20, fill="x")
        ctk.CTkButton(self.sidebar, text=LANG.get("stop_engine"), command=self.stop_engine, fg_color=THEME.colors["input_bg"], hover_color=THEME.colors["bg_card"], text_color=THEME.colors["error"], font=btn_font, height=40).pack(pady=5, padx=20, fill="x")

        ctk.CTkLabel(self.sidebar, text=LANG.get("live_logs").upper(), font=("Helvetica Neue", 10, "bold"), text_color=THEME.colors["text_sub"]).pack(pady=(40, 5), padx=20, anchor="w")
        self.log_box = ctk.CTkTextbox(self.sidebar, font=("Menlo", 11), fg_color="transparent", text_color=THEME.colors["text_sub"], wrap="word", height=200)
        self.log_box.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Ana İçerik Alanı
        self.tabs = ctk.CTkTabview(self, fg_color="transparent", segmented_button_selected_color=THEME.accent_color, segmented_button_selected_hover_color=THEME.hover_color, segmented_button_unselected_color=THEME.colors["input_bg"], segmented_button_unselected_hover_color=THEME.colors["border"], text_color=THEME.colors["text_main"])
        self.tabs.grid(row=0, column=1, sticky="nsew", padx=30, pady=20)
        
        self.tab_send = self.tabs.add(LANG.get("tab_send"))
        self.tab_contacts = self.tabs.add(LANG.get("tab_contacts"))
        self.tab_history = self.tabs.add(LANG.get("tab_history"))
        self.tab_settings = self.tabs.add(LANG.get("tab_settings"))

        self.setup_send_tab()
        self.setup_contacts_tab()
        self.setup_history_tab()
        self.setup_settings_tab()

    # --- SEKME KURULUMLARI ---
    def setup_send_tab(self):
        t = self.tab_send
        t.grid_columnconfigure(0, weight=1)
        self.create_card(t, LANG.get("recipient_label"), 0, [("combo", self.create_contact_combo), ("entry", self.create_phone_entry)])
        self.create_card(t, LANG.get("message_label"), 1, [("textbox", self.create_msg_box), ("buttons", self.create_attach_buttons)])
        self.create_card(t, LANG.get("schedule_title"), 2, [("time", self.create_time_picker), ("options", self.create_sched_options)])
        ctk.CTkButton(t, text=LANG.get("send_btn"), height=50, fg_color=THEME.accent_color, hover_color=THEME.hover_color, font=("Helvetica Neue", 14, "bold"), command=self.queue_message).grid(row=3, column=0, sticky="ew", pady=20)

    def setup_settings_tab(self):
        t = self.tab_settings
        t.grid_columnconfigure(0, weight=1)
        container = ctk.CTkFrame(t, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=10, pady=10)

        self.create_settings_group(container, LANG.get("group_appearance"), [
            (LANG.get("theme_mode"), self.create_theme_switch),
            (LANG.get("theme_color"), self.create_color_picker)
        ])
        self.create_settings_group(container, LANG.get("group_language"), [("Region", self.create_lang_selector)])
        
        ctk.CTkLabel(container, text="AURA PRO SYSTEM", font=("Helvetica Neue", 20, "bold"), text_color=THEME.colors["text_sub"]).pack(pady=(40, 5))
        ctk.CTkLabel(container, text=LANG.get("version"), font=("Menlo", 10), text_color=THEME.colors["text_sub"]).pack()

    # --- YARDIMCI GÖRSEL FONKSİYONLAR ---
    def create_settings_group(self, parent, title, rows):
        frame = ctk.CTkFrame(parent, fg_color=THEME.colors["bg_card"], corner_radius=12, border_width=1, border_color=THEME.colors["border"])
        frame.pack(fill="x", pady=10)
        ctk.CTkLabel(frame, text=title.upper(), font=("Helvetica Neue", 11, "bold"), text_color=THEME.colors["text_sub"]).pack(anchor="w", padx=20, pady=(15, 10))
        for idx, (label_text, widget_creator) in enumerate(rows):
            if idx > 0: ctk.CTkFrame(frame, height=1, fg_color=THEME.colors["border"]).pack(fill="x", padx=20)
            row = ctk.CTkFrame(frame, fg_color="transparent", height=50)
            row.pack(fill="x", padx=20, pady=5)
            if label_text != "Region": ctk.CTkLabel(row, text=label_text, font=("Helvetica Neue", 13), text_color=THEME.colors["text_main"]).pack(side="left", pady=10)
            widget_creator(row)

    def create_theme_switch(self, parent):
        mode = ctk.get_appearance_mode()
        icon = "🌙" if mode == "Dark" else "☀️"
        ctk.CTkButton(parent, text=f"{icon} {mode}", width=80, height=28, fg_color=THEME.colors["input_bg"], text_color=THEME.colors["text_main"], hover_color=THEME.colors["bg_card_alt"], command=self.toggle_mode).pack(side="right")

    def create_color_picker(self, parent):
        colors = {"Yeşil": "#06D6A0", "Mavi": "#2D9CDB", "Mor": "#AF52DE", "Turuncu": "#FF9500", "Kırmızı": "#FF3B30"}
        wrapper = ctk.CTkFrame(parent, fg_color="transparent")
        wrapper.pack(side="right")
        for name, hexcode in colors.items():
            is_active = (THEME.name == name)
            border_c = THEME.colors["text_main"]
            border_w = 2 if is_active else 0
            ctk.CTkButton(wrapper, text="", width=24, height=24, corner_radius=12, fg_color=hexcode, hover_color=hexcode, border_width=border_w, border_color=border_c, command=lambda n=name: self.change_theme(n)).pack(side="left", padx=3)

    def create_lang_selector(self, parent):
        seg = ctk.CTkSegmentedButton(parent, values=["Türkçe", "English"], command=self.set_language, selected_color=THEME.accent_color, selected_hover_color=THEME.hover_color, unselected_color=THEME.colors["input_bg"], unselected_hover_color=THEME.colors["border"], text_color=THEME.colors["text_main"])
        seg.pack(fill="x", pady=5); seg.set("Türkçe" if LANG.current_lang == "tr" else "English")

    def create_card(self, parent, title, row, widgets):
        f = ctk.CTkFrame(parent, fg_color=THEME.colors["bg_card"], corner_radius=10, border_width=1, border_color=THEME.colors["border"])
        f.grid(row=row, column=0, sticky="ew", pady=8)
        ctk.CTkLabel(f, text=title, font=("Helvetica Neue", 11, "bold"), text_color=THEME.colors["text_sub"]).pack(anchor="w", padx=15, pady=(12, 5))
        for _, func in widgets: func(f)

    def create_contact_combo(self, parent):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(fill="x", padx=15, pady=(0, 5))
        self.contact_var = ctk.StringVar()
        self.contact_combo = ctk.CTkComboBox(f, variable=self.contact_var, width=200, command=self.on_contact_select, fg_color=THEME.colors["input_bg"], border_color=THEME.colors["border"], text_color=THEME.colors["text_main"], button_color=THEME.colors["input_bg"], button_hover_color=THEME.colors["border"], dropdown_fg_color=THEME.colors["bg_card"])
        self.contact_combo.pack(side="left", fill="x", expand=True); self.refresh_contact_combo()

    def create_phone_entry(self, parent):
        self.manual_phone = ctk.CTkEntry(parent, placeholder_text="+90...", height=35, fg_color=THEME.colors["input_bg"], border_color=THEME.colors["border"], text_color=THEME.colors["text_main"])
        self.manual_phone.pack(fill="x", padx=15, pady=(0, 15))

    def create_msg_box(self, parent):
        self.msg_text = ctk.CTkTextbox(parent, height=100, fg_color="transparent", text_color=THEME.colors["text_main"], font=("Helvetica Neue", 14), wrap="word")
        self.msg_text.pack(fill="x", padx=15)

    def create_attach_buttons(self, parent):
        f = ctk.CTkFrame(parent, fg_color=THEME.colors["bg_card_alt"], height=40, corner_radius=6)
        f.pack(fill="x", padx=5, pady=5)
        self.file_path_var = ctk.StringVar()
        ctk.CTkButton(f, text=f"📋 {LANG.get('template_btn')}", width=80, height=28, fg_color="transparent", text_color=THEME.colors["text_main"], font=("bold", 11), command=self.open_template_popup).pack(side="left", padx=5, pady=5)
        ctk.CTkButton(f, text=f"📎 {LANG.get('attach_btn')}", width=80, height=28, fg_color="transparent", text_color=THEME.colors["text_main"], font=("bold", 11), command=self.browse_file).pack(side="right", padx=5, pady=5)
        ctk.CTkLabel(f, textvariable=self.file_path_var, font=("Menlo", 10), text_color=THEME.colors["text_sub"]).pack(side="left", padx=5)

    def create_time_picker(self, parent):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(fill="x", padx=15, pady=10)
        self.sched_hour = ctk.CTkComboBox(f, values=[f"{i:02d}" for i in range(24)], width=70, height=35, font=("Helvetica Neue", 16), fg_color=THEME.colors["input_bg"], text_color=THEME.colors["text_main"], state="readonly")
        self.sched_hour.pack(side="left"); self.sched_hour.set(datetime.now().strftime("%H"))
        ctk.CTkLabel(f, text=":", font=("bold", 20), text_color=THEME.colors["text_main"]).pack(side="left", padx=5)
        self.sched_min = ctk.CTkComboBox(f, values=[f"{i:02d}" for i in range(60)], width=70, height=35, font=("Helvetica Neue", 16), fg_color=THEME.colors["input_bg"], text_color=THEME.colors["text_main"], state="readonly")
        self.sched_min.pack(side="left"); self.sched_min.set(f"{(datetime.now().minute+2)%60:02d}")

    def create_sched_options(self, parent):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(fill="x", padx=15, pady=(0, 15))
        self.recurring_chk = ctk.CTkSwitch(f, text=LANG.get("repeat_daily"), progress_color=THEME.accent_color, text_color=THEME.colors["text_main"], font=("Helvetica Neue", 12))
        self.recurring_chk.pack(side="left")
        ctk.CTkButton(f, text=LANG.get("quick_add_1h"), width=60, height=24, fg_color=THEME.colors["bg_card_alt"], text_color=THEME.colors["text_main"], command=lambda: self.add_time(60)).pack(side="right")
        ctk.CTkButton(f, text=LANG.get("quick_add_10m"), width=60, height=24, fg_color=THEME.colors["bg_card_alt"], text_color=THEME.colors["text_main"], command=lambda: self.add_time(10)).pack(side="right", padx=5)
    
    # --- KİŞİLER & GEÇMİŞ TABLARI ---
    def setup_contacts_tab(self):
        t = self.tab_contacts
        t.grid_columnconfigure(0, weight=1)
        f = ctk.CTkFrame(t, fg_color=THEME.colors["bg_card"], corner_radius=10, border_color=THEME.colors["border"], border_width=1)
        f.grid(row=0, column=0, sticky="ew", pady=10)
        self.c_name = ctk.CTkEntry(f, placeholder_text="İsim", fg_color=THEME.colors["input_bg"], border_color=THEME.colors["border"], text_color=THEME.colors["text_main"])
        self.c_name.pack(side="left", fill="x", expand=True, padx=10, pady=10)
        self.c_phone = ctk.CTkEntry(f, placeholder_text="Telefon", fg_color=THEME.colors["input_bg"], border_color=THEME.colors["border"], text_color=THEME.colors["text_main"])
        self.c_phone.pack(side="left", fill="x", expand=True, padx=10, pady=10)
        ctk.CTkButton(f, text=LANG.get("save_contact_btn"), command=self.save_new_contact, fg_color=THEME.accent_color, hover_color=THEME.hover_color, text_color="white").pack(side="left", padx=10)
        
        row_act = ctk.CTkFrame(t, fg_color="transparent")
        row_act.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        ctk.CTkButton(row_act, text=f"📥 {LANG.get('import_btn')}", command=self.import_from_excel, fg_color=THEME.colors["bg_card_alt"], text_color=THEME.colors["text_main"], height=30).pack(side="left", padx=5)

        self.contact_list_frame = ctk.CTkScrollableFrame(t, fg_color="transparent")
        self.contact_list_frame.grid(row=2, column=0, sticky="nsew", pady=5)
        self.grid_rowconfigure(2, weight=1); self.load_contacts_list()

    def setup_history_tab(self):
        t = self.tab_history
        t.grid_columnconfigure(0, weight=1)
        
        row_tools = ctk.CTkFrame(t, fg_color="transparent")
        row_tools.grid(row=0, column=0, sticky="ew", pady=5)
        ctk.CTkButton(row_tools, text=f"📤 {LANG.get('export_btn')}", command=self.export_report, fg_color=THEME.colors["bg_card_alt"], text_color=THEME.colors["text_main"], height=30).pack(side="left")
        ctk.CTkButton(row_tools, text="↻ Yenile", width=60, command=self.load_history_list, fg_color=THEME.colors["bg_card"], text_color=THEME.colors["text_main"]).pack(side="right")
        
        self.history_frame = ctk.CTkScrollableFrame(t, fg_color="transparent")
        self.history_frame.grid(row=1, column=0, sticky="nsew")
        self.load_history_list()

    # --- UYGULAMA MANTIĞI & OLAYLAR ---
    def change_theme(self, name): THEME.set_theme(name); self.build_ui()
    def toggle_mode(self): ctk.set_appearance_mode("Light" if ctk.get_appearance_mode() == "Dark" else "Dark"); self.after(200, self.build_ui)
    def set_language(self, val): LANG.set_lang("tr" if val == "Türkçe" else "en"); self.build_ui()
    
    def start_engine(self): threading.Thread(target=self.driver.start_driver, daemon=True).start()
    def stop_engine(self): 
        if self.driver: self.driver.close(); self.status_lbl.configure(text=LANG.get("status_offline"), text_color=THEME.colors["error"])
    def update_status(self, text):
        self.log_box.insert("end", f"\n> {text}"); self.log_box.see("end")
        if "Hazır" in text or "Ready" in text: self.status_lbl.configure(text=LANG.get("status_online"), text_color=THEME.colors["success"])
    
    def import_from_excel(self):
        """Excel'den kişi listesi yükler."""
        p = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx;*.xls"), ("CSV", "*.csv")])
        if not p: return
        try:
            df = pd.read_csv(p) if p.endswith(".csv") else pd.read_excel(p)
            df.columns = [c.lower().strip() for c in df.columns]
            if 'name' not in df.columns or 'phone' not in df.columns:
                 messagebox.showerror("Hata", "Dosyada 'name' ve 'phone' sütunları olmalı.")
                 return
            data = []
            for _, row in df.iterrows():
                n = str(row['name'])
                ph = self.format_phone(str(row['phone']))
                if n and ph:
                    data.append((n, ph, "Imported"))
            cnt = self.db.bulk_add_contacts(data)
            self.load_contacts_list()
            self.refresh_contact_combo()
            messagebox.showinfo("Başarılı", LANG.get("import_success").format(cnt))
        except Exception as e: messagebox.showerror("Hata", f"Yükleme hatası: {e}")

    def export_report(self):
        """Gönderim geçmişini Excel olarak kaydeder."""
        try:
            hist = self.db.get_history()
            if not hist: return
            f = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx")])
            if not f: return
            df = pd.DataFrame(hist, columns=["Tarih", "Telefon", "Durum", "Mesaj"])
            df.to_excel(f, index=False)
            messagebox.showinfo("Başarılı", LANG.get("export_success").format(f))
            os.startfile(f)
        except Exception as e: messagebox.showerror("Hata", f"Dışa aktarma hatası: {e}")

    def load_contacts_list(self):
        for w in self.contact_list_frame.winfo_children(): w.destroy()
        for i, (n, p, t) in enumerate(self.db.get_contacts()):
            f = ctk.CTkFrame(self.contact_list_frame, fg_color=THEME.colors["bg_card"], corner_radius=8); f.pack(fill="x", pady=2)
            ctk.CTkLabel(f, text=n, font=("bold", 12), text_color=THEME.colors["text_main"]).pack(side="left", padx=15, pady=8)
            ctk.CTkLabel(f, text=p, text_color=THEME.colors["text_sub"]).pack(side="left")
            ctk.CTkButton(f, text="→", width=30, height=20, fg_color="transparent", text_color=THEME.accent_color, command=lambda x=p: [self.manual_phone.delete(0, "end"), self.manual_phone.insert(0, x), self.tabs.set(LANG.get("tab_send"))]).pack(side="right", padx=10)
    
    def load_history_list(self):
        for w in self.history_frame.winfo_children(): w.destroy()
        for r in self.db.get_history():
            f = ctk.CTkFrame(self.history_frame, fg_color=THEME.colors["bg_card"], corner_radius=8); f.pack(fill="x", pady=2)
            c = THEME.colors["success"] if "Success" in r[2] else THEME.colors["error"]
            ctk.CTkLabel(f, text="●", text_color=c).pack(side="left", padx=10)
            ctk.CTkLabel(f, text=r[0], width=120, text_color=THEME.colors["text_sub"], font=("Menlo", 10)).pack(side="left")
            ctk.CTkLabel(f, text=r[3][:40], text_color=THEME.colors["text_main"]).pack(side="left")

    def queue_message(self):
        p = self.format_phone(self.manual_phone.get()); m = self.msg_text.get("0.0", "end").strip(); f = self.file_path_var.get()
        if not p or (not m and not f): return messagebox.showerror("Hata", "Geçersiz giriş.")
        h=int(self.sched_hour.get()); mn=int(self.sched_min.get()); now=datetime.now(); t=now.replace(hour=h, minute=mn, second=0)
        if t<now: t+=timedelta(days=1)
        threading.Thread(target=self.wait_and_send, args=(p, m, f, (t-now).total_seconds()), daemon=True).start()
        messagebox.showinfo("Zamanlandı", f"Mesaj {t.strftime('%H:%M')} saatine ayarlandı.")
    
    def wait_and_send(self, p,m,f,w):
        time.sleep(w)
        if not self.driver.is_ready: self.driver.start_driver()
        s = self.driver.send_message(p,m,f)
        self.db.log_history(p, m, "Success" if s else "Failed")

    def format_phone(self, n):
        try: p = phonenumbers.parse("+90"+n if not n.startswith("+") else n, None); return phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.E164) if phonenumbers.is_valid_number(p) else None
        except: return None
    
    def save_new_contact(self): self.db.add_contact(self.c_name.get(), self.format_phone(self.c_phone.get())); self.load_contacts_list(); self.refresh_contact_combo()
    def refresh_contact_combo(self): self.contact_combo.configure(values=[f"{c[0]} ({c[1]})" for c in self.db.get_contacts()])
    def on_contact_select(self, v): 
        if "(" in v: self.manual_phone.delete(0,"end"); self.manual_phone.insert(0, v.split("(")[1].replace(")", ""))
    def open_template_popup(self):
        t=ctk.CTkToplevel(self); t.geometry("300x400"); t.attributes("-topmost", True)
        scroll = ctk.CTkScrollableFrame(t); scroll.pack(fill="both", expand=True)
        for c, m in LANG.get_templates().items(): 
            ctk.CTkLabel(scroll, text=c, font=("bold", 12)).pack(pady=5)
            for x in m: ctk.CTkButton(scroll, text=x, command=lambda v=x: [self.msg_text.insert("end", v), t.destroy()]).pack(pady=2, fill="x")
    def browse_file(self): 
        f=filedialog.askopenfilename(); 
        if f: self.file_path_var.set(f)
    def add_time(self, m):
        try: t = datetime.now().replace(hour=int(self.sched_hour.get()), minute=int(self.sched_min.get())) + timedelta(minutes=m); self.sched_hour.set(f"{t.hour:02d}"); self.sched_min.set(f"{t.minute:02d}")
        except: pass

if __name__ == "__main__":
    AuraApp().mainloop()