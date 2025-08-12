import pandas as pd
import openpyxl

# Читаем HTML-файл с помощью pandas
html_file = r"C:\PycharmProjects\test\contacts_07.html"
tables = pd.read_html(html_file)

# Предположим, что таблица с контактами — первая в списке
df = tables[0]

# Создаем новый Excel-файл
output_filename = 'contacts07.xlsx'
df.to_excel(output_filename, index=False)

print(f"Сохранено в файл '{output_filename}'")