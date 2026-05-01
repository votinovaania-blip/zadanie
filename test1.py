import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

# ------------------ Файл для сохранения данных ------------------
DATA_FILE = "books.json"

# ------------------ Класс приложения ------------------
class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker - Трекер прочитанных книг")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Данные: список словарей
        self.books = []
        self.load_data()

        # Создание интерфейса
        self.create_widgets()
        self.update_table()

    # ------------------ Загрузка / сохранение JSON ------------------
    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.books = json.load(f)
            except:
                self.books = []

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.books, f, indent=4, ensure_ascii=False)

    # ------------------ Создание элементов интерфейса ------------------
    def create_widgets(self):
        # Рамка для ввода данных
        input_frame = tk.LabelFrame(self.root, text="Добавить книгу", padx=10, pady=10, font=("Arial", 10, "bold"))
        input_frame.pack(pady=10, padx=10, fill="x")

        # Название книги
        tk.Label(input_frame, text="Название книги:", font=("Arial", 9)).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.title_entry = tk.Entry(input_frame, width=25, font=("Arial", 9))
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        # Автор
        tk.Label(input_frame, text="Автор:", font=("Arial", 9)).grid(row=0, column=2, sticky="e", padx=5, pady=5)
        self.author_entry = tk.Entry(input_frame, width=20, font=("Arial", 9))
        self.author_entry.grid(row=0, column=3, padx=5, pady=5)

        # Жанр
        tk.Label(input_frame, text="Жанр:", font=("Arial", 9)).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.genre_var = tk.StringVar()
        genres = ["Роман", "Детектив", "Фантастика", "Научная литература", "Поэзия", "Драма", "Приключения", "Биография"]
        self.genre_combo = ttk.Combobox(input_frame, textvariable=self.genre_var, values=genres, width=20)
        self.genre_combo.grid(row=1, column=1, padx=5, pady=5)
        self.genre_combo.current(0)

        # Количество страниц
        tk.Label(input_frame, text="Количество страниц:", font=("Arial", 9)).grid(row=1, column=2, sticky="e", padx=5, pady=5)
        self.pages_entry = tk.Entry(input_frame, width=10, font=("Arial", 9))
        self.pages_entry.grid(row=1, column=3, padx=5, pady=5)

        # Кнопка добавления
        add_btn = tk.Button(input_frame, text="📚 Добавить книгу", command=self.add_book, bg="#4CAF50", fg="white", font=("Arial", 9, "bold"))
        add_btn.grid(row=0, column=4, rowspan=2, padx=15, pady=5)

        # Рамка для фильтров
        filter_frame = tk.LabelFrame(self.root, text="Фильтрация", padx=10, pady=10, font=("Arial", 10, "bold"))
        filter_frame.pack(pady=5, padx=10, fill="x")

        tk.Label(filter_frame, text="Фильтр по жанру:", font=("Arial", 9)).grid(row=0, column=0, padx=5, pady=5)
        self.filter_genre_var = tk.StringVar(value="Все")
        filter_genre_combo = ttk.Combobox(filter_frame, textvariable=self.filter_genre_var, values=["Все"] + genres, width=15)
        filter_genre_combo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(filter_frame, text="Фильтр по страницам (>):", font=("Arial", 9)).grid(row=0, column=2, padx=5, pady=5)
        self.filter_pages_entry = tk.Entry(filter_frame, width=10, font=("Arial", 9))
        self.filter_pages_entry.grid(row=0, column=3, padx=5, pady=5)

        filter_btn = tk.Button(filter_frame, text="🔍 Применить фильтр", command=self.update_table, bg="#2196F3", fg="white", font=("Arial", 9))
        filter_btn.grid(row=0, column=4, padx=10, pady=5)

        reset_btn = tk.Button(filter_frame, text="❌ Сбросить фильтры", command=self.reset_filters, bg="#FF9800", fg="white", font=("Arial", 9))
        reset_btn.grid(row=0, column=5, padx=5, pady=5)

        # Таблица (Treeview)
        table_frame = tk.Frame(self.root)
        table_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Создание таблицы с прокруткой
        columns = ("title", "author", "genre", "pages")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        self.tree.heading("title", text="Название книги")
        self.tree.heading("author", text="Автор")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("pages", text="Страниц")
        
        self.tree.column("title", width=200, anchor="w")
        self.tree.column("author", width=150, anchor="w")
        self.tree.column("genre", width=120, anchor="center")
        self.tree.column("pages", width=80, anchor="center")

        # Вертикальная прокрутка
        scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        
        # Горизонтальная прокрутка
        scrollbar_x = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=scrollbar_x.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")

        # Кнопка удаления выбранной записи
        del_btn = tk.Button(self.root, text="🗑 Удалить выбранную книгу", command=self.delete_selected, bg="#f44336", fg="white", font=("Arial", 9, "bold"))
        del_btn.pack(pady=5)

        # Статусная строка
        self.status_label = tk.Label(self.root, text="Готово", font=("Arial", 8), fg="gray")
        self.status_label.pack(side="bottom", pady=5)

    # ------------------ Добавление книги с проверкой ------------------
    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_var.get()
        pages = self.pages_entry.get().strip()

        # Проверка на пустые поля
        if not title:
            messagebox.showerror("Ошибка", "Введите название книги")
            return
        if not author:
            messagebox.showerror("Ошибка", "Введите автора")
            return
        if not pages:
            messagebox.showerror("Ошибка", "Введите количество страниц")
            return

        # Проверка количества страниц (должно быть положительным целым числом)
        try:
            pages_val = int(pages)
            if pages_val <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Количество страниц должно быть положительным целым числом")
            return

        # Добавляем запись
        self.books.append({
            "title": title,
            "author": author,
            "genre": genre,
            "pages": pages_val
        })
        self.save_data()
        self.update_table()

        # Очистка полей
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.pages_entry.delete(0, tk.END)
        self.genre_combo.current(0)
        
        self.status_label.config(text=f"Книга '{title}' добавлена")
        messagebox.showinfo("Успех", f"Книга '{title}' успешно добавлена!")

    # ------------------ Обновление таблицы с учетом фильтров ------------------
    def update_table(self):
        # Очищаем таблицу
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Получаем фильтры
        filter_genre = self.filter_genre_var.get()
        filter_pages = self.filter_pages_entry.get().strip()

        # Фильтрация данных
        filtered = self.books
        
        # Фильтр по жанру
        if filter_genre != "Все":
            filtered = [b for b in filtered if b["genre"] == filter_genre]
        
        # Фильтр по количеству страниц (> значение)
        if filter_pages:
            try:
                pages_min = int(filter_pages)
                if pages_min >= 0:
                    filtered = [b for b in filtered if b["pages"] > pages_min]
                else:
                    messagebox.showwarning("Предупреждение", "Фильтр по страницам должен быть положительным числом")
            except ValueError:
                messagebox.showwarning("Предупреждение", "Некорректное значение фильтра по страницам")

        # Заполняем таблицу
        for book in filtered:
            self.tree.insert("", tk.END, values=(book["title"], book["author"], book["genre"], f"{book['pages']}"))
        
        self.status_label.config(text=f"Показано {len(filtered)} из {len(self.books)} книг")

    # ------------------ Сброс фильтров ------------------
    def reset_filters(self):
        self.filter_genre_var.set("Все")
        self.filter_pages_entry.delete(0, tk.END)
        self.update_table()
        self.status_label.config(text="Фильтры сброшены")

    # ------------------ Удаление выбранной книги ------------------
    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите книгу для удаления")
            return

        # Получаем данные выбранной строки
        item = self.tree.item(selected[0])
        values = item["values"]
        if values:
            title, author, genre, pages_str = values
            pages = int(pages_str)

            # Ищем и удаляем из списка
            for i, book in enumerate(self.books):
                if (book["title"] == title and book["author"] == author and 
                    book["genre"] == genre and book["pages"] == pages):
                    del self.books[i]
                    break

            self.save_data()
            self.update_table()
            self.status_label.config(text=f"Книга '{title}' удалена")
            messagebox.showinfo("Успех", f"Книга '{title}' удалена")


# ------------------ Точка входа ------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = BookTracker(root)
    root.mainloop()