import tkinter as tk

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.geometry("200x200")

        # Створення кнопки, що викликає вікно popup
        self.button = tk.Button(root, text="Show Popup", command=self.show_popup)
        self.button.pack()

    def show_popup(self):
        # Створення вікна popup
        self.popup = tk.Toplevel(self.root)
        self.popup.title("Popup Window")

        # Отримання розмірів головного вікна та вікна popup
        root_x, root_y = self.root.winfo_x(), self.root.winfo_y()
        popup_width, popup_height = self.popup.winfo_reqwidth(), self.popup.winfo_reqheight()

        # Обчислення центральних координат для вікна popup
        x = root_x + (self.root.winfo_width() - popup_width) // 2
        y = root_y + (self.root.winfo_height() - popup_height) // 2

        self.popup.geometry(f"+{x}+{y}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()
