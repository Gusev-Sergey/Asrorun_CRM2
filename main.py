from tkinter import *

# from functions import *

from functions.startwindow import *
from functions.menu_top import *
# from functions.import_xlsx_without import import_xlsx_w
import tkinter as tk

import settings



# попытка создания глобальной переменной. Словарь

# print (settings.data_dict) # способ обращения к глобальной переменной для работы из разных файлов


root = Tk()
setwindow(root) # Создание окна. подгружается из startwindow.py





menu_top(root, tk) # Создание верхнего меню. подгружается из startwindow.py

root.mainloop() # закольцовка обновления окна