import tkinter as tk
from tkinter import messagebox
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email():
    try:
        # E-posta gönderim için gerekli bilgileri al
        sender_email = sender_email_entry.get()
        sender_password = sender_password_entry.get()
        receiver_email = receiver_email_entry.get()
        subject = subject_entry.get()
        message = message_text.get("1.0", "end")

        # E-posta sunucusu ve bağlantı ayarları
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        # Bağlantı oluştur
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)

        # E-posta içeriği oluştur
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        # E-postayı gönder
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        # Başarılı mesajı göster
        messagebox.showinfo("Başarılı", "E-posta gönderildi!")

    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu:\n{e}")

# Tkinter arayüzünü oluştur
app = tk.Tk()
app.title("E-posta Gönderme Uygulaması")

sender_label = tk.Label(app, text="Gönderen E-posta:")
sender_label.pack()
sender_email_entry = tk.Entry(app)
sender_email_entry.pack()

sender_password_label = tk.Label(app, text="Gönderen Parola:")
sender_password_label.pack()
sender_password_entry = tk.Entry(app, show="*")
sender_password_entry.pack()

receiver_label = tk.Label(app, text="Alıcı E-posta:")
receiver_label.pack()
receiver_email_entry = tk.Entry(app)
receiver_email_entry.pack()

subject_label = tk.Label(app, text="Konu:")
subject_label.pack()
subject_entry = tk.Entry(app)
subject_entry.pack()

message_label = tk.Label(app, text="Mesaj:")
message_label.pack()
message_text = tk.Text(app, height=10, width=40)
message_text.pack()

send_button = tk.Button(app, text="E-posta Gönder", command=send_email)
send_button.pack()

app.mainloop()

'''sildiklerim


        #kalın yazma düğmesi
        self.bold_button = tk.Button(button_frame, text="B", font=("Arial", 12, "bold"), bg="#FFA733", fg="black", command=self.toggle_bold)
        self.bold_button.pack(side="left", padx=5, pady=5)
        self.bold_button.bind("<Enter>", on_hover)  # Fare düğmenin üzerine geldiğinde
        self.bold_button.bind("<Leave>", on_leave)  # Fare düğmenin üzerinden ayrıldığında
        #eğik yazma düğmesi
        self.italic_button = tk.Button(button_frame, text="I", font=("Arial", 12, "italic"), bg="#FFA733", fg="black", command=self.toggle_italic)
        self.italic_button.pack(side="left", padx=5, pady=5)
        self.italic_button.bind("<Enter>", on_hover)
        self.italic_button.bind("<Leave>", on_leave)
        #altı çizili yazma düğmesi
        self.underline_button = tk.Button(button_frame, text="U", font=("Arial", 12, "underline"), bg="#FFA733", fg="black", command=self.toggle_underline)
        self.underline_button.pack(side="left", padx=5, pady=5)
        self.underline_button.bind("<Enter>", on_hover)
        self.underline_button.bind("<Leave>", on_leave)
        #renk seçme düğmesi
        self.color_button = tk.Button(button_frame, text="Renk Seç", font=("Arial", 12), command=self.choose_color, bg="#FF5733", fg="white")
        self.color_button.pack(side="left", padx=5)
        self.color_button.bind("<Enter>", on_hover)
        self.color_button.bind("<Leave>", on_leave)

    def toggle_bold(self):
        self.message_editor.tag_configure("bold", font=("Arial", 12, "bold"))
        self.toggle_text_tag("bold")

    def toggle_italic(self):
        self.message_editor.tag_configure("italic", font=("Arial", 12, "italic"))
        self.toggle_text_tag("italic")

    def toggle_underline(self):
        self.message_editor.tag_configure("underline", font=("Arial", 12, "underline"))
        self.toggle_text_tag("underline")

    def toggle_text_tag(self, tag_name):
        sel_start = self.message_editor.index(tk.SEL_FIRST)
        sel_end = self.message_editor.index(tk.SEL_LAST)
        current_tags = self.message_editor.tag_names(sel_start)
        if tag_name in current_tags:
            self.message_editor.tag_remove(tag_name, sel_start, sel_end)
        else:
            self.message_editor.tag_add(tag_name, sel_start, sel_end)

    def choose_color(self):
        color = askcolor()[1]  # Renk seçici penceresini aç ve seçilen rengi al
        self.message_editor.tag_configure("color", foreground=color)
        self.toggle_text_tag("color")
'''