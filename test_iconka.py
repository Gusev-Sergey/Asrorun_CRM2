import threading
import tkinter as tk
from PIL import Image
import pystray

# Загружаем иконку для Pystray
icon_ico = 'iconka4.ico'

# Создаем объект Icon и запускаем его в отдельном потоке
def run_icon():
    icon_image = Image.open(icon_ico)
    icon = pystray.Icon("Test App", icon=icon_image)
    icon.run()

# Создаем основное окно Tkinter
root = tk.Tk()
root.title("Main Window")
root.geometry("300x200")
label = tk.Label(root, text="This is a test window")
label.pack(pady=20)

# Запускаем иконку в трее в отдельном потоке
thread = threading.Thread(target=run_icon)
thread.daemon = True  # Завершается с завершением программы
thread.start()

# Запускаем главный цикл Tkinter
root.mainloop()