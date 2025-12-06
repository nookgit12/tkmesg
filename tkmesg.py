import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading

class DmesgApp:
    def __init__(self, root):
        self.root = root
        self.root.title("tkmesg")
        
        # Text display
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=35)
        self.text_area.pack(padx=10, pady=10)

        # Buttons
        button_frame = tk.Frame(root)
        button_frame.pack()

        tk.Button(button_frame, text="Refresh", command=self.update_output).pack(side=tk.LEFT, padx=5)
        
        self.auto = False
        self.auto_button = tk.Button(button_frame, text="Start Auto-Refresh", command=self.toggle_auto)
        self.auto_button.pack(side=tk.LEFT, padx=5)

        self.update_output()

    def read_dmesg(self):
        try:
            output = subprocess.check_output(["dmesg"], text=True)
            return output
        except Exception as e:
            return f"Error running dmesg:\n{e}"

    def update_output(self):
        output = self.read_dmesg()
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, output)

    def auto_refresh(self):
        if self.auto:
            self.update_output()
            self.root.after(2000, self.auto_refresh)

    def toggle_auto(self):
        self.auto = not self.auto
        if self.auto:
            self.auto_button.config(text="Stop Auto-Refresh")
            self.auto_refresh()
        else:
            self.auto_button.config(text="Start Auto-Refresh")


if __name__ == "__main__":
    root = tk.Tk()
    app = DmesgApp(root)
    root.mainloop()
