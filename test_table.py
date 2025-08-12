from tkinter import *
from tkinter import ttk

root = Tk()
root.title("METANIT.COM")
root.geometry("250x200")
root.rowconfigure(index=0, weight=1)
root.columnconfigure(index=0, weight=1)

# определяем данные для отображения
people = [
    ("Tom", 38, "tom@email.com"), ("Bob", 42, "bob@email.com"), ("Sam", 28, "sam@email.com"),
    ("Alice", 33, "alice@email.com"), ("Kate", 21, "kate@email.com"), ("Ann", 24, "ann@email.com"),
    ("Mike", 34, "mike@email.com"), ("Alex", 52, "alex@email.com"), ("Jess", 28, "jess@email.com"),
]

# определяем столбцы
columns = ("name", "age", "email")

tree = ttk.Treeview(columns=columns, show="headings")
tree.grid(row=0, column=0, sticky="nsew")

# определяем заголовки
tree.heading("name", text="Имя", anchor=W)
tree.heading("age", text="Возраст", anchor=W)
tree.heading("email", text="Email", anchor=W)

tree.column("#1", stretch=True, width=70)
tree.column("#2", stretch=True, width=60)
tree.column("#3", stretch=True, width=100)

# добавляем данные
for person in people:
    tree.insert("", END, values=person)

# добавляем вертикальную прокрутку
scrollbar = ttk.Scrollbar(orient=VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=0, column=1, sticky="ns")

root.mainloop()