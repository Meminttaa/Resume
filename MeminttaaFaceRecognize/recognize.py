import face_recognition
import cv2
import os
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import shutil
import webbrowser # Для открытия ссылки на GitHub
import random     # Для случайных координат в мини-игре

# ---------------------------------------------------------
# ЦВЕТОВАЯ ПАЛИТРА (Стиль "Ruby Crimson Noir")
# ---------------------------------------------------------
BG_COLOR = "#1a080a"       # Глубокий темно-бордовый, почти черный
FG_COLOR = "#f5e6e8"       # Мягкий бело-розовый текст
BTN_SCAN = "#4a121a"       # Темный рубин (для базовых действий)
BTN_UPLOAD = "#801f2d"     # Средний рубин
BTN_REC = "#b32438"        # Яркий рубиновый (главное действие)
BTN_GAME = "#d9384f"       # Акцентный светло-рубиновый для игры
LOG_BG = "#120405"         # Ультра-темный фон для терминала
LOG_FG = "#ffb3ba"         # Нежно-розовый светящийся текст для логов
TEXT_MUTED = "#a67c82"     # Приглушенный цвет для второстепенного текста

# ---------------------------------------------------------
# ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ
# ---------------------------------------------------------
known_faces = []
known_names = []
dataset_folder = "dataset"

if not os.path.exists(dataset_folder):
    os.makedirs(dataset_folder)

# ---------------------------------------------------------
# ФУНКЦИИ ЛОГИКИ ПРОГРАММЫ
# ---------------------------------------------------------
def log(message):
    log_text.config(state='normal')
    log_text.insert(tk.END, message + "\n")
    log_text.see(tk.END)
    log_text.config(state='disabled')

def scan_database_thread():
    btn_scan.config(state=tk.DISABLED)
    btn_recognize.config(state=tk.DISABLED)
    
    global known_faces, known_names
    known_faces.clear()
    known_names.clear()
    
    log("=== НАЧАЛО СКАНИРОВАНИЯ БАЗЫ ДАННЫХ ===")
    
    for person_name in os.listdir(dataset_folder):
        person_folder = os.path.join(dataset_folder, person_name)
        if not os.path.isdir(person_folder):
            continue
            
        log(f"[*] Сканирование папки: {person_name}")
        
        for filename in os.listdir(person_folder):
            if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                path = os.path.join(person_folder, filename)
                
                try:
                    image_bgr = cv2.imread(path)
                    if image_bgr is None:
                        log(f"    [X] Пропуск {filename}: файл поврежден.")
                        continue
                        
                    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
                    encodings = face_recognition.face_encodings(image_rgb)
                    
                    if len(encodings) > 0:
                        known_faces.append(encodings[0])
                        known_names.append(person_name)
                    else:
                        log(f"    [-] Лицо не найдено на {filename}")
                        
                except Exception as e:
                    log(f"    [X] Ошибка с {filename}: {e}")
                    
    log(f"=== ГОТОВО! Загружено {len(known_faces)} лиц. ===")
    log("Теперь вы можете распознавать фото.\n")
    
    btn_scan.config(state=tk.NORMAL)
    btn_recognize.config(state=tk.NORMAL)

def start_scanning():
    threading.Thread(target=scan_database_thread, daemon=True).start()

