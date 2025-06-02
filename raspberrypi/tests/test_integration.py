# Testes de integração para o projeto
from unittest.mock import patch, MagicMock, call
import main

# Teste de integração para verificar se o sinal é enviado quando um pombo é detectado
def test_main_detects_pigeon_and_sends_signal(monkeypatch):
    # Mock serial.Serial
    mock_serial = MagicMock()
    # Simula sinal 'motion_detected'
    mock_serial.readline.side_effect = [b'motion_detected\n', b'']
    monkeypatch.setattr('serial.Serial', lambda *a, **kw: mock_serial)

    # Mock da função capture_image para sempre retornar um nome de arquivo
    monkeypatch.setattr('main.capture_image', lambda *a, **kw: 'test.jpg')

    # Mock modelo YOLO para sempre detectar pombo (pigeon)
    mock_model = MagicMock()
    mock_result = MagicMock()
    mock_result.names.values.return_value = ['pigeon']
    mock_model.__call__.return_value = [mock_result]
    monkeypatch.setattr('main.YOLO', lambda *a, **kw: mock_model)

    # Alteração do main loop para executar só uma vez
    with patch('builtins.__import__', side_effect=ImportError):
        try:
            main.main()
        except Exception:
            pass  # Ignore ImportError to break the loop

    # Verifica que o sinal 'pigeon\n' foi enviado
    mock_serial.write.assert_called_with(b'pigeon\n')

# Teste de integração para verificar se o sinal não é enviado quando nenhum pombo é detectado
def test_main_no_pigeon_no_signal(monkeypatch):
    mock_serial = MagicMock()
    mock_serial.readline.side_effect = [b'motion_detected\n', b'']
    monkeypatch.setattr('serial.Serial', lambda *a, **kw: mock_serial)

    monkeypatch.setattr('main.capture_image', lambda *a, **kw: 'test.jpg')

    # Mock modelo YOLO para não detectar pombo
    mock_model = MagicMock()
    mock_result = MagicMock()
    mock_result.names.values.return_value = ['cat', 'dog']
    mock_model.__call__.return_value = [mock_result]
    monkeypatch.setattr('main.YOLO', lambda *a, **kw: mock_model)

    with patch('builtins.__import__', side_effect=ImportError):
        try:
            main.main()
        except Exception:
            pass

    # Verifica que o sinal 'pigeon\n' não foi enviado
    mock_serial.write.assert_not_called()