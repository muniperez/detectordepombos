import serial
import cv2
from ultralytics import YOLO

SERIAL_PORT = '/dev/ttyUSB0'  # Porta serial do Arduino.
BAUD_RATE = 9600

# Função para capturar imagem da câmera
def capture_image(camera_index=0, filename='capture.jpg'):
    cap = cv2.VideoCapture(camera_index)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(filename, frame)
    cap.release()
    return filename if ret else None

# Função para detectar pombos na imagem usando YOLOv8
def detect_pigeon(image_path, model):
    results = model(image_path)
    for result in results:
        for cls in result.names.values():
            if 'pigeon' in cls.lower():
                return True
    return False

def main():
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    model = YOLO('yolov8n.pt')  # Modelo YOLOv8 pré-treinado.

    while True:
        line = ser.readline().decode().strip()
        if line == 'motion_detected':
            img_path = capture_image()
            if img_path:
                if detect_pigeon(img_path, model):
                    ser.write(b'pigeon\n')

if __name__ == '__main__':
    main()