import tkinter as tk
from tkinter import ttk, messagebox
import yaml
import os
from pathlib import Path

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

class FactorApp:
    def __init__(self, window_title, root=None, yaml_path=Path(__file__).parent.parent / 'game_type_descriptions' / 'game_factors.yaml'):
        self.root = root if root else tk.Tk()
        self.data = self.load_yaml_data(yaml_path)
        self.entries = []
        self.window_title = window_title

        self.create_widgets()
        self.root.title(self.window_title)
        self.load_existing_data()

    def load_yaml_data(self, yaml_path):
        if os.path.exists(yaml_path):
            with open(yaml_path, 'r') as file:
                return yaml.safe_load(file)
        else:
            messagebox.showerror("Error", f"File not found: {yaml_path}")
            self.root.quit()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        for key, value in self.data.items():
            frame = ScrollableFrame(self.notebook)
            self.notebook.add(frame, text=key)
            self.populate_frame(frame.scrollable_frame, value, key)

        save_button = ttk.Button(self.root, text="Save", command=self.save_and_quit)
        save_button.pack(pady=10)

    def populate_frame(self, frame, value, path):
        if isinstance(value, dict):
            self.add_subfields(frame, value, path)
        elif isinstance(value, list):
            self.add_factors(frame, value, path)

    def add_subfields(self, parent_frame, subfields, parent_path):
        notebook = ttk.Notebook(parent_frame)
        notebook.pack(expand=True, fill='both')

        for key, value in subfields.items():
            frame = ScrollableFrame(notebook)
            notebook.add(frame, text=key)
            self.populate_frame(frame.scrollable_frame, value, f"{parent_path}/{key}")

    def add_factors(self, parent_frame, factors, path):
        for factor in factors:
            label = ttk.Label(parent_frame, text=factor)
            label.pack(anchor='w', padx=10, pady=5)

            entry = ttk.Entry(parent_frame, validate='key', validatecommand=(self.root.register(self.validate_entry), '%P'))
            entry.pack(anchor='w', padx=10, pady=5)
            self.entries.append((path, factor, entry))

    def validate_entry(self, new_value):
        if new_value == "" or new_value.isdigit() and 0 <= int(new_value) <= 10:
            return True
        return False

    def save_and_quit(self):
        self.save_data()
        self.root.destroy()  # Quit the application

    def save_data(self):
        save_data = {}

        for path, factor, entry in self.entries:
            value = entry.get()
            if value == "":
                value = "0"
            value = int(value)

            # Construct nested dictionary structure based on path
            parts = path.split('/')
            d = save_data
            for part in parts:
                if part not in d:
                    d[part] = {}
                d = d[part]
            d[factor] = value

        save_path = Path(__file__).parent.parent / 'data' / f'{self.window_title}_data.yaml'
        with open(save_path, 'w') as file:
            yaml.dump(save_data, file)

        messagebox.showinfo("Save", f"Data saved to {save_path}")

    def load_existing_data(self):
        load_path = Path(__file__).parent.parent / 'data' / f'{self.window_title}_data.yaml'
        if os.path.exists(load_path):
            with open(load_path, 'r') as file:
                existing_data = yaml.safe_load(file)
                self.populate_entries(existing_data)

    def populate_entries(self, existing_data):
        for path, factor, entry in self.entries:
            parts = path.split('/')
            d = existing_data
            try:
                for part in parts:
                    d = d[part]
                if factor in d:
                    entry.insert(0, str(d[factor]))
            except KeyError:
                continue
