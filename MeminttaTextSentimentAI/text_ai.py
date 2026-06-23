import os
import tkinter as tk
from tkinter import messagebox, ttk
import joblib
import webbrowser  # Импортируем для открытия ссылки на GitHub
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

MODEL_FILE = "text_classifier.pkl"
VECTORIZER_FILE = "vectorizer.pkl"

# Стили оформления (Ruby Crimson Noir)
BG_COLOR = "#1a080a"
FG_COLOR = "#f5e6e8"
BTN_COLOR = "#4a121a"
BTN_ACTIVE = "#801f2d"
LOG_BG = "#120405"
LOG_FG = "#ffb3ba"
TEXT_MUTED = "#a67c82"

# 4 класса: 3 - Позитив, 2 - Нейтральный, 1 - Смешанный, 0 - Негатив
BASE_TEXTS = [
    "Отличный сайт, все работает очень быстро и удобно!",
    "Прекрасный интерфейс и чистый код, мне очень нравится.",
    "Данный программный продукт написан на языке Python.",
    "В каталоге проекта находится двадцать четыре папки студентов.",
    "Это было не совсем хорошо, но в целом я остался доволен",
    "Нормальный проект, есть плюсы и минусы, пойдет.",
    "Ужасная программа, постоянно вылетает и выдает ошибки.",
    "Ничего не понятно, бэкенд падает, интерфейс лагает.",
    "Вроде работает, но дизайн оставляет желать лучшего.",
    "Замечательный проект разработчика, выполнен на высшем уровне."
]
BASE_LABELS = [3, 3, 2, 2, 1, 1, 0, 0, 1, 3]

class TextAiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Анализатор тональности текста ИИ")
        self.root.geometry("520x720")  # Немного увеличили высоту для подвала
        self.root.configure(bg=BG_COLOR)

        self.texts = list(BASE_TEXTS)
        self.labels = list(BASE_LABELS)

        self.init_model()
        self.create_gui()

    def init_model(self):
        self.train_model(first_time=True)

    def train_model(self, first_time=False):
        self.vectorizer = CountVectorizer()
        X_train = self.vectorizer.fit_transform(self.texts)
        self.model = MultinomialNB()
        self.model.fit(X_train, self.labels)
        joblib.dump(self.model, MODEL_FILE)
        joblib.dump(self.vectorizer, VECTORIZER_FILE)
        if not first_time:
            self.log_message("[+] ИИ успешно переобучен на новых данных!")

    def create_gui(self):
        top_frame = tk.Frame(self.root, bg=BG_COLOR)
        top_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(top_frame, text="   ", bg=BG_COLOR).pack(side=tk.LEFT)
        tk.Label(top_frame, text="CRIMSON TEXT SENTIMENT AI", font=("Arial", 14, "bold"), bg=BG_COLOR, fg="#d9384f").pack(side=tk.LEFT, expand=True)

        btn_help = tk.Button(top_frame, text=" ❓ ", bg="#3d0c11", fg=LOG_FG, font=("Arial", 10, "bold"), relief="flat", activebackground=BTN_ACTIVE, activeforeground=FG_COLOR, command=self.show_help_window)
        btn_help.pack(side=tk.RIGHT, padx=5)

        # 1. Окно ввода текста
        tk.Label(self.root, text="Введите текст для анализа:", bg=BG_COLOR, fg=TEXT_MUTED, font=("Arial", 10)).pack(anchor="w", padx=25)
        self.input_text = tk.Text(self.root, height=4, width=54, bg=LOG_BG, fg=FG_COLOR, font=("Arial", 11), insertbackground=FG_COLOR, padx=5, pady=5, relief="flat")
        self.input_text.pack(pady=5)
        self.input_text.focus_set()

        # Кнопка отправки на анализ
        self.btn_analyze = tk.Button(self.root, text="🧠 Анализировать текст", bg=BTN_COLOR, fg=FG_COLOR, font=("Arial", 10, "bold"), relief="flat", activebackground=BTN_ACTIVE, activeforeground=FG_COLOR, command=self.analyze_text)
        self.btn_analyze.pack(pady=10)

        # 2. Главный вердикт ИИ
        tk.Label(self.root, text="Главный вердикт ИИ:", bg=BG_COLOR, fg=TEXT_MUTED, font=("Arial", 10)).pack(anchor="w", padx=25)
        self.lbl_verdict = tk.Label(self.root, text="Ожидание ввода...", font=("Arial", 12, "bold"), bg=LOG_BG, fg=LOG_FG, width=44, height=2, relief="flat")
        self.lbl_verdict.pack(pady=5)

        # Подробная аналитика (Прогресс-бары)
        tk.Label(self.root, text="Подробный анализ распределения вероятностей:", bg=BG_COLOR, fg=TEXT_MUTED, font=("Arial", 10)).pack(anchor="w", padx=25, pady=(5, 0))
        
        self.analysis_frame = tk.Frame(self.root, bg=LOG_BG, padx=15, pady=10)
        self.analysis_frame.pack(fill="x", padx=25, pady=5)
        
        self.bars = {}
        self.labels_proba = {}
        classes_info = [(3, "Позитив 😊"), (2, "Нейтральный 😐"), (1, "Смешанный 🏎"), (0, "Негативный 😡")]
        
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Crimson.Horizontal.TProgressbar", troughcolor=LOG_BG, background="#b32438", thickness=12)

        for code, name in classes_info:
            row = tk.Frame(self.analysis_frame, bg=LOG_BG)
            row.pack(fill="x", pady=2)
            tk.Label(row, text=f"{name}:", bg=LOG_BG, fg=FG_COLOR, font=("Arial", 9), width=12, anchor="w").pack(side=tk.LEFT)
            
            bar = ttk.Progressbar(row, length=220, mode='determinate', style="Crimson.Horizontal.TProgressbar")
            bar.pack(side=tk.LEFT, padx=5)
            self.bars[code] = bar
            
            lbl = tk.Label(row, text="0.0%", bg=LOG_BG, fg=LOG_FG, font=("Consolas", 9), width=6, anchor="e")
            lbl.pack(side=tk.LEFT)
            self.labels_proba[code] = lbl

        # 3. Блок обратной связи
        tk.Label(self.root, text="Если вердикт неверный, укажите правильный класс:", bg=BG_COLOR, fg=TEXT_MUTED, font=("Arial", 10)).pack(anchor="w", padx=25, pady=(10, 0))
        
        frame_feedback = tk.Frame(self.root, bg=BG_COLOR)
        frame_feedback.pack(pady=5)

        tk.Button(frame_feedback, text="😊 Позитив", bg="#1e3d24", fg=FG_COLOR, font=("Arial", 9, "bold"), relief="flat", command=lambda: self.correct_model(3)).pack(side=tk.LEFT, padx=3)
        tk.Button(frame_feedback, text="😐 Нейтрал", bg="#122d4a", fg=FG_COLOR, font=("Arial", 9, "bold"), relief="flat", command=lambda: self.correct_model(2)).pack(side=tk.LEFT, padx=3)
        tk.Button(frame_feedback, text="🏎 Смешанный", bg="#4a4212", fg=FG_COLOR, font=("Arial", 9, "bold"), relief="flat", command=lambda: self.correct_model(1)).pack(side=tk.LEFT, padx=3)
        tk.Button(frame_feedback, text="😡 Негатив", bg="#4a1212", fg=FG_COLOR, font=("Arial", 9, "bold"), relief="flat", command=lambda: self.correct_model(0)).pack(side=tk.LEFT, padx=3)

        # Лог-терминал
        self.log_text = tk.Text(self.root, height=4, width=54, state='disabled', bg=LOG_BG, fg=LOG_FG, font=("Consolas", 9), relief="flat", padx=5, pady=5)
        self.log_text.pack(pady=10)
        self.log_message("Система готова. Модель расширена до 4-х классов.")

        # --- ПОДВАЛ: Секция разработчика (как в модуле распознавания лиц) ---
        lbl_developer = tk.Label(self.root, text="💻 Разработано: github.com/Meminttaa", bg=BG_COLOR, fg=TEXT_MUTED, font=("Arial", 9, "italic"), cursor="hand2")
        lbl_developer.pack(side=tk.BOTTOM, pady=10)
        lbl_developer.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/Meminttaa"))

    def log_message(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        self.log_text.config(state='disabled')

    def analyze_text(self):
        text = self.input_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Внимание", "Пожалуйста, введите текст!")
            return

        X_test = self.vectorizer.transform([text])
        prediction = self.model.predict(X_test)[0]
        probabilities = self.model.predict_proba(X_test)[0]

        classes = {3: "ПОЗИТИВНЫЙ 😊", 2: "НЕЙТРАЛЬНЫЙ 😐", 1: "СМЕШАННЫЙ 🏎", 0: "НЕГАТИВНЫЙ 😡"}
        
        main_proba = probabilities[prediction] * 100
        self.lbl_verdict.config(text=f"{classes[prediction]} ({main_proba:.2f}%)")
        
        for code in self.bars.keys():
            proba_percent = probabilities[code] * 100
            self.bars[code]['value'] = proba_percent
            self.labels_proba[code].config(text=f"{proba_percent:.1f}%")

        self.log_message(f"[Анализ] Код ответа: {prediction}")

    def correct_model(self, correct_label):
        text = self.input_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Внимание", "Пожалуйста, введите текст.")
            return

        self.texts.append(text)
        self.labels.append(correct_label)
        
        self.train_model()
        
        self.lbl_verdict.config(text="Модель обновлена! Ожидание нового ввода...")
        for code in self.bars.keys():
            self.bars[code]['value'] = 0
            self.labels_proba[code].config(text="0.0%")
            
        self.input_text.delete("1.0", tk.END)
        self.input_text.focus_set()
        
        messagebox.showinfo("ИИ Дообучен", "Спасибо! Текст добавлен в базу данных ИИ. Веса модели успешно скорректированы.")

    def show_help_window(self):
        help_win = tk.Toplevel(self.root)
        help_win.title("Справка: Как работает Crimson Text AI")
        help_win.geometry("460x390")
        help_win.configure(bg=BG_COLOR)
        help_win.transient(self.root)
        help_win.grab_set()

        tk.Label(help_win, text="📊 ПОДРОБНАЯ СПРАВКА ПО МОДЕЛИ", font=("Arial", 12, "bold"), bg=BG_COLOR, fg="#d9384f").pack(pady=10)

        info_text = (
            "🤖 Модифицированный алгоритм:\n"
            "Приложение использует Мультиномиальный Наивный Байес\n"
            "для параллельного распределения математических вероятностей\n"
            "сразу по 4-м независимым классам тональности.\n\n"
            "📈 Матрица подробного анализа:\n"
            "Прогресс-бары показывают точный внутренний вес каждого слова\n"
            "в общей структуре предложения. Если фраза содержит нейтральные\n"
            "факты («написан на Python»), ИИ отдаст приоритет Нейтральному классу.\n\n"
            "🔄 Дообучение на лету:\n"
            "Если ИИ сомневается или выдает ошибочный процент уверенности,\n"
            "кликом по соответствующей кнопке вы принудительно заносите\n"
            "данную лингвистическую конструкцию в базу данных бэкенда.\n"
            "Модель мгновенно перестраивает векторы частотности слов."
        )

        tk.Label(help_win, text=info_text, justify=tk.LEFT, bg=LOG_BG, fg=FG_COLOR, font=("Arial", 10), padx=15, pady=15, relief="flat").pack(padx=15, pady=5)
        tk.Button(help_win, text="Понятно", bg=BTN_COLOR, fg=FG_COLOR, font=("Arial", 10, "bold"), width=15, relief="flat", command=help_win.destroy, activebackground=BTN_ACTIVE, activeforeground=FG_COLOR).pack(pady=15)

if __name__ == "__main__":
    root = tk.Tk()
    app = TextAiApp(root)
    root.mainloop()