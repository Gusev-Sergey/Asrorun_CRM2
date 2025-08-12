from functions.import_xlsx_without import *
from functions.contacts_show import show_contacts_in_window
from functions.save_base import save_base
from functions.load_base import load_base
from functions.buckup_bd import backup_base
from functions.import_xlsx_add import import_xls_add
from functions.import_clients import import_xlsx_clients
from functions.import_xlsx_clients_check import import_xlsx_clients_check
from functions.clients_show import clients_show
import settings
from PIL import Image
import pystray
import threading


def run_icon(icon_path):
    # Загружаем иконку для Pystray
    icon_image = Image.open(icon_path)
    # Создаем объект Icon и запускаем его
    icon = pystray.Icon("Astrorum Arbor", icon=icon_image)
    icon.run()

def menu_top(root, tk):
    # Укажите правильный путь к файлам иконок
    icon_png = r'sources/iconka.png'  # Иконка для Tkinter (формат .png)
    icon_ico = r'C:\PycharmProjects\stepik\Astrorum_CRM\sources\iconka_ico.ico'  # Иконка для Pystray (формат .ico)

    # Загружаем иконку для Tkinter
    icon_photo = tk.PhotoImage(file=icon_png)
    root.iconphoto(True, icon_photo)

    # Запускаем иконку в трее в отдельном потоке
    thread = threading.Thread(target=run_icon, args=(icon_ico,))
    thread.daemon = True  # Демон-поток, завершение с программой
    thread.start()



    # Формируем верхнее меню
    mainmenu = tk.Menu(root)
    root.config(menu=mainmenu)





    font_style = ("Tahoma", 12)

    # Формируем верхнее меню
    mainmenu = tk.Menu(root)
    root.config(menu=mainmenu)

    ajust_menu = tk.Menu(mainmenu, tearoff=0, font=font_style)
    ajust_menu.add_command(label="Настройки 1")
    ajust_menu.add_command(label="Настройки 2")
    # ajust_menu.add_command(label="Сохранить...")

    #
    helpmenu = tk.Menu(mainmenu, tearoff=0, font=font_style)
    helpmenu.add_command(label="Помощь")
    helpmenu.add_command(label="О программе")

    download = tk.Menu(mainmenu, tearoff=0, font=font_style)
    download.add_cascade(label="(Врем)Импорт контактов из .xlsx без проверок", command=lambda: import_xlsx_w(settings.data_dict))
    download.add_cascade(label="Импорт контактов из .xlsx. Дополнить базу", command=lambda: import_xls_add(settings.data_dict))
    download.add_cascade(label="(Врем)Сохранить всю базу данных из xlsx", command=lambda: save_base(settings.data_dict))
    download.add_cascade(label="Сделать backup БД", command=lambda: backup_base())
    download.add_cascade(label="Загрузить базу данных контактов", command=load_base)
    download.add_cascade(label="(врем)Импорт контрагентов без проверки", command=import_xlsx_clients)
    download.add_cascade(label="Импорт контрагентов с проверкой", command=lambda: import_xlsx_clients_check(root))


    #
    crm_menu = tk.Menu(mainmenu, tearoff=0, font=font_style)
    crm_menu.add_command(label="Контакты", command=lambda: show_contacts_in_window(root, ""))
    crm_menu.add_command(label="Контрагенты", command=lambda: clients_show(root, ""))
    crm_menu.add_command(label="Выход", command=root.destroy)  # Выход из программы



    mainmenu.add_cascade(label="CRM", font=font_style, menu=crm_menu)
    mainmenu.add_cascade(label="Служебные", font=font_style, menu=download)
    mainmenu.add_cascade(label="Настройки", font=font_style, menu=ajust_menu)
    mainmenu.add_cascade(label="Справка", font=font_style, menu=helpmenu)


