import tkinter as tk
from tkinter import messagebox
import json
import os

# Цвета для светлой темы
LIGHT_TEXT_COLOR = "#584738"
LIGHT_BACKGROUND_COLOR = "#B59E7D"
LIGHT_BUTTON_COLOR = "#8B7355"
LIGHT_HOVER_COLOR = "#6B5A4A"

# Цвета для тёмной темы
DARK_TEXT_COLOR = "#B59E7D"
DARK_BACKGROUND_COLOR = "#584738"
DARK_BUTTON_COLOR = "#6B5A4A"
DARK_HOVER_COLOR = "#8B7355"

# Текущая тема (по умолчанию светлая)
current_theme = "light"

# Функция для загрузки данных из JSON-файла
def load_data(letter):
    file_path = f"data_{letter}.json"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    else:
        messagebox.showerror("Ошибка", f"Файл для буквы {letter} не найден.")
        return {}

# Функция для отображения списка слов
def show_words(letter):
    data = load_data(letter)
    if not data:
        return

    # Очищаем фрейм для контента
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Кнопка "Назад" к буквам
    back_button = tk.Button(
        content_frame,
        text="← Назад к буквам",
        command=show_alphabet,
        font=("Helvetica", 12),
        fg="white",
        bg=LIGHT_BUTTON_COLOR if current_theme == "light" else DARK_BUTTON_COLOR,
        relief="flat",
        bd=0,
        padx=20,
        pady=10,
        activebackground=LIGHT_HOVER_COLOR if current_theme == "light" else DARK_HOVER_COLOR,
        activeforeground="white"
    )
    back_button.pack(pady=10)

    # Canvas для прокрутки
    canvas = tk.Canvas(content_frame, bg=LIGHT_BACKGROUND_COLOR if current_theme == "light" else DARK_BACKGROUND_COLOR, highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    # Добавляем Scrollbar
    scrollbar = tk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # Настраиваем Canvas для работы с Scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # Фрейм для кнопок слов внутри Canvas
    words_frame = tk.Frame(canvas, bg=LIGHT_BACKGROUND_COLOR if current_theme == "light" else DARK_BACKGROUND_COLOR)
    canvas.create_window((0, 0), window=words_frame, anchor="nw")

    # Отображаем слова
    for word in data:
        button = tk.Button(
            words_frame,
            text=word,
            command=lambda w=word, d=data: show_meaning(w, d[w]),
            font=("Helvetica", 12),
            fg=LIGHT_TEXT_COLOR if current_theme == "light" else DARK_TEXT_COLOR,
            bg=LIGHT_BUTTON_COLOR if current_theme == "light" else DARK_BUTTON_COLOR,
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
            width=30,  # Увеличиваем ширину кнопок
            activebackground=LIGHT_HOVER_COLOR if current_theme == "light" else DARK_HOVER_COLOR,
            activeforeground="white"
        )
        button.pack(fill="x", pady=5, padx=20)  # Добавляем отступы по бокам

# Функция для отображения алфавита
def show_alphabet():
    # Очищаем фрейм для контента
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Фрейм для центрирования кнопок букв
    center_frame = tk.Frame(content_frame, bg=LIGHT_BACKGROUND_COLOR if current_theme == "light" else DARK_BACKGROUND_COLOR)
    center_frame.pack(expand=True)

    # Отображаем буквы
    for i, letter in enumerate("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"):
        button = tk.Button(
            center_frame,
            text=letter,
            command=lambda l=letter: show_words(l),
            font=("Helvetica", 14),
            fg="white",
            bg=LIGHT_BUTTON_COLOR if current_theme == "light" else DARK_BUTTON_COLOR,
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
            activebackground=LIGHT_HOVER_COLOR if current_theme == "light" else DARK_HOVER_COLOR,
            activeforeground="white"
        )
        button.grid(row=i // 6, column=i % 6, padx=10, pady=10)

# Функция для отображения значения слова
def show_meaning(word, meaning):
    meaning_window = tk.Toplevel(root)
    meaning_window.title(word)
    meaning_window.geometry("600x400")
    meaning_window.configure(bg=LIGHT_BACKGROUND_COLOR if current_theme == "light" else DARK_BACKGROUND_COLOR)

    # Заголовок
    label = tk.Label(
        meaning_window,
        text=word,
        font=("Helvetica", 18, "bold"),
        fg=LIGHT_TEXT_COLOR if current_theme == "light" else DARK_TEXT_COLOR,
        bg=LIGHT_BACKGROUND_COLOR if current_theme == "light" else DARK_BACKGROUND_COLOR
    )
    label.pack(pady=20)

    # Текст значения
    text_frame = tk.Frame(meaning_window, bg=LIGHT_BACKGROUND_COLOR if current_theme == "light" else DARK_BACKGROUND_COLOR)
    text_frame.pack(fill="both", expand=True, padx=20, pady=10)

    text = tk.Text(
        text_frame,
        wrap="word",
        font=("Helvetica", 12),
        fg=LIGHT_TEXT_COLOR if current_theme == "light" else DARK_TEXT_COLOR,
        bg=LIGHT_BACKGROUND_COLOR if current_theme == "light" else DARK_BACKGROUND_COLOR,
        bd=0,
        highlightthickness=0
    )
    text.insert("1.0", meaning)
    text.config(state="disabled")  # Запрещаем редактирование
    text.pack(fill="both", expand=True)

# Функция для смены темы
def toggle_theme():
    global current_theme
    if current_theme == "light":
        current_theme = "dark"
    else:
        current_theme = "light"
    apply_theme()

# Применение текущей темы
def apply_theme():
    theme_text_color = LIGHT_TEXT_COLOR if current_theme == "light" else DARK_TEXT_COLOR
    theme_bg_color = LIGHT_BACKGROUND_COLOR if current_theme == "light" else DARK_BACKGROUND_COLOR
    theme_button_color = LIGHT_BUTTON_COLOR if current_theme == "light" else DARK_BUTTON_COLOR
    theme_hover_color = LIGHT_HOVER_COLOR if current_theme == "light" else DARK_HOVER_COLOR

    root.configure(bg=theme_bg_color)
    title_label.config(fg=theme_text_color, bg=theme_bg_color)
    content_frame.config(bg=theme_bg_color)

    for widget in content_frame.winfo_children():
        if isinstance(widget, tk.Button):
            widget.config(
                fg="white" if widget["text"] in "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ← Назад к буквам" else theme_text_color,
                bg=theme_button_color,
                activebackground=theme_hover_color,
                activeforeground="white"
            )
        elif isinstance(widget, tk.Canvas):
            widget.config(bg=theme_bg_color)

    theme_button.config(
        text="🌙" if current_theme == "light" else "☀️",
        bg=theme_button_color,
        activebackground=theme_hover_color
    )

# Главное окно
root = tk.Tk()
root.title("Настольная энциклопедия «Хочу все знать 2025»")
root.geometry("800x600")
root.configure(bg=LIGHT_BACKGROUND_COLOR)

# Кнопка смены темы
theme_button = tk.Button(
    root,
    text="🌙",
    command=toggle_theme,
    font=("Helvetica", 12),
    fg="white",
    bg=LIGHT_BUTTON_COLOR,
    relief="flat",
    bd=0,
    padx=10,
    pady=5,
    activebackground=LIGHT_HOVER_COLOR,
    activeforeground="white"
)
theme_button.place(x=10, y=10)

# Заголовок
title_label = tk.Label(
    root,
    text="Выберите букву:",
    font=("Helvetica", 24, "bold"),
    fg=LIGHT_TEXT_COLOR,
    bg=LIGHT_BACKGROUND_COLOR
)
title_label.pack(pady=30)

# Фрейм для контента (буквы или слова)
content_frame = tk.Frame(root, bg=LIGHT_BACKGROUND_COLOR)
content_frame.pack(fill="both", expand=True, padx=20, pady=20)

# Изначально отображаем алфавит
show_alphabet()

# Запуск главного окна
root.mainloop()