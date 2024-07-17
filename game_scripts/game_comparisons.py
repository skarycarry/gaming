import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
from pathlib import Path

class ComparisonApp:
    def __init__(self, title, csv_path=Path(__file__).parent.parent / 'data' / 'comparisons.csv', root=None):
        self.root = root if root else tk.Tk()
        self.title = title
        self.csv_path = csv_path
        self.entries = []

        self.root.title(self.title)

        self.load_csv()

    def load_csv(self):
        if not os.path.exists(self.csv_path):
            # Create a new CSV file with a 1x1 matrix
            df = pd.DataFrame({self.title: [10]}, index=[self.title])
            df.to_csv(self.csv_path)
            messagebox.showinfo("CSV Created", f"CSV created with a single entry for {self.title}")
        else:
            # Read the existing CSV file
            self.df = pd.read_csv(self.csv_path, index_col=0)
            self.create_display_widgets()

    def create_display_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        for col in self.df.columns:
            label = ttk.Label(self.root, text=col)
            label.pack(anchor='w', padx=10, pady=5)

            entry = ttk.Entry(self.root)
            entry.pack(anchor='w', padx=10, pady=5)
            entry.insert(0, str(self.df.at[self.title, col]) if self.title in self.df.index else "")
            self.entries.append((col, entry))

        save_button = ttk.Button(self.root, text="Save", command=self.save_and_quit)
        save_button.pack(pady=10)

    def save_and_quit(self):
        self.save_data()
        self.root.destroy()  # Quit the application

    def save_data(self):
        title = self.title

        # Collect new data from entries
        new_data = {}
        for col, entry in self.entries:
            value = entry.get()
            new_data[col] = int(value) if value.isdigit() else 0

        if title in self.df.index:
            # Update existing row and column
            for col in new_data:
                self.df.at[title, col] = new_data[col]
                self.df.at[col, title] = new_data[col]
        else:
            # Create new row
            new_row = pd.Series(new_data, name=title)
            new_row[title] = 100  # Set the diagonal element to 100
            self.df = pd.concat([self.df, new_row.to_frame().T])

            # Add new column with zeros, then update it
            self.df[title] = 0
            for col in new_data:
                self.df.at[col, title] = new_data[col]

            # Set the diagonal element to 10
            self.df.at[title, title] = 10

        self.df.to_csv(self.csv_path)
        messagebox.showinfo("Save", f"Data saved to {self.csv_path}")
