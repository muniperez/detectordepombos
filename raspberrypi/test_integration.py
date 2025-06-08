import os
import pytest
from ultralytics import YOLO
from main import detect_bird

@pytest.mark.integration
def test_detect_pigeon_on_real_image():
    # Path to your test image
    image_path = os.path.join("files", "images", "pombo.jpg")
    # Load the YOLO model (will download if not present)
    model = YOLO('yolov8n.pt')
    # Run detection
    result = detect_bird(image_path, model)
    
    assert result is True  # Assert que a imagem contém um pombo (pássaro)

@pytest.mark.integration
def test_detect_pigeon_on_real_image2():
    # Path to your test image
    image_path = os.path.join("files", "images", "pombo2.jpg")
    # Load the YOLO model (will download if not present)
    model = YOLO('yolov8n.pt')
    # Run detection
    result = detect_bird(image_path, model)
    
    assert result is True  # Assert que a imagem contém um pombo (pássaro)

@pytest.mark.integration
def test_detect_not_pigeon_on_real_image():
    # Path to your test image
    image_path = os.path.join("files", "images", "gato.jpg")
    # Load the YOLO model (will download if not present)
    model = YOLO('yolov8n.pt')
    # Run detection
    result = detect_bird(image_path, model)
    
    assert result is False  # Assert que a imagem não contém um pombo (é um gato)

@pytest.mark.integration
def test_detect_not_pigeon_on_real_image2():
    # Path to your test image
    image_path = os.path.join("files", "images", "gato2.jpg")
    # Load the YOLO model (will download if not present)
    model = YOLO('yolov8n.pt')
    # Run detection
    result = detect_bird(image_path, model)
    
    assert result is False  # Assert que a imagem não contém um pombo (é um gato)