import cv2
import os
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser  # Импортируем для работы со ссылкой

# ---------------------------------------------------------
# ЦВЕТОВАЯ ПАЛИТРА (Стиль "Ruby Crimson Noir") 
# ---------------------------------------------------------
BG_COLOR = "#1a080a"       
FG_COLOR = "#f5e6e8"       
BTN_COLOR = "#4a121a"       
BTN_ACTIVE = "#801f2d"     
LOG_BG = "#120405"         
LOG_FG = "#ffb3ba"         
TEXT_MUTED = "#a67c82"     

class ImageFilterApp:
    def __init__(self, root):
        self.root = root
        # Убрали скобочки и текст из названия окна
        self.root.title("Фильтрация изображений ИИ")
        self.root.geometry("550x540")  # Немного увеличили высоту для подвала
        self.root.configure(bg=BG_COLOR)

        # Загружаем встроенный в OpenCV ультра-легкий шаблон для поиска лиц
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        self.create_gui()

    def log(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')

    def open_github(self, event):
        """Открывает браузер со ссылкой на GitHub"""
        webbrowser.open("https://github.com/Meminttaa")

    def create_gui(self):
        # Заголовок
        tk.Label(self.root, text="IMAGE FILTER & TEMPLATE AI", font=("Arial", 14, "bold"), bg=BG_COLOR, fg="#d9384f").pack(pady=15)

        # Кнопка загрузки
        self.btn_process = tk.Button(self.root, text="📥 Загрузить картинку для анализа", bg=BTN_COLOR, fg=FG_COLOR, 
                                     font=("Arial", 11, "bold"), relief="flat", activebackground=BTN_ACTIVE, 
                                     activeforeground=FG_COLOR, command=self.process_image)
        self.btn_process.pack(pady=10)

        # Терминал логов
        tk.Label(self.root, text="Терминал анализа фильтров:", bg=BG_COLOR, fg=TEXT_MUTED, font=("Arial", 10)).pack(anchor="w", padx=25)
        self.log_text = tk.Text(self.root, height=14, width=60, state='disabled', bg=LOG_BG, fg=LOG_FG, font=("Consolas", 10), relief="flat", padx=10, pady=10)
        self.log_text.pack(padx=25, pady=5)

        self.log("Система фильтрации готова к работе. Ожидание файла...")

        # --- СЕКЦИЯ РАЗРАБОТЧИКА (ПОДВАЛ) ---
        github_label = tk.Label(self.root, text="💻 Разработано: github.com/Meminttaa", bg=BG_COLOR, fg=TEXT_MUTED, 
                                font=("Arial", 10, "underline"), cursor="hand2", activeforeground="#d9384f")
        github_label.pack(side=tk.BOTTOM, pady=15)
        github_label.bind("<Button-1>", self.open_github)

    def process_image(self):
        file_path = filedialog.askopenfilename(
            title="Выберите изображение",
            filetypes=[("Изображения", "*.jpg *.jpeg *.png")]
        )
        if not file_path:
            return

        img = cv2.imread(file_path)
        if img is None:
            self.log("[ОШИБКА] Не удалось прочитать файл.")
            return

        self.log(f"\n=== ЗАПУСК АНАЛИЗА: {os.path.basename(file_path)} ===")

        # 1. ФИЛЬТР РАЗМЕРА
        height, width, _ = img.shape
        self.log(f"[1] Фильтр размера: Разрешение -> {width}x{height}px")
        
        if width < 150 or height < 150:
            self.log("[-] ПРЕДУПРЕЖДЕНИЕ: Картинка слишком мала! Шаблон может не распознаться.")
            messagebox.showwarning("Фильтр размера", f"Внимание! Картинка слишком маленькая ({width}x{height}px).\nРекомендуется разрешение от 150x150px.")
        else:
            self.log("[+] Фильтр размера: Проверка пройдена успешно.")

        # 2. ФИЛЬТР ЦВЕТА
        b, g, r = cv2.split(img)
        if np.array_equal(b, g) and np.array_equal(g, r):
            color_status = "Черно-белое (Оттенки серого) ⚪"
        else:
            color_status = "Цветное (Палитра RGB/BGR) 🔴"
        self.log(f"[2] Фильтр цвета: Определен тип -> {color_status}")

        # 3. ФИЛЬТР ШАБЛОНА (Поиск биометрических контуров лица)
        self.log("[3] Фильтр шаблона: Поиск ключевых контуров лица...")
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) > 0:
            self.log(f"[+] Шаблон найден! Обнаружено лиц на фото: {len(faces)}")
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (56, 56, 217), 2)
            
            self.log("[Система] Результат выведен на экран.")
            cv2.imshow("Фильтр шаблона ИИ - Результат", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            self.log("[-] Шаблон не совпал: Лица на изображении не обнаружены.")
            messagebox.showinfo("Фильтр шаблона", "Анализ завершен: Ключевой биометрический шаблон лица на фото не найден.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageFilterApp(root)
    root.mainloop()