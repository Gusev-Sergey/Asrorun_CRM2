import sqlite3 as sq

# Функция для создания/открытия базы данных и таблицы
def setup_database():
    with sq.connect("base/base_contacts 04.db") as con:
        cursor = con.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bcontacts (
                name_id INTEGER PRIMARY KEY AUTOINCREMENT,
                contact TEXT,
                second_name TEXT,
                first_name TEXT,
                patronymic TEXT,
                post TEXT,
                company TEXT,
                phone TEXT,
                email TEXT,
                inn TEXT,
                comment TEXT
            );
        """)

# Функция для добавления записи
def add_record(contact_data):
    with sq.connect("base/base_contacts 04.db") as con:
        cursor = con.cursor()
        insert_query = """
            INSERT INTO bcontacts (contact, second_name, first_name, patronymic, post, company, phone, email, inn, comment)
            VALUES (?,?,?,?,?,?,?,?,?,?)
        """
        cursor.execute(insert_query, contact_data)
        con.commit()
        print("Запись успешно добавлена!")

# Функция для обновления записи
def update_record(name_id, updated_data):
    with sq.connect("base/base_contacts 04.db") as con:
        cursor = con.cursor()
        update_query = """
            UPDATE bcontacts SET
                contact = ?,
                second_name = ?,
                first_name = ?,
                patronymic = ?,
                post = ?,
                company = ?,
                phone = ?,
                email = ?,
                inn = ?,
                comment = ?
            WHERE name_id = ?
        """
        updated_data.append(name_id)  # Добавляем идентификатор в конец массива
        cursor.execute(update_query, updated_data)
        con.commit()
        print("Запись успешно обновлена!")

# Тестовая функция для демонстрации возможностей
def main():
    setup_database()

    # Добавляем тестовую запись
    test_data = [
        "Иван Иванов",  # contact
        "Иванов",      # second_name
        "Иван",        # first_name
        "Иванович",    # patronymic
        "Генеральны директор",  # post
        "ООО \"Ростех\"",  # company
        "+7 999 123-45-67",  # phone
        "ivanov@gmail.com",  # email
        "",              # inn
        "Тестовый комментарий"  # comment
    ]
    add_record(test_data)

    # Обновляем запись
    updated_data = [
        "Иван Петрович Иванов",  # contact
        "Иванов",               # second_name
        "Иван",                 # first_name
        "Петрович",             # patronymic
        "Исполнительный директор",  # post
        "ООО \"Роснаука\"",    # company
        "+7 999 123-45-68",    # phone
        "ivan.petrovich@gmail.com",  # email
        "1234567890",          # inn
        "Обновлённый комментарий"  # comment
    ]
    update_record(1, updated_data)

if __name__ == "__main__":
    main()