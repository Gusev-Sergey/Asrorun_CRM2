
import sqlite3 as sq

def check_record_exists(name_id):
    with sq.connect("base/base_contacts 04.db") as con:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM bcontacts WHERE name_id = ?", (name_id,))
        existing_record = cursor.fetchone()
        if existing_record:
            print(f"Запись с name_id {name_id} существует в базе данных.")
        else:
            print(f"Запись с name_id {name_id} не существует в базе данных.")

# Пример использования
check_record_exists(1)  # Замените 1 на нужный вам name_id