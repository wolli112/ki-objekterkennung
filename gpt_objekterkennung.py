'''
KI-Objekterkennung im Vollbildmodus (Kiosk)
https://github.com/wolli112/ki-objekterkennung

MIT License

Copyright (c) 2024 wolli112

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
__version__ = '0.1'
__author__ = 'wolli112'

from openaiapikey import OPENAI_API_KEY
import tkinter as tk
import base64
import requests
from PIL import ImageTk, Image
from take_photo import capture_photo
import RPi.GPIO as GPIO
import time

# GPIO-Pins definieren
GPIO.setmode(GPIO.BCM)

# GPIO als Eingang mit Pull-Down konfigurieren
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Pfad zum Bild
bild_pfad = "image.jpeg"

# Prompt
text_lang = "Beschreibe das Objekt in der Bildmitte kurz. Hintergrund muss nicht beschrieben werden, auch der Würfel auf dem es steht ist nicht relevant."
text_kurz = "Beschreibe das Objekt in der Bildmitte mit einem Wort. Hintergrund muss nicht beschrieben werden."

# Schriftart für Antwort
text_font = ('Arial', 16)

# Funktion zum Codieren des Bildes
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Funktion zum Upload zu GTP und Rückgabe der Antwort
def upload_gpt(textprompt):
    
    antwort_text = tk.Text(root, height=5, width=80, font=text_font, wrap=tk.WORD)
    antwort_text.grid(row=6, column=0, columnspan=5, pady=10)
    antwort_text.insert(tk.END, "Anfrage wird übermittelt")
    antwort_text.tag_configure('color', foreground="red")
    antwort_text.tag_add('color', '1.0', 'end')
    antwort_text.tag_configure('center', justify='center')
    antwort_text.tag_add('center', '1.0', 'end')
    root.update()
    
    base64_image = encode_image(bild_pfad)

    headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    payload = {
      "model": "gpt-4o",
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": textprompt
            },
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
              }
            }
          ]
        }
      ],
      "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    
    json_response = response.json()
    content = json_response['choices'][0]['message']['content']
    
    antwort_text = tk.Text(root, height=5, width=80, font=text_font, wrap=tk.WORD)
    antwort_text.grid(row=6, column=0, columnspan=5, pady=10)
    antwort_text.insert(tk.END, content)
    antwort_text.tag_configure('color', foreground="black")
    antwort_text.tag_add('color', '1.0', 'end') 
    antwort_text.tag_configure('center', justify='center')
    antwort_text.tag_add('center', '1.0', 'end')
    root.update()

# Funktion zum Bild erstellen
def bild_erstellen():
    
    antwort_text = tk.Text(root, height=5, width=80, font=text_font)
    antwort_text.grid(row=6, column=0, columnspan=5, pady=10)
    antwort_text.insert(tk.END, "")
    root.update()

    capture_photo("image.jpeg")
    img = Image.open(bild_pfad)
    
    # Konvertieren des PIL-Bild in ein tkinter-Bild
    img_tk = ImageTk.PhotoImage(img)

    # Zeigt das Bild in einem Label im Hauptfenster an
    bild_label = tk.Label(root)
    bild_label.grid(row=5, column=0, columnspan=5, pady=5)
    bild_label.config(image=img_tk)
    bild_label.image = img_tk
    root.update()

# Funktion für Antwort Auswahl
def abfrage():
    global text
    auswahl = input("Antwort kurz = 1 oder lang = 2 : ")
    if auswahl == "1":
        text = text_kurz
        upload_gpt(text)
    elif auswahl == "2":
        text = text_lang
        upload_gpt(text)
    elif auswahl == "3":
        bild_erstellen()

# Erstellen des Hauptfenster
root = tk.Tk()
root.configure(bg="white")
root.title("KI-Objekterkennung mit GPT-4o von wolli112")
w, h = root.winfo_screenwidth(), root.winfo_screenheight() # Fenster mit Menü und groß
root.geometry("%dx%d+0+0" % (w, h)) # Fenster mit Menü und groß
root.wm_attributes("-fullscreen","true") # Fenster im Vollbild
root.overrideredirect(1) # Entfernen der Menüleiste bei Bedarf

# Konfiguration für zentrierte Ausrichtung
root.grid_columnconfigure(0, weight=1)  # Spalte 0 auf zentrierte Ausrichtung einstellen

# Textfeld mit Programmbeschriftung
program_text = tk.Label(root, font=("Arial", 40, "bold"), text="KI-Objekterkennung mit GPT-4o von wolli112", bg="white")
program_text.grid(row=1, column=0, columnspan=5, pady=10)
root.update()

# Aktualisieren das Hauptfenster, um die Größe an den Inhalt anzupassen
root.update_idletasks()

# Hauptprogramm
try:
    while True:
        # GPIO-Pins abfragen und entsprechende Funktionen aufrufen
        if GPIO.input(26) == GPIO.HIGH:
            bild_erstellen()
            time.sleep(1)
        if GPIO.input(22) == GPIO.HIGH:
            text = text_lang
            upload_gpt(text)
            time.sleep(1)
        if GPIO.input(27) == GPIO.HIGH:
            text = text_kurz
            upload_gpt(text)
            time.sleep(1)

        time.sleep(0.5)  # Kurze Pause, um CPU-Last zu reduzieren

except KeyboardInterrupt:
    GPIO.cleanup()  # Aufräumen, wenn das Programm beendet wird

# Hauptschleife fürs Fenster
root.mainloop()


