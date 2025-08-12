from tkinter import *
from tkinter import ttk

root = Tk()
root.title("METANIT.COM")
root.geometry("250x200")

# определяем данные для отображения
people = [("Tom", 38, "tom@email.com"), ("Bob", 42, "bob@email.com"), ("Sam", 28, "sam@email.com")]

# определяем столбцы
columns = ("name", "age", "email")

tree = ttk.Treeview(columns=columns, show="headings")
tree.pack(expand=1, fill=BOTH)


def sort(col, reverse):
    # получаем все значения столбцов в виде отдельного списка
    l = [(tree.set(k, col), k) for k in tree.get_children("")]
    # сортируем список
    l.sort(reverse=reverse)
    # переупорядочиваем значения в отсортированном порядке
    for index, (_, k) in enumerate(l):
        tree.move(k, "", index)
    # в следующий раз выполняем сортировку в обратном порядке
    tree.heading(col, command=lambda: sort(col, not reverse))


# определяем заголовки
tree.heading("name", text="Имя", anchor=W, command=lambda: sort(0, False))
tree.heading("age", text="Возраст", anchor=W, command=lambda: sort(1, False))
tree.heading("email", text="Email", anchor=W, command=lambda: sort(2, False))

tree.column("#1", stretch=NO, width=70)
tree.column("#2", stretch=NO, width=60)
tree.column("#3", stretch=NO, width=100)

# добавляем данные
for person in people:
    tree.insert("", END, values=person)

root.mainloop()