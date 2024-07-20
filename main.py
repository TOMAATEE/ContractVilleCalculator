from tkinter import *
from tkinter import ttk
from rooms_n_config import rooms, default, font


def reset_entry():
    for j in entries:
        j.delete(0, END)
        j.insert(0, "1" if j._name in default else "0")


def set_all():
    for j in entries:
        j.delete(0, END)
        j.insert(0, all_entry.get())


def validate(input, action):
    if action == "1":  # 1 = insert, 0 = delete
        if not input.isdigit():
            return False
    return True


def calculate():
    needed = {}
    total = 0
    for e in entries:                      # for every room entry ...
        amount = int(e.get())
        if amount == 0:                    # ... that isn't 0 ...
            continue
        total += amount
        for item in lower_rooms[e._name]:  # ... multiply the needed furniture amount by the amount of rooms ...
            if item not in needed:
                needed[item] = lower_rooms[e._name][item] * amount
            else:                          # ... and add them together if there are multiple of the same furniture
                needed[item] += lower_rooms[e._name][item] * amount

    all_you_need = ""
    for stuff in needed:
        all_you_need += f"{stuff}: {needed[stuff]}\n"
    furniture_label.config(text=all_you_need)
    total_label.config(text=f"Amount of rooms: {total} total")


# Create the main window
root = Tk()
root.title("ContractVille-Calculator")
root.option_add("*font", font)

lower_rooms = {}
entries = []

# Create labels and entries for every room and add them to the grid
row_val = 0
col_val = 0

total_label = ttk.Label(root, text="Amount of rooms:")
total_label.grid(row=row_val, column=col_val, sticky='nsew', ipadx=5, ipady=5, padx=5, columnspan=2)

(ttk.Label(root, text="Required Furniture:")
 .grid(row=row_val, column=col_val + 2, sticky='nsew', ipadx=5, ipady=5, columnspan=2))

furniture_label = ttk.Label(root)
furniture_label.grid(row=row_val + 1, column=col_val + 2,
                     rowspan=len(rooms), columnspan=2,
                     sticky='new', ipadx=5, ipady=5)
row_val += 1
x = 0
for room in rooms:
    lower_rooms[room.lower()] = rooms[room]  # needed because entry names have to be lower case
    entries.append(room)

    entries[-1] = ttk.Entry(root, width=3, justify="center", name=room.lower(), validate="key")
    entries[-1]['validatecommand'] = (entries[-1].register(validate), '%P', '%d')
    entries[-1].grid(row=row_val, column=col_val, sticky='nsew', ipadx=5, ipady=5, pady=2, padx=5)
    entries[-1].insert(0, default[room.lower()] if room.lower() in default else "0")

    (ttk.Label(root, text=(room+"(s)"))
     .grid(row=row_val, column=col_val + 1, sticky='nsew', ipadx=5, ipady=5, pady=2))
    row_val += 1

# Additional buttons
(Button(root, text="Calculate", command=calculate)
 .grid(row=row_val, column=col_val, sticky='nsw', ipadx=5, ipady=5, padx=5, pady=5, columnspan=2))
col_val += 2
(Button(root, text="Reset to default", command=reset_entry)
 .grid(row=row_val, column=col_val, ipadx=5, ipady=5, padx=5, pady=5))
col_val += 1
(Button(root, text="set all to:", command=set_all)
 .grid(row=row_val, column=col_val, ipadx=5, ipady=5, padx=5, pady=5))
col_val += 1
all_entry = ttk.Entry(root, width=3, justify="center", validate="key")
all_entry['validatecommand'] = (all_entry.register(validate), '%P', '%d')
all_entry.grid(row=row_val, column=col_val, sticky='nsew', ipadx=5, ipady=5, pady=5, padx=5)
all_entry.insert(0, "0")

# Configure row and column weights so that everything expands with window resizing
for i in range(len(rooms)+5):
    root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)

# Start the main loop
root.mainloop()
