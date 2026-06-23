import cv2
import os
import numpy as np
import time

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

# Имитируем размеры экрана смартфона
Window.size = (450, 750)

# ---------------------------------------------------------
# ЦВЕТОВАЯ ПАЛИТРА (Стиль "Ruby Crimson Noir")
# ---------------------------------------------------------
BG_COLOR = get_color_from_hex("#1a080a")       
BTN_COLOR = get_color_from_hex("#4a121a")       
BTN_ACTIVE = get_color_from_hex("#801f2d")     
LOG_BG = get_color_from_hex("#120405")         
LOG_FG = get_color_from_hex("#ffb3ba")         
TEXT_MUTED = get_color_from_hex("#a67c82")     
ACCENT_RED = get_color_from_hex("#d9384f")     

class MobileFilterApp(App):
    def build(self):
        self.title = "Фильтрация изображений ИИ"
        
        # Загружаем встроенный каскад Хаара
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)

        # Главный контейнер (Мобильный Layout)
        main_layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        # Делаем фон приложения темно-бордовым
        with main_layout.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(rgba=BG_COLOR)
            self.rect = Rectangle(size=Window.size, pos=main_layout.pos)
        main_layout.bind(pos=self._update_rect, size=self._update_rect)

        # Шапка
        title = Label(text="IMAGE FILTER & TEMPLATE AI", font_size='18sp', bold=True, color=ACCENT_RED, size_hint_y=None, height=40)
        main_layout.add_widget(title)

        # Кнопка загрузки
        btn_upload = Button(
            text="📥 Загрузить картинку для анализа",
            background_normal='',
            background_color=BTN_COLOR,
            font_size='14sp',
            bold=True,
            size_hint_y=None,
            height=55
        )
        btn_upload.bind(on_press=self.open_file_chooser)
        main_layout.add_widget(btn_upload)

        # Логи
        main_layout.add_widget(Label(text="Терминал анализа фильтров:", color=TEXT_MUTED, font_size='12sp', size_hint_y=None, height=20, halign='left', text_size=(420, None)))
        
        scroll = ScrollView(size_hint=(1, None), height=180)
        self.log_text = Label(text="Система фильтрации готова. Ожидание файла...\n", color=LOG_FG, font_name="RobotoMono-Regular", font_size='11sp', size_hint_y=None, halign='left', valign='top')
        self.log_text.bind(texture_size=self.log_text.setter('size'))
        scroll.add_widget(self.log_text)
        
        # Контейнер для терминала логов
        log_container = BoxLayout(orientation='vertical', size_hint=(1, None), height=190, padding=5)
        with log_container.canvas.before:
            Color(rgba=LOG_BG)
            self.log_rect = Rectangle(size=(420, 190), pos=log_container.pos)
        log_container.bind(pos=self._update_log_rect, size=self._update_log_rect)
        log_container.add_widget(scroll)
        main_layout.add_widget(log_container)

        # Экран смартфона для вывода фото
        main_layout.add_widget(Label(text="Экран предпросмотра смартфона:", color=TEXT_MUTED, font_size='12sp', size_hint_y=None, height=20, halign='left', text_size=(420, None)))
        self.result_image = Image(source='', size_hint=(1, 1), allow_stretch=True)
        main_layout.add_widget(self.result_image)

        # Подвал
        github_lbl = Label(text="💻 Разработано: github.com/Meminttaa", color=TEXT_MUTED, font_size='12sp', size_hint_y=None, height=30, underline=True)
        main_layout.add_widget(github_lbl)

        return main_layout

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def _update_log_rect(self, instance, value):
        self.log_rect.pos = instance.pos
        self.log_rect.size = instance.size

    def logger(self, message):
        self.log_text.text += message + "\n"

    def open_file_chooser(self, instance):
        # На мобильных платформах используется системный диалог. 
        # В Windows Kivy использует встроенный FileChooser, но чтобы не перегружать UI, 
        # мы вызываем стандартный пуленепробиваемый проводник Windows через tkinter.
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(filetypes=[("Изображения", "*.jpg *.jpeg *.png *.bmp")])
        if file_path:
            self.process_image(file_path)

    def process_image(self, file_path):
        if self.face_cascade.empty():
            self.logger("[ОШИБКА] Модель ИИ (каскад) не найдена!")
            return

        img = cv2.imread(file_path)
        if img is None:
            self.logger("[ОШИБКА] Не удалось прочитать файл.")
            return

        self.logger(f"\n=== ЗАПУСК АНАЛИЗА: {os.path.basename(file_path)} ===")

        # 1. ФИЛЬТР РАЗМЕРА
        shape_data = img.shape
        height, width = shape_data[0], shape_data[1]
        channels = shape_data[2] if len(shape_data) > 2 else 1
        
        self.logger(f"[1] Фильтр размера: {width}x{height}px (Каналов: {channels})")
        if width < 150 or height < 150:
            self.logger("[-] ПРЕДУПРЕЖДЕНИЕ: Картинка слишком мала!")

        # 2. ФИЛЬТР ЦВЕТА
        if channels == 1:
            color_status = "Черно-белое (Оттенки серого) ⚪"
        elif channels == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            b, g, r = cv2.split(img)
            color_status = "Черно-белое ⚪" if np.array_equal(b, g) and np.array_equal(g, r) else "Цветное (RGBA) 🔴"
        else:
            b, g, r = cv2.split(img)
            color_status = "Черно-белое ⚪" if np.array_equal(b, g) and np.array_equal(g, r) else "Цветное (RGB/BGR) 🔴"
        self.logger(f"[2] Фильтр цвета: {color_status}")

        # 3. ФИЛЬТР ШАБЛОНА
        self.logger("[3] Фильтр шаблона: Поиск контуров...")
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if channels > 1 else img.copy()
        faces = self.face_cascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) > 0:
            self.logger(f"[+] Шаблон найден! Лиц на фото: {len(faces)}")
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (217, 56, 56), 3)
            
            # Сохраняем результат во временный кэш
            temp_output = "kivy_mobile_result.jpg"
            cv2.imwrite(temp_output, img)
            
            # Обновляем картинку и сбрасываем внутренний кэш Kivy через reload()
            self.result_image.source = temp_output
            self.result_image.reload()
            self.logger("[Система] Результат выведен на экран.")
        else:
            self.logger("[-] Шаблон не совпал: Лица не обнаружены.")
            self.result_image.source = ''

if __name__ == '__main__':
    MobileFilterApp().run()