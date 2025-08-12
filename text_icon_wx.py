import pystray
from PIL import Image
import tkinter as tk
from tkinter import ttk
import threading

# Загрузка иконки
icon_path = 'sources\\iconka4.ico'
icon_image = Image.open(icon_path)

# Функция для создания иконки в трее
def create_tray_icon():
    def on_clicked(icon, item):
        if str(item) == "Exit":
            icon.stop()
            root.destroy()

    menu = (
        pystray.MenuItem('Exit', on_clicked),
    )

    tray_icon = pystray.Icon("My App", icon_image, "My App", menu)
    tray_icon.run()

# Функция для создания окна ttk
def create_ttk_window():
    root = tk.Tk()
    root.title("My App")

    # Создание фрейма ttk
    frame = ttk.Frame(root, padding=10)
    frame.grid()

    # Добавление виджетов
    label = ttk.Label(frame, text="Hello, World!")
    label.grid(column=0, row=0)

    button = ttk.Button(frame, text="Click Me", command=lambda: print("Button clicked!"))
    button.grid(column=0, row=1)

    # Запуск главного цикла
    root.mainloop()

# Запуск иконки в трее в отдельном потоке
tray_thread = threading.Thread(target=create_tray_icon)
tray_thread.daemon = True  # Демон-поток, завершение с программой
tray_thread.start()

# Запуск окна ttk
create_ttk_window()