import cv2
import time
import numpy as np
import simpleaudio as sa
from ultralytics import YOLO

# Função para capturar imagem da câmera
def capture_image(camera_index=0, filename='capture.jpg'):
    cap = cv2.VideoCapture(camera_index)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(filename, frame)
    cap.release()
    return filename if ret else None

# Função para detectar pombos na imagem usando YOLOv8
def detect_bird(image_path, model, min_confidence=0.5):
    results = model(image_path)
    for result in results:
        # Verifica cada objeto detectado para analisar o nível de confiança e a classe
        for box in result.boxes:
            cls_id = int(box.cls[0])
            cls_name = result.names[cls_id].lower()
            conf = float(box.conf[0])
            print(f"[DEBUG] Detected: {cls_name}, Confidence: {conf}")
            if 'bird' in cls_name and conf >= min_confidence:
                return True
    return False

# Função para tocar um som em uma frequência específica (Hz)
def play_tone(frequency=1400, duration=1.0, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = np.sin(frequency * 2 * np.pi * t)
    audio = (tone * 32767).astype(np.int16)
    play_obj = sa.play_buffer(audio, 1, 2, sample_rate)
    play_obj.wait_done()

def main():
    model = YOLO('yolov8n.pt')  # Modelo YOLOv8 pré-treinado.
    while True:
        img_path = capture_image()
        if img_path:
            if detect_bird(img_path, model):
                play_tone(1400, duration=1.0)
        time.sleep(5)

if __name__ == '__main__':
    main()