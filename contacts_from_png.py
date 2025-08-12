import easyocr

# Инициализация OCR
reader = easyocr.Reader(['ru'])  # Список поддерживаемых языков

# Распознавание текста
result = reader.readtext('111_kz.png')

# Вывод результата
for detection in result:
    print(detection[1])  # Распознанный текст