def upload_to_database():
    messagebox.showinfo(
        "Инструкция по добавлению",
        "Как добавить человека в базу:\n\n"
        "Шаг 1. Сейчас откроется окно — выберите файл с чёткой фотографией лица.\n\n"
        "Шаг 2. Появится следующее окно — напишите имя (например, Meminttaa) или выберите из списка.\n\n"
        "Шаг 3. После добавления обязательно нажмите '1. Сканировать базу', чтобы программа его запомнила!"
    )

    file_path = filedialog.askopenfilename(
        title="Выберите фото для добавления в базу",
        filetypes=[("Изображения", "*.jpg *.jpeg *.png")]
    )
    if not file_path:
        return 
        
    existing_names = [d for d in os.listdir(dataset_folder) if os.path.isdir(os.path.join(dataset_folder, d))]

    dialog = tk.Toplevel(root)
    dialog.title("Выбор профиля")
    dialog.geometry("380x180")
    dialog.configure(bg=BG_COLOR)
    dialog.transient(root) 
    dialog.grab_set()      

    tk.Label(dialog, text="Выберите существующее имя из списка\nили введите совершенно новое:", 
             bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 11), pady=15).pack()

    # Настройка стиля для выпадающего списка под темную тему
    style = ttk.Style()
    style.theme_use('default')
    style.configure("TCombobox", fieldbackground=LOG_BG, background=BTN_SCAN, foreground=FG_COLOR)
    
    combo = ttk.Combobox(dialog, values=existing_names, width=35, font=("Arial", 10), style="TCombobox")
    combo.pack(pady=5)
    
    result_name = tk.StringVar()

    def on_ok():
        name = combo.get().strip()
        if name:
            result_name.set(name)
            dialog.destroy()
        else:
            messagebox.showwarning("Ошибка", "Имя не может быть пустым!", parent=dialog)

    def on_cancel():
        dialog.destroy()

    btn_frame = tk.Frame(dialog, bg=BG_COLOR)
    btn_frame.pack(pady=15)
    
    tk.Button(btn_frame, text="OK", command=on_ok, width=12, bg=BTN_REC, fg=FG_COLOR, font=("Arial", 10, "bold"), relief="flat", activebackground=BTN_GAME, activeforeground=FG_COLOR).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Отмена", command=on_cancel, width=12, bg="#3d0c11", fg=TEXT_MUTED, font=("Arial", 10, "bold"), relief="flat", activebackground=BTN_SCAN, activeforeground=FG_COLOR).pack(side=tk.LEFT, padx=10)

    root.wait_window(dialog)

    person_name = result_name.get()
    if not person_name:
        return 

    person_folder = os.path.join(dataset_folder, person_name)
    if not os.path.exists(person_folder):
        os.makedirs(person_folder)
        log(f"[+] Создан новый профиль (папка): {person_name}")
        
    filename = os.path.basename(file_path)
    destination = os.path.join(person_folder, filename)
    
    try:
        shutil.copy(file_path, destination)
        log(f"[+] Фото успешно добавлено к: '{person_name}'!")
        log("ВНИМАНИЕ: Нажмите 'Сканировать базу', чтобы программа запомнила это фото.\n")
    except Exception as e:
        log(f"[X] Ошибка при сохранении фото: {e}")

def recognize_photo():
    if len(known_faces) == 0:
        messagebox.showwarning("Внимание", "База пуста или не отсканирована!\nСначала нажмите 'Сканировать базу'.")
        return

    file_path = filedialog.askopenfilename(
        title="Выберите фото для распознавания",
        filetypes=[("Изображения", "*.jpg *.jpeg *.png")]
    )
    if not file_path:
        return

    log(f"Анализ фото: {os.path.basename(file_path)}...")
    
    test_bgr = cv2.imread(file_path)
    if test_bgr is None:
        log("ОШИБКА: Не удалось прочитать тестовое фото!")
        return

    unknown_image = cv2.cvtColor(test_bgr, cv2.COLOR_BGR2RGB)
    
    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

    cv2_image = test_bgr.copy()

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.55)
        name = "Unknown"

        if True in matches:
            face_distances = face_recognition.face_distance(known_faces, face_encoding)
            best_match_index = np.argmin(face_distances)
            
            if matches[best_match_index]:
                name = known_names[best_match_index]

        # Цвет рамок BGR (переведен в оттенки темно-рубиновой эстетики)
        if name == "Me":
            color = (100, 240, 140)    # Светло-зеленый акцент для "Me" чтобы выделялся
        elif name != "Unknown":
            color = (130, 56, 217)     # Розово-рубиновый для знакомых
        else:
            color = (56, 56, 217)      # Красный для незнакомцев
            
        cv2.rectangle(cv2_image, (left, top), (right, bottom), color, 2)
        cv2.putText(cv2_image, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    log("Анализ завершен! Результат выведен в новом окне.\n")
    cv2.imshow("Result", cv2_image)
    cv2.waitKey(0)
    cv2.destroyWindow("Result")

# ---------------------------------------------------------
# ПАСХАЛКИ И ССЫЛКИ
# ---------------------------------------------------------
def open_github(event):
    """Открывает браузер со ссылкой на GitHub"""
    webbrowser.open("https://github.com/Meminttaa")

def play_minigame():
    """Открывает мини-игру в новом окне"""
    game_win = tk.Toplevel(root)
    game_win.title("Аим-тренер: Поймай баг!")
    game_win.geometry("400x400")
    game_win.configure(bg=BG_COLOR)
    game_win.transient(root)
    
    score = tk.IntVar(value=0)
    
    tk.Label(game_win, text="Кликай по жуку как можно быстрее!", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 12)).pack(pady=10)
    lbl_score = tk.Label(game_win, text="Счет: 0", bg=BG_COLOR, fg=LOG_FG, font=("Arial", 16, "bold"))
    lbl_score.pack()

    # Кнопка-жук, перекрашенная под общую тему
    bug_btn = tk.Button(game_win, text="🪲", font=("Arial", 20), bg=BTN_REC, fg=FG_COLOR, relief="flat", cursor="target", activebackground=BTN_GAME)
    
    def catch_bug():
        score.set(score.get() + 1)
        lbl_score.config(text=f"Счет: {score.get()}")
        new_x = random.randint(20, 330)
        new_y = random.randint(80, 330)
        bug_btn.place(x=new_x, y=new_y)

    bug_btn.config(command=catch_bug)
    bug_btn.place(x=170, y=170)

