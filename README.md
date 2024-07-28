# KI-Objekterkennung im Vollbildmodus (Kiosk)
Mit diesem Skript können Objekte von der KI erkannt werden und anschließend beschrieben werden.

Die Bedienung erfolgt komplett über drei Taster.

Geeignet ist hier ganz gut ein Raspberry Pi 4 oder jedes andere System.

Verwendet wird die API von OpenAI mit GPT-4o.

### Zum Betrieb wird ein OpenAI APi Key benötigt.

In dem Pfad in dem die gpt_objekterkennung.py liegt, muss auch die openapikey.py und take_photo.py liegen.

![IMG_9588](https://github.com/user-attachments/assets/1ea4aa72-7324-42c9-ab1b-6c4589f07652)

![IMG_9583](https://github.com/user-attachments/assets/9f1b6546-535f-44d2-8db1-e64e5495f67a)

![IMG_9586](https://github.com/user-attachments/assets/f8cf8634-a576-4a20-ac1d-d40cc66cc510)

![Ohne Titel](https://github.com/user-attachments/assets/3407b749-6260-4a03-9e59-2c4b4edeaa5a)

### GPIO PIN`s

Bild erstellen = GPIO 26 = PIN37

Kurze Antwort = GPIO 27 = PIN13

Lange Antwort = GPIO 22 = PIN15

3,3V = PIN17


Das Vollbildprogramm kann nur beendet werden wenn man den laufenden Prozess beendet.
