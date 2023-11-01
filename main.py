import pywhatkit as kt
import tkinter as tk
from tkinter import messagebox, Toplevel, filedialog
from datetime import datetime
import webbrowser
import requests
from tkinter.colorchooser import askcolor

class UserNameInputApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Discord Kullanıcı Adınızı Girin")

        self.label_username = tk.Label(root, text="Lütfen Discord Kullanıcı Adınızı Girin:", font=("Arial", 14))
        self.label_username.pack(pady=20)

        self.entry_username = tk.Entry(root, font=("Arial", 12))
        self.entry_username.pack()

        self.submit_button = tk.Button(root, text="Onayla", font=("Arial", 12), command=self.open_main_app)
        self.submit_button.pack(pady=10)

    def open_main_app(self):
        user_name = self.entry_username.get()
        if user_name:
            self.root.destroy()  # Kullanıcı adı girme penceresini kapat
            root = tk.Tk()
            app = WhatsAppSchedulerApp(root, user_name)
            root.mainloop()

class WhatsAppSchedulerApp:
    def __init__(self, root, user_name):
        self.root = root
        self.root.title("WhatsApp Mesaj Gönderici")
        self.root.configure(bg="#f0f0f0")
        self.user_name = user_name  # Kullanıcı adını kaydet
        self.create_ui()

    def create_username_window(self):
        username_window = tk.Toplevel(self.root)
        username_window.title("Discord Kullanıcı Adınızı Girin")

        label_username = tk.Label(username_window, text="Lütfen Discord Kullanıcı Adınızı Girin:", font=("Arial", 14))
        label_username.pack(pady=20)

        self.entry_username = tk.Entry(username_window, font=("Arial", 12))
        self.entry_username.pack()

        submit_button = tk.Button(username_window, text="Giriş", font=("Arial", 12), command=self.on_submit_username)
        submit_button.pack(pady=10)

    def on_submit_username(self):
        self.user_name = self.entry_username.get()
        if self.user_name:
            self.root.deiconify()  # Ana pencereyi görünür yap
            self.create_ui()

    def create_ui(self):
        title_label = tk.Label(self.root, text="WhatsApp Mesaj Gönderici", font=("Helvetica", 24, "bold"), fg="#4a90e2", bg="#f0f0f0")
        title_label.pack(pady=20)

        self.label_welcome = tk.Label(self.root, text=f"Hoş geldiniz, {self.user_name}!", font=("Arial", 16), bg="#f0f0f0")
        self.label_welcome.pack(pady=20)

        mobile_frame = tk.Frame(self.root, bg="#f0f0f0")
        mobile_frame.pack(pady=10)
        
        self.label_mobile = tk.Label(mobile_frame, text="Alıcının Telefon Numarasını Girin:", font=("Arial", 12), bg="#f0f0f0")
        self.label_mobile.pack(side="left")
        self.entry_mobile = tk.Entry(mobile_frame, font=("Arial", 12))
        self.entry_mobile.pack(side="left")

        message_frame = tk.Frame(self.root, bg="#f0f0f0")
        message_frame.pack(pady=10)
        self.label_message = tk.Label(message_frame, text="Göndermek istediğiniz Mesajı Girin veya Dosyadan Yükleyin:", font=("Arial", 12), bg="#f0f0f0")
        self.label_message.pack(side="top")
        self.message_editor = tk.Text(message_frame, height=5, width=40, font=("Arial", 10))
        self.message_editor.pack(side="top")

        # Hover Efekti Fonksiyonları
        def on_hover(event):
            event.widget.config(bg="#FFC947", fg="white")

        def on_leave(event):
            event.widget.config(bg="#FFA733", fg="black")

        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(pady=10)

        #emoji düğmesi
        self.emoji_button = tk.Button(button_frame, text="Emoji Seçin", font=("Arial", 12), bg="#FFA733", fg="black", command=self.open_emoji_picker)
        self.emoji_button.pack(side="left", padx=5, pady=5)
        self.emoji_button.bind("<Enter>", on_hover)
        self.emoji_button.bind("<Leave>", on_leave)
        #Şablon düğmesi
        self.template_button = tk.Button(button_frame, text="Şablon Seçin", font=("Arial", 12), bg="#FFA733", fg="black", command=self.show_template_menu)
        self.template_button.pack(side="left", padx=5, pady=5)
        self.template_button.bind("<Enter>", on_hover)
        self.template_button.bind("<Leave>", on_leave)
        #Dosya Seçme düğmesi
        self.button_load_file = tk.Button(button_frame, text="Dosya Seç", font=("Arial", 12), bg="#FFA733", fg="black", command=self.load_file)
        self.button_load_file.pack(side="left", padx=5, pady=5)
        self.button_load_file.bind("<Enter>", on_hover)
        self.button_load_file.bind("<Leave>", on_leave)
        #Gönderme Zamanı yeri
        time_frame = tk.Frame(self.root, bg="#f0f0f0")
        time_frame.pack(pady=10)
        self.label_time = tk.Label(time_frame, text="Gönderme Zamanını Girin (Saat:Dakika):", font=("Arial", 12), bg="#f0f0f0")
        self.label_time.pack(side="left")

        self.time_picker = tk.Spinbox(time_frame, font=("Arial", 12), from_=0, to=23, width=2)
        self.time_picker.pack(side="left")
        time_separator_label = tk.Label(time_frame, text=":", font=("Arial", 12), bg="#f0f0f0")
        time_separator_label.pack(side="left")
        self.minute_picker = tk.Spinbox(time_frame, font=("Arial", 12), from_=0, to=59, width=2)
        self.minute_picker.pack(side="left")
        #Mesaj Gönderme düğmesi
        self.button_send = tk.Button(self.root, text="Mesajı Gönder", font=("Arial", 14, "bold"), bg="#25D366", fg="white", command=self.send_message)
        self.button_send.pack(pady=20)
        #yardım düğmesi
        help_button = tk.Button(self.root, text="Yardım", font=("Arial", 12), bg="#FF5733", fg="white", command=self.show_help)
        help_button.pack()
        #Hakkında düğmesi
        self.about_icon = "❓"
        about_button = tk.Button(self.root, text=f"{self.about_icon} Hakkında", font=("Arial", 12), bg="#7289DA", fg="white", command=self.show_about)
        about_button.pack(pady=10)

        #çıkış yapma düğmesi
        self.exit_button = tk.Button(self.root, text="Çıkış Yap", font=("Arial", 12), relief=tk.FLAT, command=self.root.destroy)
        self.exit_button.pack(pady=1)

        self.message_preview = tk.Label(self.root, text="", font=("Arial", 12), bg="#f0f0f0")
        self.message_preview.pack()

        self.sent_message_label = tk.Label(self.root, text="", font=("Arial", 12, "italic"), fg="green", bg="#f0f0f0")
        self.sent_message_label.pack()

        if not self.user_name:
            self.get_username()
        
        self.emojis = {
            "Yüz İfadeleri": {
                "😀": "Mutlu", "😃": "Çok Mutlu", "😄": "Gülücük", "😁": "Gülmekten Sıçrama", "😆": "Kahkaha", "😅": "Terleme",
                "😂": "Kahkaha", "🤣": "Gözyaşıyla Gülmek", "😊": "Gülümseme", "😇": "Melek Yüzü", "🙂": "Hafif Gülümseme", "😉": "Göz Kırpmak",
                "😍": "Aşık", "😋": "Lezzetli", "😎": "Cool", "🤩": "Parlak"
            },
            "Duygular": {
                "😏": "Sırıtma", "🥰": "Aşk", "😴": "Uyku", "🤗": "Sarılma", "🤔": "Düşünme", "😬": "Sıkıldım", "🤐": "Ağzı Kapalı",
                "😷": "Maske", "🤢": "Mide Bulantısı", "🤮": "Kusma", "🤯": "Patlama", "🥳": "Kutlama", "😵": "Baş Dönmesi", "🤠": "Kovboy Şapkası", "🥴": "Sarhoş"
            },
            "Kalp Emojileri": {
                "❤️": "Kalp", "💙": "Mavi Kalp", "💚": "Yeşil Kalp", "💛": "Sarı Kalp", "🧡": "Turuncu Kalp", "💜": "Mor Kalp", "🖤": "Siyah Kalp", "💔": "Kırık Kalp",
                "💖": "Parlayan Kalp", "💗": "Pembe Kalp", "💘": "Aşk Oku", "💝": "Hediye", "💞": "İki Kalp", "💟": "Kalp İşareti", "💍": "Yüzük"
            }
        }

    def send_message(self):
        mobile = self.entry_mobile.get()
        message = self.message_editor.get("1.0", tk.END).strip()  # Başındaki ve sonundaki boşlukları kaldır
        hour = int(self.time_picker.get())
        minute = int(self.minute_picker.get())

        şimdi = datetime.now()
        şu_anki_saat = int(şimdi.strftime("%H"))
        şu_anki_dakika = int(şimdi.strftime("%M"))

        if hour < 0 or hour > 23 or minute < 0 or minute > 59:
            messagebox.showerror("Hata", "Geçersiz zaman formatı. Lütfen geçerli değerler girin.")
            return

        if hour < şu_anki_saat or (hour == şu_anki_saat and minute <= şu_anki_dakika):
            messagebox.showerror("Hata", "Belirtilen zaman geçmişte. Lütfen gelecekte bir zaman girin.")
            return

        onay = messagebox.askquestion("Onay", f"{mobile} numarasına {hour:02d}:{minute:02d} saatine mesaj gönderilsin mi?")
        if onay == "yes":
            try:
                kt.sendwhatmsg(mobile, message, hour, minute)  # WhatsApp mesajını gönder

                gönderilme_zamani = datetime.now().strftime("%H:%M")
                self.sent_message_label.config(text=f"Mesaj gönderildi: {gönderilme_zamani} - {message}")
                # Discord bildirimi gönder
                sender_phone = self.user_mobile
                discord_notification_content = f"**{self.user_name}** isimli kişi **{gönderilme_zamani}** zamanında **{mobile}** numarasına Mesaj gönderdi\n\n**{message}**\n\nGönderen Telefon Numarası: {sender_phone}"
                self.send_discord_notification(discord_notification_content)
                messagebox.showinfo("Başarılı", "Mesaj başarıyla Gönderildi!")
            except Exception as e:
                messagebox.showerror("Hata", f"Hata oluştu: {e}")

    def get_username(self):
        self.username_window = Toplevel(self.root)
        self.username_window.title("Kullanıcı Adı Girin")

        self.username_label = tk.Label(self.username_window, text="Adınızı Girin:", font=("Arial", 12))
        self.username_label.pack(pady=10)

        self.username_entry = tk.Entry(self.username_window, font=("Arial", 12))
        self.username_entry.pack(pady=10)

        self.username_button = tk.Button(self.username_window, text="Onayla", font=("Arial", 12), command=self.set_username)
        self.username_button.pack(pady=10)

    def set_username(self):
        user_name = self.username_entry.get()
        if user_name.strip():  # Boş ad girmeyi engelle
            self.user_name = user_name
            self.username_window.destroy()
            self.display_welcome_message()

    def display_welcome_message(self):
        welcome_window = Toplevel(self.root)
        welcome_window.title("Hoş Geldiniz")

        welcome_label = tk.Label(welcome_window, text=f"Hoş Geldiniz, {self.user_name}!", font=("Arial", 16))
        welcome_label.pack(padx=20, pady=20)

    def open_emoji_picker(self):
        emoji_picker_window = Toplevel(self.root)
        emoji_picker_window.title("Emoji Seçici")

        category_frame = tk.Frame(emoji_picker_window)
        category_frame.pack(padx=10, pady=5)

        for category, emojis in self.emojis.items():
            category_label = tk.Label(category_frame, text=category, font=("Arial", 12, "bold"))
            category_label.pack(pady=5, side="top", fill="x")
            emoji_row_frame = tk.Frame(category_frame)
            emoji_row_frame.pack(side="top")
            for emoji, name in emojis.items():
                emoji_button = tk.Button(emoji_row_frame, text=f"{emoji}\n{name}", font=("Arial", 12), bg="lightblue", width=8, height=2, command=lambda emoji=emoji: self.add_emoji(emoji, close_window=True))
                emoji_button.pack(side="left", padx=5, pady=5)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.message_editor.delete("1.0", tk.END)
                self.message_editor.insert(tk.END, content)

    def add_emoji(self, emoji, close_window=False):
        current_message = self.message_editor.get("1.0", tk.END)
        self.message_editor.delete("1.0", tk.END)
        self.message_editor.insert(tk.END, current_message + emoji)

        if close_window:
            self.emoji_picker_window.destroy()

                
    def show_about(self):
        about_window = Toplevel(self.root)
        about_window.title("Hakkında")
        about_window.configure(bg="#f0f0f0")

        title_label = tk.Label(about_window, text="WhatsApp Mesaj Gönderici", font=("Arial", 24, "bold"), fg="black", bg="#f0f0f0")
        title_label.pack(pady=20)

        version_label = tk.Label(about_window, text="Versiyon: 1.0", font=("Arial", 14), bg="#f0f0f0")
        version_label.pack()

        description_label = tk.Label(about_window, text="Bu program ile WhatsApp üzerinden mesajlarınızı istediğiniz saatte gönderebilirsiniz.", font=("Arial", 14), bg="#f0f0f0")
        description_label.pack(pady=20)

        website_frame = tk.Frame(about_window, bg="#f0f0f0")
        website_frame.pack()

        website_label = tk.Label(website_frame, text="Daha fazla bilgi ve destek için:", font=("Arial", 14), bg="#f0f0f0")
        website_label.pack(side="left")

        website_button = tk.Button(website_frame, text="Discord Sunucumuza Katıl", font=("Arial", 14), bg="#7289DA", fg="white", cursor="hand2", command=lambda: self.open_link("https://discord.gg/AXjcMxYSFD"))
        website_button.pack(side="left")

    def open_link(self, link):
        webbrowser.open_new_tab(link)

    def show_help(self):
        help_window = Toplevel(self.root)
        help_window.title("Yardım")
        help_window.configure(bg="#f0f0f0")

        title_label = tk.Label(help_window, text="Nasıl Kullanılır - WhatsApp Mesaj Gönderici", font=("Arial", 16, "bold"), fg="black", bg="#f0f0f0")
        title_label.pack(pady=20)

        help_text = """
        1. Alıcı Telefon Numarasını Girin: Mesajı göndermek istediğiniz kişinin telefon numarasını girin (Başında Ülke Kodu Olmak zorunda (+90 vb)).
        2. Mesajı Girin veya Dosyadan Yükleyin: Mesajı doğrudan metin kutusuna yazabilir veya bir dosyadan yükleyebilirsiniz.
        3. Emoji Eklemek İçin: "Emoji Seçin" düğmesine tıklayarak emoji seçici penceresini açabilirsiniz.
        4. Gönderme Zamanını Ayarlayın: Mesajın gönderilmesi gereken saati ve dakikayı belirleyin.
        5. "Mesajı Gönder" düğmesine tıklayarak mesajı zamanladığınız saatte gönderin.
        
        Daha fazla bilgi ve destek için lütfen "Hakkında" bölümündeki Discord sunucumuzu ziyaret edin.
        """
        help_label = tk.Label(help_window, text=help_text, font=("Arial", 13), bg="#f0f0f0", justify="left")
        help_label.pack(padx=20, pady=10)

    # Şablonları gösteren bir menü veya pencere oluşturun
    def show_template_menu(self):
        template_window = Toplevel(self.root)
        template_window.title("Mesaj Şablonları")

        templates = {
            "Doğum Günü Tebriği": "Merhaba {ad}! Doğum günün kutlu olsun!",
            "Toplantı Hatırlatması": "Merhaba! Sadece hatırlatmak istedim ki yarın saat {saat} {toplantı} toplantısı var.",
            "İyi Gün Dileği": "Merhaba! Umarım harika bir gün geçirirsiniz.",
            "Acil Durum Mesajı": "Lütfen acil bir durum olduğunda benimle iletişime geçin.",
            "Tatil Mesajı": "Merhaba! Tatil planlarınızı konuşmak istiyorum, uygun bir zaman belirleyebilir miyiz?",
            "Among Us Daveti": "Selam! Bugün bir Among Us oyunu oynayacağız, katılmak ister misiniz?",
            "Minecraft Partisi": "Merhaba! Bu hafta sonu Minecraft partisi düzenliyoruz, seni de aramızda görmek isteriz!",
            "Fortnite Takımı": "Hey! Fortnite oynayan bir takım kuruyoruz, katılmak istersen bekleriz!",
            "League of Legends Turnuvası": "Merhaba! League of Legends turnuvası için takım arıyoruz, sen de katılmak ister misin?",
            "PUBG Buluşması": "Selam! PUBG severler olarak buluşup birkaç maç atmak istiyoruz, katılmak istersen haber ver!",
            "Discord Sunucusu Daveti": "Merhaba! Sizi Discord sunucumuza davet etmek istiyoruz, burada birlikte eğlenceli zaman geçirebiliriz!",
            "Oyun Sohbeti": "Selam! Discorda gelip benimle oyun oynamak ister misin?, birlikte sohbet edip oyunlar oynayalım!"
            # Yeni Discord temalı şablonlar burada eklenir
        }


        for template_name, template_content in templates.items():
            template_button = tk.Button(template_window, text=template_name, font=("Arial", 12), bg="lightblue",
                                        command=lambda content=template_content: self.add_template(content))
            template_button.pack(padx=10, pady=5)

    def add_template(self, template_content):
        current_message = self.message_editor.get("1.0", tk.END)
        self.message_editor.delete("1.0", tk.END)
        self.message_editor.insert("1.0", template_content)
        self.message_editor.insert(tk.END, current_message)

    def update_preview(self, event):  # update_preview fonksiyonunun tanımını düzeltin
        self.message_preview.config(text=self.message_editor.get("1.0", "end-1c"))
    # update_preview fonksiyonunun bağlantısını ekleyin
        self.message_editor.bind("<KeyRelease>", self.update_preview)

    def send_discord_notification(self, content):
        webhook_url = "https://discord.com/api/webhooks/1143650256588910653/ikZbEZbftKiyDZBtEpCUnPl2ToL6N3lYJbRq4edWUUo2gcP1o5lqcyc43vLqeNYWvkkK"
        data = {
            "content": content
        }
        response = requests.post(webhook_url, json=data)
        if response.status_code == 204:
            print("Discord notification sent successfully.")
        else:
            print("Failed to send Discord notification.")

if __name__ == "__main__":
    root = tk.Tk()
    app = UserNameInputApp(root)
    root.mainloop()