# ---------------------------------------------------------
# ГРАФИЧЕСКИЙ ИНТЕРФЕЙС (GUI)
# ---------------------------------------------------------
root = tk.Tk()
root.title("Умная система распознавания лиц")
root.geometry("550x620") 
root.configure(bg=BG_COLOR) 

# Заголовок
title_label = tk.Label(root, text="CRIMSON FACE RECOGNITION AI", font=("Arial", 15, "bold"), bg=BG_COLOR, fg=BTN_GAME)
title_label.pack(pady=(15, 0))

# --- Панель с кнопками ---
frame_buttons = tk.Frame(root, bg=BG_COLOR)
frame_buttons.pack(pady=10)

# Для всех кнопок добавлены activebackground и activeforeground, чтобы они корректно подсвечивались при нажатии
btn_scan = tk.Button(frame_buttons, text="1. 🔴 Сканировать базу (Обновить)", width=40, height=2, 
                     bg=BTN_SCAN, fg=FG_COLOR, font=("Arial", 10, "bold"), relief="flat", command=start_scanning,
                     activebackground=BTN_UPLOAD, activeforeground=FG_COLOR)
btn_scan.pack(pady=5)

btn_upload = tk.Button(frame_buttons, text="2. 🩸 Добавить фото в базу", width=40, height=2, 
                       bg=BTN_UPLOAD, fg=FG_COLOR, font=("Arial", 10, "bold"), relief="flat", command=upload_to_database,
                       activebackground=BTN_REC, activeforeground=FG_COLOR)
btn_upload.pack(pady=5)

btn_recognize = tk.Button(frame_buttons, text="3. 👁 Распознать лица на фотографии", width=40, height=2, 
                          bg=BTN_REC, fg=FG_COLOR, font=("Arial", 11, "bold"), relief="flat", command=recognize_photo,
                          activebackground=BTN_GAME, activeforeground=FG_COLOR)
btn_recognize.pack(pady=5)

# Кнопка мини-игры
btn_game = tk.Button(frame_buttons, text="🎮 Мини-игра", width=20, height=1, 
                     bg=BTN_GAME, fg=FG_COLOR, font=("Arial", 9, "bold"), relief="flat", command=play_minigame,
                     activebackground=BTN_REC, activeforeground=FG_COLOR)
btn_game.pack(pady=(10, 0))

# --- Текстовая панель для вывода процесса ---
tk.Label(root, text="Терминал процессов:", bg=BG_COLOR, fg=TEXT_MUTED, font=("Arial", 10)).pack(anchor="w", padx=20)

log_text = tk.Text(root, height=10, width=65, state='disabled', bg=LOG_BG, fg=LOG_FG, 
                   font=("Consolas", 10), relief="flat", padx=10, pady=10)
log_text.pack(padx=20, pady=5)

log("Система инициализирована. Готова к работе.\nПожалуйста, нажмите 'Сканировать базу'.")

# --- ССЫЛКА НА GITHUB ---
github_label = tk.Label(root, text="💻 Разработано: github.com/Meminttaa", bg=BG_COLOR, fg=TEXT_MUTED, font=("Arial", 10, "underline"), cursor="hand2", activeforeground=BTN_GAME)
github_label.pack(side=tk.BOTTOM, pady=10)
github_label.bind("<Button-1>", open_github) 

root.mainloop()