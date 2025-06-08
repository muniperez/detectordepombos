# Testes unitários para o projeto
from unittest.mock import patch, MagicMock
import main

# Testa a captura de imagens
def test_capture_image_success(tmp_path):
    # Utiliza mocking da livraria de captura de imagens
    with patch('main.cv2.VideoCapture') as mock_video:
        mock_cap = MagicMock()
        mock_video.return_value = mock_cap
        mock_cap.read.return_value = (True, 'frame')
        with patch('main.cv2.imwrite') as mock_imwrite:
            filename = tmp_path / "test.jpg"
            result = main.capture_image(camera_index=0, filename=str(filename))
            assert result == str(filename)
            mock_imwrite.assert_called_once()

# Testa a captura de imagens com falha
def test_capture_image_failure():
    with patch('main.cv2.VideoCapture') as mock_video:
        mock_cap = MagicMock()
        mock_video.return_value = mock_cap
        mock_cap.read.return_value = (False, None)
        result = main.capture_image()
        assert result is None

# Testa a detecção do pombo com sucesso
def test_detect_pigeon_found():
    mock_model = MagicMock()
    mock_result = MagicMock()
    mock_result.names.values.return_value = ['cat', 'Pigeon', 'dog']
    mock_model.return_value = [mock_result]
    assert main.detect_bird('some_image.jpg', mock_model) is True

# Testa a detecção de objeto que não é pombo
def test_detect_pigeon_not_found():
    mock_model = MagicMock()
    mock_result = MagicMock()
    mock_result.names.values.return_value = ['cat', 'dog']
    mock_model.return_value = [mock_result]
    assert main.detect_bird('some_image.jpg', mock_model) is False

# Testa se o som é tocado corretamente
def test_play_tone():
    with patch('main.sa.play_buffer') as mock_play_buffer:
        mock_play_obj = MagicMock()
        mock_play_buffer.return_value = mock_play_obj
        main.play_tone(frequency=1400, duration=1.0)
        mock_play_buffer.assert_called_once()
        mock_play_obj.wait_done.assert_called_once()

