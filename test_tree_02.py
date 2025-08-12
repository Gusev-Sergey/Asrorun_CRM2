import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog  # Импортируем simpledialog


def on_tree_double_click(event):
    # Получаем выбранный элемент
    selected_item = tree.selection()[0]

    # Запрашиваем новое значение через диалоговое окно
    new_value = simpledialog.askstring('Изменить',
                                       f'Значение текущего элемента: {tree.item(selected_item)["values"][0]}')

    if new_value is not None:
        # Меняем значение выбранного элемента
        tree.item(selected_item, values=(new_value,))


root = tk.Tk()
root.title("Пример редактирования дерева")

# Создаем дерево
columns = ('1', '2')
tree = ttk.Treeview(root, columns=(columns), show='headings')
tree.heading('1', text="Колонка")
tree.heading('2', text="Колонка 2")

# Добавляем несколько начальных записей
tree.insert("", "end", values=("строка 100"))
tree.insert("", "end", values=("Строка 2"))
tree.insert("", "end", values=("Строка 3", "gggg"))

# Привязываем событие двойного клика мыши к изменению строки
tree.bind("<Double-1>", on_tree_double_click)

# Располагаем дерево на экране
tree.pack(expand=True, fill='both')

root.mainloop()