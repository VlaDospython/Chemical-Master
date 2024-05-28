import tkinter as tk


def update_position():
    root_x, root_y = toplevel.winfo_x(), toplevel.winfo_y()
    root_x1, root_y1 = root.winfo_x(), root.winfo_y()

    toplevel.geometry(f"+{int((root_x1 + root_x) / 2)}+{int((root_y1 + root_y) / 2)}")
    root.geometry(f"+{int((root_x1 + root_x) / 2)}+{int((root_y1 + root_y) / 2)}")
    toplevel.lift()

    root.after(3, update_position)


def on_minimize(event):
    root.iconify()
    toplevel.iconify()


def on_deiconify(event):
    root.deiconify()
    toplevel.deiconify()


root = tk.Tk()
root.title("Root Window")
root.geometry("700x500")

toplevel = tk.Toplevel(root)
toplevel.title("Toplevel Window")
toplevel.geometry("400x300")

root.bind("<Unmap>", on_minimize)
toplevel.bind("<Unmap>", on_minimize)

root.bind("<Map>", on_deiconify)
toplevel.bind("<Map>", on_deiconify)

update_position()

root.mainloop()
