from tkinter import ttk, Entry

from functions.import_xlsx_without import *

def show_contacts_in_window(root):

    dict = imp()

    # print("zx-spectrum", dict)
    # print("!!!!!", dict)

    font_style = ("Tahoma", 12)

    # en1=ttk.Entry(root, font="Tahoma 12")  # создали форму для вывода
    # Entry(root, font="Tahoma 12", bg=fon_label_edit, name=name)  # создали форму для вывода

    # en1.pack()
# btn["text"]="Send"

    # en1["text"]="Проверка"
    # en1.insert(0, "Проверка___999")
    # insert(index, str)

    label_style = ttk.Style()
    label_style.configure("My.TLabel",  # имя стиля
                          font="Tahoma 12",  # шрифт
                          foreground="black",  # цвет текста
                          padding=1,  # отступы
                          background="#D9DCE0",# фоновый цве
                          borderwidth=1)

    input_entry = ttk.Entry(name="entry_to_search", font=font_style, style="My.TLabel")

    label1 = ttk.Label(text="Контакт", name="label_contact", font=font_style, style="My.TLabel")
    label2 = ttk.Label(text="Фамилия", name="label_sername", font=font_style, style="My.TLabel")
    label3 = ttk.Label(text="Имя", name="label_firstname", font=font_style, style="My.TLabel")
    label4 = ttk.Label(text="Отчество", name="label_3dname", font=font_style, style="My.TLabel")
    label5 = ttk.Label(text="Должность", name="label_post", font=font_style, style="My.TLabel")
    label6 = ttk.Label(text="Компания", name="label_company", font=font_style, style="My.TLabel")
    label7 = ttk.Label(text="Телефон", name="label_phone", font=font_style, style="My.TLabel")
    label8 = ttk.Label(text="e-mail", name="label_email", font=font_style, style="My.TLabel")

    # label1.grid(row=0, column=0, padx=15, pady=5, columnspan=3, sticky="nw")
    input_entry.grid(row=0, column=0, columnspan=7, padx=1, pady=1, sticky="nw")

    label1.grid(row=1, column=0, padx=1, pady=1, sticky="nw")
    label2.grid(row=1, column=1, padx=1, pady=1, sticky="nw")
    label3.grid(row=1, column=2, padx=5, pady=5, sticky="nw")
    label4.grid(row=1, column=3, padx=5, pady=5, sticky="nw")
    label5.grid(row=1, column=4, padx=5, pady=5, sticky="nw")
    label6.grid(row=1, column=5, padx=5, pady=5, sticky="nw")
    label7.grid(row=1, column=6, padx=5, pady=5, sticky="nw")
    label8.grid(row=1, column=7, padx=5, pady=5, sticky="nw")

    root.columnconfigure(0, weight=20)
    root.columnconfigure(1, weight=10)
    root.columnconfigure(2, weight=10)
    root.columnconfigure(3, weight=10)
    root.columnconfigure(4, weight=10)
    root.columnconfigure(5, weight=100)
    root.columnconfigure(6, weight=10)
    root.columnconfigure(7, weight=10)

    # for r in range(3):
    #     for c in range(8):
    #         btn = ttk.Button(text=f"11222333444({r},{c})")
    #         btn.grid(row=r+1, column=c, sticky="nw")

    for i in range(40):
        for j in range(8):

            name = str(i) + "name" + str(j)

            if j == 5:
                lab_temp = ttk.Label(text=dict[i][j], name=name, wraplength=350, borderwidth=2,background="#B3DDCE")
                lab_temp.grid(row=(i + 2), column=j, sticky="nw", padx=2, pady=2)

            else:
                lab_temp = ttk.Label(text=dict[i][j], name=name, borderwidth=2, background="#B3DDCE")
                lab_temp.grid(row=(i + 2), column=j, sticky="nw", padx=2, pady=2)




            # lab_temp = ttk.Label(text=dict[i][j], name=name)
            # lab_temp.grid(row=i + 1, column=j, sticky="nw")