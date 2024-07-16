import tkinter as tk
from tkinter import filedialog
from pathlib import Path

class TextSaverApp:
    def __init__(self, filename):
        self.filename = filename
        self.root = tk.Tk()
        self.root.title("Text Entry")
        
        self.text_area = tk.Text(self.root, wrap=tk.WORD, height=20, width=50)
        self.text_area.pack(padx=10, pady=10)
        
        self.save_button = tk.Button(self.root, text="Save", command=self.save_text)
        self.save_button.pack(pady=10)
        
        self.root.mainloop()
    
    def save_text(self):
        text = self.text_area.get("1.0", tk.END)
        with open(Path(__file__).parent.parent / 'data' / f'{self.filename}_text.txt', 'w') as file:
            file.write(text)
        self.root.destroy()

# Usage
if __name__ == "__main__":
    save_path = "yup"
    app = TextSaverApp(save_path)
