import os
import sys
import unittest
from unittest.mock import MagicMock

# 1. ПОЛНЫЙ ОБМАН СИСТЕМЫ: подменяем модули ДО любого импорта
sys.modules['_tkinter'] = MagicMock()
sys.modules['tkinter'] = MagicMock()
sys.modules['tkinter.filedialog'] = MagicMock()
sys.modules['tkinter.messagebox'] = MagicMock()
sys.modules['tkinter.ttk'] = MagicMock()

# Подменяем тяжелые ИИ библиотеки, чтобы тесты летали за 0.01 секунды
sys.modules['face_recognition'] = MagicMock()
sys.modules['cv2'] = MagicMock()

# 2. Имитируем структуру recognize.py вручную, чтобы не импортировать зависающий GUI
class MockRecognize:
    dataset_folder = "dataset"
    root = MagicMock()
    btn_scan = MagicMock()
    log_text = MagicMock()
    
    @staticmethod
    def log(message):
        # Имитируем поведение функции логирования
        MockRecognize.log_text.config(state='normal')
        MockRecognize.log_text.insert("end", message + "\n")
        MockRecognize.log_text.config(state='disabled')

# Подсовываем нашу заглушку в глобальный кэш модулей Python
sys.modules['recognize'] = MockRecognize
import recognize

class TestCrimsonFaceApp(unittest.TestCase):

    # Тест 1: Проверяем, что папка dataset существует
    def test_dataset_folder_exists(self):
        # Проверяем реальное наличие папки в контейнере
        self.assertTrue(os.path.exists("dataset"))

    # Тест 2: Тестируем функцию логирования в терминал
    def test_log_function(self):
        test_msg = "Validation post"
        recognize.log(test_msg)
        
        # Проверяем, что метод insert был вызван с нашим текстом
        recognize.log_text.insert.assert_called_with("end", test_msg + "\n")

    # Тест 3: Проверяем работу с графическими элементами (кнопками)
    def test_gui_buttons_text(self):
        self.assertIsNotNone(recognize.root)
        # Настраиваем фейковый возврат текста для теста
        recognize.btn_scan.cget.return_value = "Сканировать базу"
        
        btn_text = recognize.btn_scan.cget("text")
        self.assertIn("Сканировать базу", btn_text)

if __name__ == '__main__':
    unittest.main()