# 🤖 AURA PRO - WhatsApp Bot

Bu proje, WhatsApp üzerinden otomatik mesajlaşma, zamanlama ve kişi yönetimi sağlayan gelişmiş bir bot uygulamasıdır.

## 🚀 Özellikler

- **Toplu Mesaj Gönderimi**: Kişilere veya gruplara otomatik mesaj gönderin.
- **Zamanlayıcı**: Mesajları ileri bir tarih ve saat için planlayın.
- **Kişi Yönetimi**: Excel/CSV ile toplu kişi ekleyin ve düzenleyin.
- **Modern Arayüz**: Koyu/Açık tema seçenekleri ve özelleştirilebilir renkler.
- **Raporlama**: Gönderim geçmişini Excel olarak dışa aktarın.

## 🛠 Kurulum

1.  Python 3.x'in kurulu olduğundan emin olun.
2.  Gerekli kütüphaneleri yükleyin:
    ```bash
    pip install customtkinter selenium pandas webdriver-manager phonenumbers pillow
    ```

## 📦 .exe Oluşturma

Projeyi çalıştırılabilir `.exe` dosyasına dönüştürmek için aşağıdaki PyInstaller komutunu kullanın:

```bash
pyinstaller --noconfirm --onefile --windowed --icon "icon.ico" --name "AuraBot" --collect-all customtkinter main.py
```

## 📄 Lisans

Bu proje MIT lisansı altında dağıtılmaktadır.
