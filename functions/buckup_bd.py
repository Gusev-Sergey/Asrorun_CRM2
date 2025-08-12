import sqlite3
import os
import datetime
from tkinter.messagebox import showinfo, showerror



def backup_base():
    # Путь к базе данных и директории для резервных копий
    db_path = "base/base_contacts.db"
    backup_dir = "base/backup/"

    # Создаем директорию для резервных копий, если она не существует
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # Получаем текущее время для имени файла
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_file = os.path.join(backup_dir, f"backup_{timestamp}.db")

    # Создаем резервную копию
    try:
        # Открываем соединение с исходной базой данных
        conn = sqlite3.connect(db_path)
        # Создаем резервную копию
        with sqlite3.connect(backup_file) as backup_conn:
            conn.backup(backup_conn)
        showinfo(title="Резервная копия", message=f"Резервная копия успешно создана: {backup_file}")
        # print(f"Резервная копия успешно создана: {backup_file}")
    except Exception as e:
        showerror(title="Ошибка", message=f"Ошибка при создании резервной копии: {e}")
        # print(f"Ошибка при создании резервной копии: {e}")
    finally:
        conn.close()
