import tkinter as tk

def add_item(entry, listbox):
    item = entry.get()
    if item:
        listbox.insert(tk.END, item)
        entry.delete(0, tk.END)

def confirm():
    global widgets_to_create

    # Check if there are items in the list
    if listbox.size() == 0:
        # If the list is empty, recreate the initial widgets
        for widget in widgets_to_create:
            widget.grid()
    else:
        # If the list has items, clear the list and hide the widgets
        listbox.delete(0, tk.END)
        for widget in widgets_to_create:
            widget.grid_remove()

def delete_item(listbox):
    selected_item = listbox.curselection()
    if selected_item:
        index = selected_item[0]
        listbox.delete(index)

def create_widgets():
    global widgets_to_create, entry, listbox
    widgets_to_create = []

    label = tk.Label(root, text="Enter a new item:")
    entry = tk.Entry(root)
    add_button = tk.Button(root, text="Add Item", command=lambda: add_item(entry, listbox))
    confirm_button = tk.Button(root, text="Confirm", command=confirm)
    delete_button = tk.Button(root, text="Delete Item", command=lambda: delete_item(listbox))

    widgets_to_create.extend([label, entry, add_button, confirm_button, delete_button])

    row = 1
    for widget in widgets_to_create:
        widget.grid(row=row, column=0, padx=10, pady=5)
        row += 1

root = tk.Tk()
root.title("Widget List Manager")

listbox = tk.Listbox(root)
listbox.grid(row=0, column=1, padx=10, pady=5)

widgets_to_create = []
entry = None

create_widgets()

root.mainloop()
