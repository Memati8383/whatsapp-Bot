from PIL import Image
import os
import subprocess

# 1. Convert Icon
try:
    img = Image.open("icon.png")
    img.save("icon.ico", format='ICO', sizes=[(256, 256)])
    print("Icon converted successfully.")
except Exception as e:
    print(f"Icon conversion failed: {e}")

# 2. Create README.md
readme_content = """# 🤖 AURA PRO - WhatsApp Bot

Bu proje, WhatsApp üzerinden otomatik mesajlaşma, zamanlama ve kişi yönetimi sağlayan gelişmiş bir bot uygulamasıdır.

## 🚀 Özellikler

*   **Toplu Mesaj Gönderimi**: Kişilere veya gruplara otomatik mesaj gönderin.
*   **Zamanlayıcı**: Mesajları ileri bir tarih ve saat için planlayın.
*   **Kişi Yönetimi**: Excel/CSV ile toplu kişi ekleyin ve düzenleyin.
*   **Modern Arayüz**: Koyu/Açık tema seçenekleri ve özelleştirilebilir renkler.
*   **Raporlama**: Gönderim geçmişini Excel olarak dışa aktarın.

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
"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme_content)
print("README.md created.")

# 3. Build .exe
print("Building .exe...")
try:
    subprocess.run([
        "pyinstaller", 
        "--noconfirm", 
        "--onefile", 
        "--windowed", 
        "--icon", "icon.ico", 
        "--name", "AuraBot", 
        "--collect-all", "customtkinter", 
        "main.py"
    ], check=True)
    print("Build successful.")
except subprocess.CalledProcessError as e:
    print(f"Build failed: {e}")
