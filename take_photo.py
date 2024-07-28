import cv2

def capture_photo(file_path):
    # Öffne die Webcam
    cap = cv2.VideoCapture(0)  # 0 steht für /dev/video0

    # Überprüfen, ob die Kamera erfolgreich geöffnet wurde
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
    # Setze die Auflösung (Beispiel: 640x480)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Warte kurz, um sicherzustellen, dass die Kamera betriebsbereit ist
    cv2.waitKey(2000)

    # Foto aufnehmen
    ret, frame = cap.read()

    # Überprüfen, ob das Foto erfolgreich aufgenommen wurde
    if not ret:
        print("Error: Failed to capture image from webcam.")
        return

    # Bild speichern
    cv2.imwrite(file_path, frame)

    # Kamera freigeben
    cap.release()
    cv2.destroyAllWindows()

