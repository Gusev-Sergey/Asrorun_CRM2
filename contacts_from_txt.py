import re

# Чтение данных из файла
with open('contacts.txt', 'r', encoding='utf-8') as file:
    data = file.read()

# Разделение данных на записи
records = data.strip().split('\n\n')

# Регулярные выражения для извлечения данных
name_pattern = re.compile(r'([А-ЯЁ][а-яё]+)\s+([А-ЯЁ][а-яё]+)\s+([А-ЯЁ][а-яё]+)')
phone_pattern = re.compile(r'(\d{1,3}\s*\d{3}\s*\d{3}-\d{2}-\d{2})')
email_pattern = re.compile(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})')
position_pattern = re.compile(r'([А-ЯЁа-яё\s]+)')

# Вывод данных в консоль
for record in records:
    lines = record.strip().split('\n')
    name_match = name_pattern.search(lines[0])
    if name_match:
        first_name = name_match.group(1)
        patronymic = name_match.group(2)
        last_name = name_match.group(3)
    else:
        first_name = ''
        patronymic = ''
        last_name = ''

    position = ''
    phone = ''
    email = ''
    status = ''

    for line in lines[1:]:
        if position_pattern.match(line):
            position = line.strip()
        elif phone_pattern.match(line):
            phone = phone_pattern.search(line).group(1)
        elif email_pattern.match(line):
            email = email_pattern.search(line).group(1)
        elif 'уволился' in line:
            status = 'Уволился'

    # Вывод данных в консоль
    print(f"Имя: {first_name}")
    print(f"Отчество: {patronymic}")
    print(f"Фамилия: {last_name}")
    print(f"Должность: {position}")
    print(f"Телефон: {phone}")
    print(f"Email: {email}")
    print(f"Статус: {status}")
    print("---")