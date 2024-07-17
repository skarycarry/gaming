import tkinter as tk
from pathlib import Path

class TextSaverApp:
    def __init__(self, filename):
        self.filename = filename
        self.filepath = Path(__file__).parent.parent / 'data' / f'{self.filename}_text.txt'
        
        self.root = tk.Tk()
        self.root.title("Text Entry")
        
        self.text_area = tk.Text(self.root, wrap=tk.WORD, height=20, width=50)
        self.text_area.pack(padx=10, pady=10)
        
        self.load_text()
        
        self.save_button = tk.Button(self.root, text="Save", command=self.save_text)
        self.save_button.pack(pady=10)
        
        self.root.mainloop()
    
    def load_text(self):
        if self.filepath.exists():
            with open(self.filepath, 'r') as file:
                text = file.read()
                self.text_area.insert(tk.END, text)
    
    def save_text(self):
        text = self.text_area.get("1.0", tk.END)
        with open(self.filepath, 'w') as file:
            file.write(text)
        self.root.destroy()
